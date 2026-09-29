from services.source_service import get_related_sources


article = {
    "title": "Artificial intelligence safety concerns",
    "source": "AP News",
    "date": "09/29/2026",
    "snippet": "A recent discussion has highlighted concerns surrounding the safety of artificial intelligence.",
    "link": "https://apnews.com/article/pope-trump-artificial-intelligence-anthropic-0790f258461d114c920ec6158c2a1921"
}


sources = get_related_sources(article, "en")


print("\n")
print("=" * 60)
print("RELATED NEWS SOURCES")
print("=" * 60)
print("\n")


for index, source in enumerate(sources, start=1):

    print(f"SOURCE {index}")
    print("-" * 40)

    print("Title:", source["title"])
    print("Source:", source["source"])
    print("Date:", source["date"])
    print("Snippet:", source["snippet"])
    print("Link:", source["link"])

    print()