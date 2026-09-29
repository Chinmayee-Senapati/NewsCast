import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def generate_podcast_script(
    source_bundle,
    language="en"
):

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing from .env"
        )

    client = Groq(
        api_key=api_key,
        timeout=60.0,
        max_retries=2
    )

    language_names = {

        "en": "English",

        "hi": "Hindi"

    }

    selected_language = language_names.get(
        language,
        "English"
    )

    prompt = f"""
Create a short news podcast script in
{selected_language}.

The podcast should sound like a natural
conversation between two speakers:

HOST:
Introduces the story and asks questions.

EXPERT:
Explains the information available in
the sources.

IMPORTANT GROUNDING RULES:

1. Use ONLY information contained in the
SOURCE BUNDLE below.

2. The PRIMARY ARTICLE is the main source
for the story.

3. RELATED SOURCES may provide supporting
context.

4. Do NOT treat a related-source headline
as if you have read the full article.

5. If a related source says
"Only the headline and metadata are available",
you MUST NOT infer additional facts from
that source.

6. Do NOT invent names of hosts, experts,
researchers, organizations, politicians,
or other people.

7. Do NOT invent quotes, statistics,
dates, locations, events, credentials,
or institutions.

8. Do NOT use outside knowledge.

9. If the available information does not
answer a question, explicitly say that
the available sources do not provide that
information.

10. Keep the conversation factual,
neutral, and easy to understand.

11. Clearly distinguish facts from
uncertainty.

12. Do not present speculation as fact.

13. Keep the conversation around
2-3 minutes when spoken.

14. Write the entire script in
{selected_language}.

15. Use exactly these speaker labels:

HOST:
EXPERT:

SOURCE BUNDLE:

{source_bundle}
"""

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[

            {
                "role": "system",
                "content": (
                    "You are a factual news podcast "
                    "script writer. "
                    "You must never invent information. "
                    "The provided source bundle is "
                    "your only source of factual "
                    "information."
                )
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.3,

        max_completion_tokens=1500

    )

    return response.choices[0].message.content
    
