import asyncio
import base64
import os
import re
import shutil
import subprocess
import tempfile
import time
import traceback
from datetime import datetime
from pathlib import Path

import edge_tts
import imageio_ffmpeg
from dotenv import load_dotenv
from sarvamai import SarvamAI
from sarvamai.core.api_error import ApiError

load_dotenv()


# ==================================================
# VOICE CONFIGURATION
# ==================================================

VOICE_MAP = {
    "en": {
        "HOST": "en-IN-NeerjaNeural",
        "EXPERT": "en-IN-PrabhatNeural",
    },
    "hi": {
        "HOST": "hi-IN-SwaraNeural",
        "EXPERT": "hi-IN-MadhurNeural",
    },
}

SARVAM_VOICE_MAP = {
    "HOST": "shubh",
    "EXPERT": "ritu",
}


# ==================================================
# PARSE PODCAST SCRIPT
# ==================================================

def parse_script(script):
    """
    Convert a script into:
    [
        ("HOST", "Welcome to the podcast."),
        ("EXPERT", "Let's begin.")
    ]
    """

    if not script or not script.strip():
        raise ValueError("Podcast script is empty.")

    turns = []

    pattern = re.compile(
        r"^\s*(HOST|EXPERT)\s*:\s*(.*?)\s*$",
        re.IGNORECASE,
    )

    for line in script.splitlines():
        line = line.strip()

        if not line:
            continue

        match = pattern.match(line)

        if not match:
            continue

        speaker = match.group(1).upper()
        text = match.group(2).strip()

        if text:
            turns.append((speaker, text))

    if not turns:
        raise ValueError(
            "No HOST or EXPERT dialogue was found in the script."
        )

    return turns


# ==================================================
# ENGLISH AND HINDI TTS
# ==================================================

async def generate_voice(text, voice, output_path):
    """Generate an audio segment using Edge TTS."""

    if not text or not text.strip():
        raise ValueError("Cannot generate audio from empty text.")

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
    )

    await communicate.save(output_path)

    if (
        not os.path.exists(output_path)
        or os.path.getsize(output_path) == 0
    ):
        raise RuntimeError(
            f"Edge TTS did not create a valid audio file: {output_path}"
        )


# ==================================================
# ODIA TTS USING SARVAMAI
# ==================================================

