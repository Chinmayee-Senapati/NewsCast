import asyncio
import edge_tts


async def generate_test():

    tests = [
        {
            "name": "english",
            "voice": "en-IN-NeerjaNeural",
            "text": (
                "Hello and welcome to Newscast. "
                "This is a test of the English podcast voice."
            )
        },
        {
            "name": "hindi",
            "voice": "hi-IN-SwaraNeural",
            "text": (
                "नमस्ते और न्यूज़कास्ट में आपका स्वागत है। "
                "यह हिंदी पॉडकास्ट आवाज़ का परीक्षण है।"
            )
        },
        {
            "name": "odia",
            "voice": "or-IN-SubhasiniNeural",
            "text": (
                "ନମସ୍କାର ଏବଂ ନ୍ୟୁଜକାଷ୍ଟକୁ ସ୍ୱାଗତ। "
                "ଏହା ଓଡ଼ିଆ ପଡକାଷ୍ଟ ଭଏସର ଏକ ପରୀକ୍ଷା।"
            )
        }
    ]

    for test in tests:

        print(f"\nGenerating {test['name']} voice...")

        communicate = edge_tts.Communicate(
            test["text"],
            test["voice"]
        )

        await communicate.save(
            f"audio/test_{test['name']}.mp3"
        )

        print(
            f"Created: audio/test_{test['name']}.mp3"
        )


asyncio.run(generate_test())