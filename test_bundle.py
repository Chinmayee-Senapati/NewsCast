from services.source_service import get_related_sources
from services.source_bundle_service import build_source_bundle


article = {
    "title": "Artificial intelligence safety concerns",
    "source": "AP News",
    "date": "09/29/2026",
    "snippet": (
        "A recent discussion has highlighted concerns "
        "surrounding the safety of artificial intelligence "
        "and how governments and technology companies "
        "should approach these risks."
    ),
    "link": (
        "https://apnews.com/article/"
        "pope-trump-artificial-intelligence-anthropic-"
        "0790f258461d114c920ec6158c2a1921"
    )
}


related_sources = get_related_sources(
    article,
    "en"
)


bundle = build_source_bundle(
    article,
    related_sources
)


print("\n")
print("=" * 60)
print("SOURCE BUNDLE")
print("=" * 60)
print("\n")

print(bundle)