from services.source_service import get_related_sources
from services.source_bundle_service import build_source_bundle
from services.ai_service import generate_podcast_script


article = {

    "title":
        "Artificial intelligence safety concerns",

    "source":
        "AP News",

    "date":
        "09/29/2026",

    "snippet":
        (
            "A recent discussion has highlighted "
            "concerns surrounding the safety of "
            "artificial intelligence and how "
            "governments and technology companies "
            "should approach these risks."
        ),

    "link":
        (
            "https://apnews.com/article/"
            "pope-trump-artificial-intelligence-"
            "anthropic-0790f258461d114c920ec6158c2a1921"
        )
}


print("\nCollecting related sources...\n")


related_sources = get_related_sources(
    article,
    "en"
)


print(
    f"Found {len(related_sources)} "
    "related sources."
)


print("\nBuilding source bundle...\n")


source_bundle = build_source_bundle(
    article,
    related_sources
)


print(
    "Generating podcast script...\n"
)


script = generate_podcast_script(
    source_bundle,
    "en"
)


print("\n")
print("=" * 60)
print("GENERATED PODCAST SCRIPT")
print("=" * 60)
print("\n")


print(script)