def generate_sarvam_voice(text, output_path, speaker):
    """
    Generate Odia speech with SarvamAI.

    Important:
    - A 402 insufficient-quota error is not retried.
    - Other API failures are raised to the caller.
    - WAV output is converted to MP3 using FFmpeg.
    """

    api_key = os.getenv("SARVAM_API_KEY")

    if not api_key:
        raise RuntimeError(
            "SARVAM_API_KEY is missing from the .env file."
        )

    if not text or not text.strip():
        raise ValueError("Cannot generate audio from empty text.")

    client = SarvamAI(
        api_subscription_key=api_key
    )

    print(f"Generating Odia speech for speaker {speaker}...")

    try:
        result = client.text_to_speech.convert(
            text=text,
            language_code="od-IN",
            model="bulbul:v3",
            speaker=speaker,
            pace=1.0,
            speech_sample_rate=22050,
        )

    except ApiError as exc:
        status_code = getattr(exc, "status_code", None)
        error_body = getattr(exc, "body", None)

        if status_code == 402:
            raise RuntimeError(
                "Odia audio generation failed: SarvamAI reports "
                "'No credits available'. Add credits to the account "
                "or configure another Odia TTS provider."
            ) from exc

        if status_code == 429:
            raise RuntimeError(
                "SarvamAI rate limit reached. Please wait before "
                "trying Odia podcast generation again."
            ) from exc

        raise RuntimeError(
            f"SarvamAI returned API status {status_code}: {error_body}"
        ) from exc

    if not getattr(result, "audios", None):
        raise RuntimeError("SarvamAI returned no audio data.")

    wav_path = output_path + ".wav"

    try:
        audio_data = base64.b64decode(result.audios[0])

        if not audio_data:
            raise RuntimeError("SarvamAI returned empty audio data.")

        with open(wav_path, "wb") as audio_file:
            audio_file.write(audio_data)

        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

        subprocess.run(
            [
                ffmpeg_path,
                "-y",
                "-i",
                wav_path,
                "-codec:a",
                "libmp3lame",
                "-q:a",
                "4",
                output_path,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if (
            not os.path.exists(output_path)
            or os.path.getsize(output_path) == 0
        ):
            raise RuntimeError(
                "FFmpeg did not create a valid Odia MP3 segment."
            )

    except subprocess.CalledProcessError as exc:
        details = exc.stderr or str(exc)

        raise RuntimeError(
            f"Failed to convert Odia audio to MP3: {details}"
        ) from exc

    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)


# ==================================================
# GENERATE INDIVIDUAL SPEAKER SEGMENTS
# ==================================================

async def generate_speaker_segments(
    turns,
    language,
    temp_directory,
):
    """
    Generate one audio segment for each HOST/EXPERT turn.

    English and Hindi use Edge TTS.
    Odia uses SarvamAI.
    """

    language = (language or "en").lower().strip()

    if language not in ("en", "hi", "or"):
        raise ValueError(
            f"Unsupported podcast language: {language}"
        )

    segment_paths = []

    for index, (speaker, text) in enumerate(turns, start=1):
        speaker = speaker.upper()
        text = text.strip()

        if speaker not in ("HOST", "EXPERT"):
            continue

        if not text:
            continue

        output_path = os.path.join(
            temp_directory,
            f"segment_{index:03d}.mp3",
        )

        print(f"Generating {speaker} segment {index}...")

        try:
            if language == "or":
                sarvam_speaker = SARVAM_VOICE_MAP[speaker]

                # SarvamAI's SDK call is synchronous.
                await asyncio.to_thread(
                    generate_sarvam_voice,
                    text,
                    output_path,
                    sarvam_speaker,
                )

            else:
                voice = VOICE_MAP[language][speaker]

                await generate_voice(
                    text,
                    voice,
                    output_path,
                )

            if (
                not os.path.exists(output_path)
                or os.path.getsize(output_path) == 0
            ):
                raise RuntimeError(
                    f"Segment {index} was not generated correctly."
                )

            segment_paths.append(output_path)

        except Exception:
            # Remove a partially written segment.
            if os.path.exists(output_path):
                os.remove(output_path)

            raise

    if not segment_paths:
        raise RuntimeError("No audio segments were generated.")

    return segment_paths


# ==================================================
# COMBINE SEGMENTS INTO ONE PODCAST
# ==================================================

def combine_audio(segment_paths, output_path):
    """Combine generated MP3 segments in the correct order."""

    if not segment_paths:
        raise ValueError("No audio segments were provided.")

    for path in segment_paths:
        if (
            not os.path.exists(path)
            or os.path.getsize(path) == 0
        ):
            raise RuntimeError(
                f"Audio segment is missing or empty: {path}"
            )

    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    concat_list_path = output_path + ".concat.txt"

    try:
        with open(
            concat_list_path,
            "w",
            encoding="utf-8",
        ) as list_file:
            for path in segment_paths:
                absolute_path = os.path.abspath(path)
                escaped_path = absolute_path.replace("\\", "/")
                escaped_path = escaped_path.replace("'", "'\\''")

                list_file.write(
                    f"file '{escaped_path}'\n"
                )

        subprocess.run(
            [
                ffmpeg_path,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                concat_list_path,
                "-c:a",
                "libmp3lame",
                "-q:a",
                "4",
                output_path,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if (
            not os.path.exists(output_path)
            or os.path.getsize(output_path) == 0
        ):
            raise RuntimeError(
                "FFmpeg did not create the combined podcast."
            )

    except subprocess.CalledProcessError as exc:
        details = exc.stderr or str(exc)

        raise RuntimeError(
            f"Failed to combine podcast audio: {details}"
        ) from exc

    finally:
        if os.path.exists(concat_list_path):
            os.remove(concat_list_path)


# ==================================================
# MAIN PODCAST AUDIO GENERATOR
# ==================================================

def generate_podcast_audio(script, language):
    """
    Generate the complete podcast MP3.

    Returns:
        Filename of the generated podcast.

    Raises:
        RuntimeError or ValueError if generation fails.
    """

    language = (language or "en").lower().strip()

    turns = parse_script(script)

    audio_directory = Path("audio")
    audio_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"podcast_{language}_{timestamp}.mp3"
    output_path = str(audio_directory / filename)

    temp_directory = tempfile.mkdtemp(
        prefix="newscast_audio_"
    )

    segment_paths = []

    try:
        print(
            f"Starting podcast audio generation "
            f"for language: {language}"
        )

        segment_paths = asyncio.run(
            generate_speaker_segments(
                turns,
                language,
                temp_directory,
            )
        )

        print("\nCombining podcast segments...")

        combine_audio(
            segment_paths,
            output_path,
        )

        print(f"Podcast audio created: {filename}")

        return filename

    except Exception as exc:
        print(f"Podcast audio generation failed: {exc}")
        traceback.print_exc()

        # Delete an incomplete final podcast.
        if os.path.exists(output_path):
            os.remove(output_path)

        # Re-raise so the Flask route can report the failure.
        raise

    finally:
        # Delete all temporary audio segments.
        for path in segment_paths:
            if os.path.exists(path):
                os.remove(path)

        # Clean up any remaining temporary files.
        shutil.rmtree(
            temp_directory,
            ignore_errors=True,
        )