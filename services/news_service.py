import os

from dotenv import load_dotenv
from serpapi import GoogleSearch


load_dotenv()


def search_news(
    query,
    language="en"
):

    api_key = os.getenv(
        "SERPAPI_KEY"
    )

    if not api_key:
        raise ValueError(
            "SERPAPI_KEY is missing from .env"
        )

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
        "q": query,
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

    articles = []

    for item in news_results:

        source = item.get(
            "source",
            {}
        )

        source_name = (
            source.get("name", "")
            if isinstance(source, dict)
            else ""
        )

        link = item.get(
            "link",
            ""
        )

        if not source_name or not link:
            continue

        articles.append({

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
            ),

            "thumbnail": item.get(
                "thumbnail",
                ""
            ),

            "link": link

        })

    return articles