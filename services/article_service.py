import requests
import trafilatura


def extract_article_text(url):

    if not url:
        return ""

    try:
        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/154.0 Safari/537.36"
                )
            }
        )

        response.raise_for_status()

        text = trafilatura.extract(
            response.text,
            url=url,
            favor_precision=True
        )

        if not text:
            return ""

        # Keep the article reasonably small for the AI request.
        return text[:12000]

    except Exception as error:

        print(
            f"Article extraction failed: {error}"
        )

        return ""