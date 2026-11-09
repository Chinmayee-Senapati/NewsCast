import os
import re

import trafilatura
from dotenv import load_dotenv
from serpapi import GoogleSearch

from services.translation_service import translate_texts


load_dotenv()


def search_news(query, language="en"):
    """Search Google News and translate headlines when requested."""

    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        raise ValueError("SERPAPI_KEY is missing from .env")

    language_map = {
        "en": "en",
        "hi": "hi",
        "or": "or",
    }

    selected_language = language_map.get(language, "en")

    params = {
        "engine": "google_news",
        "q": query,
        "hl": selected_language,
        "api_key": api_key,
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    news_results = results.get("news_results", [])
    articles = []

    for item in news_results:
        source = item.get("source", {})

        source_name = (
            source.get("name", "")
            if isinstance(source, dict)
            else ""
        )

        link = item.get("link", "")

        if not source_name or not link:
            continue

        articles.append({
            "title": item.get("title", ""),
            "source": source_name,
            "date": item.get("date", ""),
            "snippet": item.get("snippet", ""),
            "thumbnail": item.get("thumbnail", ""),
            "link": link,
        })

    # Translate only headlines not already written in the target script.
    if language in ("hi", "or") and articles:
        if language == "hi":
            target_script = re.compile(r"[\u0900-\u097F]")
        else:  # Odia
            target_script = re.compile(r"[\u0B00-\u0B7F]")

        indexes_to_translate = [
            i
            for i, article in enumerate(articles)
            if article["title"]
            and not target_script.search(article["title"])
        ]

        titles_to_translate = [
            articles[i]["title"]
            for i in indexes_to_translate
        ]

        if titles_to_translate:
            translated_titles = translate_texts(
                titles_to_translate,
                target=language,
            )

            for index, translated_title in zip(
                indexes_to_translate, translated_titles
            ):
                articles[index]["title"] = translated_title

    return articles