
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def generate_podcast_script(
    source_bundle,
    language="en"
):
    api_key = os.getenv("GROQ_API_KEY")

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
        "hi": "Hindi",
        "or": "Odia"
    }

    selected_language = language_names.get(
        language,
        "English"
    )

    prompt = f"""
Create a news podcast script in {selected_language}.

{'''
ODIA-ONLY LENGTH REQUIREMENTS:
- These length requirements apply only to Odia podcasts.
- Write approximately 350–400 spoken words, targeting 2–3 minutes.
- Include a meaningful introduction, source-supported details,
  explanatory questions and answers, and a conclusion.
- Alternate between HOST and EXPERT for multiple turns.
- Do not finish after only two or three exchanges.
- Use enough detail to explain the story, but never invent facts
  or repeat information merely to increase length.
''' if language == "or" else ""}


The podcast should sound like a natural,
clearly structured conversation between two speakers:

HOST:
Introduces the story and asks questions.

EXPERT:
Explains information from the supplied sources.
This is a scripted explanatory voice, not a real
interview or a claim that an actual expert joined.

IMPORTANT GROUNDING RULES:

1. Use ONLY information contained in the SOURCE BUNDLE.

2. The PRIMARY ARTICLE is the main source for the story.

3. RELATED SOURCES may provide supporting context,
but do not let them override the primary article.

4. Do NOT treat a related-source headline as if you
have read the full article.

5. If a related source says
"Only the headline and metadata are available",
do NOT infer additional facts from that source.

6. Do NOT invent names of hosts, experts, researchers,
organizations, politicians, or other people.

7. Do NOT invent quotes, statistics, dates, locations,
events, credentials, or institutions.

8. Do NOT use outside knowledge.

9. If the available information does not answer a
question, explicitly say the sources do not provide
that information.

10. Keep the conversation factual, neutral, and easy
to understand.

11. Clearly distinguish established facts from
uncertainty, opinion, and speculation.

12. Preserve attribution. Make clear who made a claim,
offered a recommendation, or expressed an opinion.
Do not attribute an individual's recommendation
to all the paper's authors unless the sources support it.

13. Clearly label hypothetical examples as hypothetical.
Do not add technical details to an example unless
they appear in the source or are clearly presented
as a simple illustration rather than a reported fact.

14. When discussing timelines or probabilities, state
only what the supplied sources establish. Do not turn
the absence of a forecast into a prediction.

15. Do not imply that a real interview took place.
The EXPERT is a scripted explanatory speaker, not
a real guest, unless the source bundle explicitly
documents an actual interview.

16. Aim for a 3–5 minute spoken episode by default,
adjusting the length to the complexity of the story and
the amount of reliable source material available.
A short story may be shorter; a complex story may need
more time. Do not sacrifice important context merely
to meet a time limit.

17. Write the entire script in {selected_language}.

18. Use exactly these speaker labels:

HOST:

EXPERT:

19. Return only the podcast dialogue. Do not include
Markdown formatting, introductory commentary, or
a separate summary.

20. Before finalizing the script, check every factual
claim against the supplied source bundle. Remove or
qualify any claim that cannot be supported.

Do not strengthen a source's wording or turn a
possibility into a certainty. Preserve important
qualifications and attribution.

21. Include enough relevant information for listeners to
understand the complete story. Explain the background,
chronology, key people or organizations, what happened,
what prompted the development, its reported significance,
and what remains unknown, whenever the SOURCE BUNDLE
supports those details. Do not invent missing context.
Do not add generic background or unsupported advice.

22. Avoid redundant repetition, but do not confuse repetition
with useful explanation. A fact may be revisited when doing
so helps explain its significance, connect two developments,
answer a question, or make an important detail easier to
understand. Do not remove context just to make the script
shorter.

23. Attribute announcements to the specific source identified
in the supplied material. Do not imply that a broader institution
or government body made a statement unless the supplied sources
support that attribution.

24. When related sources provide only headlines or metadata,
describe only what those headlines say. Do not imply that
their full articles were read, their reporting was verified,
or that they independently confirmed the primary source.

25. Keep the opening focused and engaging, giving listeners
enough context to understand the story. Use the closing to
explain the main takeaway or unresolved question. Avoid
repeating entire sections, but do not force the episode to
end before the story has been adequately explained.

26. Preserve the exact level of attribution in the supplied
sources. Do not name a ministry, department, or authority
as the issuer unless the source explicitly identifies it.

27. Never promise or imply that following advice will ensure
or guarantee personal safety. Summarize the source's actual
recommendations without adding assurances about their outcome.

28. Use a natural HOST–EXPERT conversation that develops
the story progressively. The HOST should ask meaningful
questions that help listeners understand the subject, and
the EXPERT should answer with relevant source-supported
details and explanations. The final EXPERT response may
provide a useful conclusion when appropriate, but must not
merely repeat the HOST's closing summary.

If the sources disagree, explain the disagreement
rather than silently choosing one version.

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
                    "script writer. You must never "
                    "invent information. The supplied "
                    "source bundle is your only source "
                    "of factual information. Preserve "
                    "attribution, distinguish hypothetical "
                    "examples from reported events, and "
                    "state uncertainty honestly."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_completion_tokens=(
            5000 if language == "or" else 1500
        )
    )

    script = response.choices[0].message.content

    if not script:
        raise ValueError(
            "Groq returned an empty podcast script."
        )

    return script.strip()
