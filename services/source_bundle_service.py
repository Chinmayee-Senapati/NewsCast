
import re
from urllib.parse import urlparse


def select_relevant_liveblog_text(article_text, title, url):
    """Return the relevant live-blog update, or an empty string if uncertain."""

    if not article_text or not title:
        return article_text

    # Detect likely live-blog URLs or pages with multiple timestamped updates.
    is_liveblog_url = "liveblog" in urlparse(url).path.lower()

    timestamp_pattern = re.compile(
        r"(?m)^\s*\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?\s*(?:IST|GMT|UTC)?\s*,?\s*"
        r"\d{1,2}\s+[A-Za-z]+\s+\d{4}\s*$",
        re.IGNORECASE
    )

    timestamps = list(timestamp_pattern.finditer(article_text))

    if not is_liveblog_url and len(timestamps) < 2:
        return article_text

    # Split the page into timestamped updates.
    if len(timestamps) < 2:
        return ""

    sections = []

    for index, match in enumerate(timestamps):
        start = match.start()
        end = (
            timestamps[index + 1].start()
            if index + 1 < len(timestamps)
            else len(article_text)
        )
        section = article_text[start:end].strip()

        if section:
            sections.append(section)

    # Compare title words with each update, ignoring common words.
    stop_words = {
        "the", "a", "an", "and", "or", "to", "in", "on", "of",
        "for", "after", "amid", "with", "as", "is", "are", "was",
        "were", "it", "its", "by", "from", "that", "this", "their",
        "news", "update", "updates", "live", "latest", "breaking",
        "urges", "urge"
    }

    def meaningful_words(text):
        words = re.findall(r"[a-z0-9]+", text.lower())
        return {word for word in words if len(word) > 2 and word not in stop_words}

    title_words = meaningful_words(title)

    if not title_words:
        return ""

    scored_sections = []

    for section in sections:
        # The first line after the timestamp is usually the update headline.
        section_lines = [
            line.strip()
            for line in section.splitlines()
            if line.strip()
        ]

        if len(section_lines) < 2:
            continue

        headline = section_lines[1]
        headline_words = meaningful_words(headline)
        overlap = title_words & headline_words

        if len(overlap) >= 2:
            score = len(overlap) / len(title_words)
            scored_sections.append((score, len(overlap), section))

    if not scored_sections:
        return ""

    scored_sections.sort(key=lambda item: (item[0], item[1]), reverse=True)

    # If the best match is tied with another update, avoid guessing.
    best = scored_sections[0]
    if len(scored_sections) > 1:
        second = scored_sections[1]
        if best[:2] == second[:2]:
            return ""

    return best[2]

SOURCE_GROUNDING_RULES = """
PODCAST FACT-CHECKING RULES

1. Treat the PRIMARY ARTICLE as the main source for the episode.
2. Use extracted article text only for claims it actually supports.
3. A search snippet supports only the information stated in that snippet.
4. A related source's headline or metadata does not establish details
   that are not present in its available information.
5. Do not combine separate sources into a claim unless the available
   information from those sources supports that connection.
6. Never invent direct quotes, statistics, names, dates, or attributions.
7. Clearly distinguish reported facts, opinions, predictions, and
   hypothetical scenarios.
8. If the available material does not establish a detail, say so or
   leave it out.
9. Use related sources for relevant supporting context, not as a
   replacement for missing primary-article evidence.
10. Do not claim to have independently verified information unless
    the supplied source material establishes that verification.
"""

def build_source_bundle(article, related_sources):

    lines = []

    # ==========================================
    # PRIMARY ARTICLE
    # ==========================================

    lines.append("PRIMARY ARTICLE")
    lines.append("=" * 40)

    lines.append(
        f"Title: {article.get('title', '')}"
    )

    lines.append(
        f"Source: {article.get('source', '')}"
    )

    lines.append(
        f"Date: {article.get('date', '')}"
    )


    article_text = article.get("article_text", "").strip()
    snippet = article.get("snippet", "").strip()

    article_text = select_relevant_liveblog_text(
        article_text,
        article.get("title", ""),
        article.get("link", "")
    )

    if not article_text:
        print(
            "Live-blog filtering could not identify a relevant update. "
            "Using the available snippet instead."
        )
    if article_text:
        lines.append("Full extracted article text:")
        lines.append(article_text)

        if snippet:
            lines.append(
                f"Original search snippet: {snippet}"
            )

    elif snippet:
        lines.append(
            f"Available article information: {snippet}"
        )

    else:
        lines.append(
            "Available article information: "
            "No article text or snippet is available."
        )


    lines.append(
        f"URL: {article.get('link', '')}"
    )

    lines.append("")


    # ==========================================
    # RELATED SOURCES
    # ==========================================

    lines.append("RELATED SOURCES")
    lines.append("=" * 40)

    if not related_sources:

        lines.append(
            "No related sources were found."
        )

    else:

        for index, source in enumerate(
            related_sources,
            start=1
        ):

            lines.append(
                f"RELATED SOURCE {index}"
            )

            lines.append(
                f"Title: {source.get('title', '')}"
            )

            lines.append(
                f"Source: {source.get('source', '')}"
            )

            lines.append(
                f"Date: {source.get('date', '')}"
            )

            source_snippet = source.get(
                "snippet",
                ""
            ).strip()

            if source_snippet:

                lines.append(
                    f"Available information: "
                    f"{source_snippet}"
                )

            else:

                lines.append(
                    "Available information: "
                    "Only the headline and metadata "
                    "are available."
                )

            lines.append(
                f"URL: {source.get('link', '')}"
            )

            lines.append("")


    return SOURCE_GROUNDING_RULES + "\n\n" + "\n".join(lines)
