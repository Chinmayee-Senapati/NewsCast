import asyncio
import os
import re
import subprocess
from datetime import datetime

import edge_tts
import imageio_ffmpeg


VOICE_MAP = {
    "en": {
        "host": "en-IN-NeerjaNeural",
        "expert": "en-IN-PrabhatNeural"
    },
    "hi": {
        "host": "hi-IN-SwaraNeural",
        "expert": "hi-IN-MadhurNeural"
    }
}


# ---------------------------------------------------------
# PARSE PODCAST SCRIPT
# ---------------------------------------------------------

def parse_script(script):
    if not script:
        return []

    pattern = re.compile(
        r"^\s*\**\s*(HOST|EXPERT)\s*:\s*\**\s*(.*?)"
        r"(?=^\s*\**\s*(?:HOST|EXPERT)\s*:\s*\**|\Z)",
        re.IGNORECASE | re.MULTILINE | re.DOTALL
    )

    turns = []

    for match in pattern.finditer(script):
        speaker = match.group(1).lower()
        text = match.group(2).strip()

        if not text:
            continue

        # Remove Markdown formatting around speaker labels
        text = re.sub(
            r"^\s*\**\s*(HOST|EXPERT)\s*:\s*\**\s*",
            "",
            text,
            flags=re.IGNORECASE
        ).strip()

        # Remove stray Markdown bold markers
        text = text.replace("**", "").strip()

        if text:
            turns.append((speaker, text))

    return turns
# ---------------------------------------------------------
# GENERATE ONE VOICE SEGMENT
# ---------------------------------------------------------

async def generate_voice(
    text,
    voice,
    output_path
):
    communicate = edge_tts.Communicate(
        text,
        voice
    )

    await communicate.save(
        output_path
    )


# ---------------------------------------------------------
# GENERATE ALL SPEAKER SEGMENTS
# ---------------------------------------------------------

async def generate_speaker_segments(
    turns,
    language,
    temp_directory
):

    if language not in VOICE_MAP:
        raise ValueError(
            f"TTS is not configured for language: {language}"
        )

    voices = VOICE_MAP[language]

    segment_paths = []

    for index, (speaker, text) in enumerate(turns):

        voice = voices.get(speaker)

        if not voice:
            raise ValueError(
                f"No voice configured for speaker: {speaker}"
            )

        filename = (
            f"segment_{index:03d}_{speaker}.mp3"
        )

        output_path = os.path.join(
            temp_directory,
            filename
        )

        print(
            f"Generating {speaker.upper()} segment "
            f"{index + 1}..."
        )

        await generate_voice(
            text,
            voice,
            output_path
        )

        segment_paths.append(
            output_path
        )

    return segment_paths


# ---------------------------------------------------------
# COMBINE SEGMENTS IN ORDER
# ---------------------------------------------------------

def combine_audio(
    segment_paths,
    output_path
):

    if not segment_paths:
        raise ValueError(
            "No audio segments were generated."
        )

    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    # Create a temporary concat file.
    concat_file = os.path.join(
        os.path.dirname(output_path),
        "concat_list.txt"
    )

    with open(
        concat_file,
        "w",
        encoding="utf-8"
    ) as file:

        for segment_path in segment_paths:

            absolute_path = os.path.abspath(
                segment_path
            )

            # FFmpeg concat file requires
            # single quotes around paths.
            safe_path = absolute_path.replace(
                "'",
                "'\\''"
            )

            file.write(
                f"file '{safe_path}'\n"
            )

    command = [
        ffmpeg_path,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        concat_file,
        "-codec:a",
        "libmp3lame",
        "-q:a",
        "4",
        output_path
    ]

    subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if os.path.exists(concat_file):
        os.remove(concat_file)


# ---------------------------------------------------------
# MAIN PODCAST AUDIO GENERATOR
# ---------------------------------------------------------

def generate_podcast_audio(
    script,
    language
):

    if not script:
        raise ValueError(
            "Podcast script is empty."
        )

    if language not in VOICE_MAP:
        raise ValueError(
            f"Podcast audio is not available "
            f"for language: {language}"
        )

    # -----------------------------------------
    # Parse conversation
    # -----------------------------------------

    turns = parse_script(script)

    if not turns:
        raise ValueError(
            "No HOST/EXPERT conversation "
            "was found in the podcast script."
        )

    print(
        f"\nParsed {len(turns)} podcast turns."
    )

    for index, (speaker, text) in enumerate(
        turns,
        start=1
    ):
        preview = text[:80]

        print(
            f"Turn {index}: "
            f"{speaker.upper()} → {preview}"
        )

    # -----------------------------------------
    # Create directories
    # -----------------------------------------

    os.makedirs(
        "audio",
        exist_ok=True
    )

    temp_directory = os.path.join(
        "audio",
        "temp"
    )

    os.makedirs(
        temp_directory,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"podcast_{language}_{timestamp}.mp3"
    )

    output_path = os.path.join(
        "audio",
        filename
    )

    segment_paths = []

    try:

        # -----------------------------------------
        # Generate each speaker's segment
        # -----------------------------------------

        segment_paths = asyncio.run(
            generate_speaker_segments(
                turns,
                language,
                temp_directory
            )
        )

        # -----------------------------------------
        # Combine in conversation order
        # -----------------------------------------

        print(
            "\nCombining podcast segments..."
        )

        combine_audio(
            segment_paths,
            output_path
        )

        print(
            f"Podcast audio created: {filename}"
        )

    finally:

        # -----------------------------------------
        # Delete temporary segments
        # -----------------------------------------

        for segment_path in segment_paths:

            if os.path.exists(segment_path):
                os.remove(segment_path)

    return filename