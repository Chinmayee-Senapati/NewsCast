
import os
import re
from urllib.parse import urlparse

from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()


def _normalise_text(text):
    """Convert text to lowercase words for basic relevance checks."""
    return set(
        re.findall(r"[a-z0-9]+", (text or "").lower())
    )


def _normalise_url(url):
    """Ignore URL query strings, fragments, and trailing slashes."""
    if not url:
        return ""

    parsed = urlparse(url.strip())

    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]

    path = parsed.path.rstrip("/")

    return f"{host}{path}".lower()


def get_related_sources(article, language="en"):
    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        raise ValueError("SERPAPI_KEY is missing from .env")

    title = (article.get("title") or "").strip()

    if not title:
        return []

    language_map = {
        "en": "en",
        "hi": "hi",
    }

    hl = language_map.get(language, "en")

    # Search the article title and its central concepts.
    params = {
        "engine": "google_news",
        "q": title,
        "hl": hl,
        "api_key": api_key,
    }
    results = GoogleSearch(params).get_dict()
    news_results = results.get("news_results", [])

    selected_url = _normalise_url(article.get("link", ""))

    # Ignore generic words that provide little topical information.
    stop_words = {
        "the", "a", "an", "and", "or", "but", "of", "to",
        "in", "on", "for", "with", "by", "from", "is", "are",
        "was", "were", "be", "this", "that", "how", "what",
        "why", "may", "could", "would", "should", "you",
        "your", "its", "their", "they", "it", "as", "at",
        "has", "have", "had", "not", "all", "about",
    }

    primary_words = _normalise_text(title) - stop_words

    # Very short titles are not reliable enough for strict filtering.
    if len(primary_words) < 2:
        return []

    sources = []
    seen_urls = set()

    blocked_sources = {
        "facebook.com",
        "facebook",
        "instagram.com",
        "instagram",
        "x.com",
        "twitter",
    }

    for item in news_results:
        source = item.get("source", {})

        if isinstance(source, dict):
            source_name = source.get("name", "")
        else:
            source_name = ""

        link = item.get("link", "")
        result_title = (item.get("title") or "").strip()

        if not source_name or not link or not result_title:
            continue

        normalised_url = _normalise_url(link)

        # Exclude the original article and duplicate URLs.
        if normalised_url == selected_url:
            continue

        if not normalised_url or normalised_url in seen_urls:
            continue

        source_lower = source_name.lower()

        if any(blocked in source_lower for blocked in blocked_sources):
            continue

        result_words = _normalise_text(result_title) - stop_words

        # Keep results sharing at least two meaningful title words.
        # This is a basic filter, not a guarantee of factual relevance.
        overlap = primary_words & result_words

        if len(overlap) < 2:
            continue

        sources.append({
            "title": result_title,
            "source": source_name,
            "date": item.get("date", ""),
            "snippet": (item.get("snippet") or "").strip(),
            "link": link,
        })

        seen_urls.add(normalised_url)

        if len(sources) >= 3:
            break

    return sources
