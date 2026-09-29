import os

from dotenv import load_dotenv
from serpapi import GoogleSearch


load_dotenv()


def get_related_sources(
    article,
    language="en"
):

    api_key = os.getenv(
        "SERPAPI_KEY"
    )

    if not api_key:
        raise ValueError(
            "SERPAPI_KEY is missing from .env"
        )

    title = article.get(
        "title",
        ""
    ).strip()

    if not title:
        return []

    language_map = {
        "en": "en",
        "hi": "hi"
    }

    hl = language_map.get(
        language,
        "en"
    )

    params = {

        "engine": "google_news",

        "q": title,

        "hl": hl,

        "api_key": api_key

    }

    search = GoogleSearch(
        params
    )

    results = search.get_dict()

    news_results = results.get(
        "news_results",
        []
    )

    sources = []

    selected_link = article.get(
        "link",
        ""
    )

    blocked_sources = {

        "facebook.com",
        "facebook",

        "instagram.com",
        "instagram",

        "x.com",
        "twitter"

    }

    for item in news_results:

        source = item.get(
            "source",
            {}
        )

        if isinstance(
            source,
            dict
        ):

            source_name = source.get(
                "name",
                ""
            )

        else:

            source_name = ""

        link = item.get(
            "link",
            ""
        )

        if not source_name or not link:
            continue

        if link == selected_link:
            continue

        source_lower = source_name.lower()

        if any(
            blocked in source_lower
            for blocked in blocked_sources
        ):
            continue

        sources.append({

            "title": item.get(
                "title",
                ""
            ),

            "source": source_name,

            "date": item.get(
                "date",
                ""
            ),

            "snippet": item.get(
                "snippet",
                ""
            ).strip(),

            "link": link

        })

        if len(sources) >= 5:
            break

    return sources