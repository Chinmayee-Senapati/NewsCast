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

    snippet = article.get("snippet", "").strip()

    if snippet:
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


    return "\n".join(lines)