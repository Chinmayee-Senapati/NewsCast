
import os

from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
    send_from_directory,
)

from services.news_service import search_news
from services.ai_service import generate_podcast_script
from services.article_service import extract_article_text
from services.translation_service import translate_texts
from services.podcast_service import generate_podcast_audio
from services.source_service import get_related_sources
from services.source_bundle_service import build_source_bundle
from translations.translations import TRANSLATIONS


# ==========================================================
# CONFIGURATION
# ==========================================================

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "newscast-development-secret-key"
)

SUPPORTED_LANGUAGES = [
    "en",
    "hi",
    "or",
]


# ==========================================================
# LANGUAGE HELPERS
# ==========================================================

def get_current_language():
    language = session.get("language", "en")

    if language not in SUPPORTED_LANGUAGES:
        language = "en"

    return language


def get_translations(language):
    return TRANSLATIONS.get(
        language,
        TRANSLATIONS.get("en", {})
    )


def translate_news_results(results, language):
    """Translate article titles and snippets without changing source metadata."""
    if language == "en" or not results:
        return results

    texts = []

    for article in results:
        texts.append(article.get("title", ""))
        texts.append(article.get("snippet", ""))

    translated_texts = translate_texts(
        texts,
        target=language
    )

    for index, article in enumerate(results):
        article["title"] = translated_texts[index * 2]
        article["snippet"] = translated_texts[index * 2 + 1]

    return results


# ==========================================================
# HOME / LANGUAGE
# ==========================================================

@app.route("/")
def index():
    return render_template("language.html")


@app.route("/language")
def language():
    return render_template("language.html")


@app.route("/set-language", methods=["POST"])
def set_language():
    language = request.form.get(
        "language",
        ""
    ).strip()

    if language not in SUPPORTED_LANGUAGES:
        language = "en"

    session["language"] = language

    return redirect(url_for("home"))


# ==========================================================
# HOME
# ==========================================================

@app.route("/home")
def home():
    language = get_current_language()
    translations = get_translations(language)

    return render_template(
        "home.html",
        language=language,
        translations=translations
    )


# ==========================================================
# SEARCH
# ==========================================================

@app.route("/search")
def search():
    language = get_current_language()
    translations = get_translations(language)

    query = request.args.get(
        "q",
        ""
    ).strip()

    results = []

    if query:
        try:
            results = search_news(
                query,
                language=language
            )

        except Exception as error:
            print(f"News search failed: {error}")
            results = []

    return render_template(
        "search.html",
        query=query,
        results=results,
        language=language,
        translations=translations
    )


# ==========================================================
# TOPIC / ARTICLE
# ==========================================================

@app.route("/topic")
def topic():
    language = get_current_language()
    translations = get_translations(language)

    article = {
        "title": request.args.get("title", ""),
        "source": request.args.get("source", ""),
        "date": request.args.get("date", ""),
        "snippet": request.args.get("snippet", ""),
        "thumbnail": request.args.get("thumbnail", ""),
        "link": request.args.get("link", ""),
    }

    return render_template(
        "topic.html",
        article=article,
        language=language,
        translations=translations
    )


# ==========================================================
# TOPIC NEWS
# ==========================================================

@app.route("/news-topic/<topic_name>")
def news_topic(topic_name):
    language = get_current_language()
    translations = get_translations(language)

    topic_map = {
        "world": "World news",
        "india": "India news",
        "technology": "Technology news",
        "sports": "Sports news",
    }

    query = topic_map.get(topic_name.lower())

    if not query:
        return "Topic not found", 404

    try:
        results = search_news(
            query,
            language=language
        )

    except Exception as error:
        print(f"Topic news search failed: {error}")
        results = []

    return render_template(
        "search.html",
        query=query,
        results=results,
        language=language,
        translations=translations
    )


# ==========================================================
# GENERATE PODCAST
# ==========================================================

@app.route("/generate-podcast", methods=["POST"])
def generate_podcast():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "error": "No request data was provided."
            }), 400

        article = data.get("article", {})
        language = data.get("language") or get_current_language()

        # --------------------------------------------------
        # Validate language
        # --------------------------------------------------

        if language not in SUPPORTED_LANGUAGES:
            return jsonify({
                "success": False,
                "error": "Unsupported language."
            }), 400

        # --------------------------------------------------
        # Validate article
        # --------------------------------------------------

        if not isinstance(article, dict):
            return jsonify({
                "success": False,
                "error": "Invalid article data."
            }), 400

        title = article.get("title", "")

        if not isinstance(title, str):
            return jsonify({
                "success": False,
                "error": "Invalid article title."
            }), 400

        title = title.strip()

        if not title:
            return jsonify({
                "success": False,
                "error": "Article title is missing."
            }), 400

        # --------------------------------------------------
        # Keep article data consistent
        # --------------------------------------------------

        article_data = {
            "title": title,
            "source": article.get("source", ""),
            "date": article.get("date", ""),
            "snippet": article.get("snippet", ""),
            "thumbnail": article.get("thumbnail", ""),
            "link": article.get("link", ""),
        }

        print("\n" + "=" * 60)
        print("PODCAST GENERATION STARTED")
        print("=" * 60)

        # --------------------------------------------------
        # STEP 1: Collect related sources
        # --------------------------------------------------

        print("\nCollecting related sources...")

        related_sources = get_related_sources(
            article_data,
            language=language
        )

        print(
            f"Found {len(related_sources)} related sources."
        )

        # --------------------------------------------------
        # STEP 2: Extract primary article text
        # --------------------------------------------------

        print("\nExtracting primary article text...")

        article_text = extract_article_text(
            article_data.get("link", "")
        )

        if article_text:
            article_data["article_text"] = article_text

            print(
                f"Extracted {len(article_text)} characters."
            )
        else:
            print(
                "Full article unavailable; "
                "using the existing snippet."
            )

        # --------------------------------------------------
        # STEP 3: Build source bundle
        # --------------------------------------------------

        print("\nBuilding source bundle...")

        source_bundle = build_source_bundle(
            article_data,
            related_sources
        )

        # --------------------------------------------------
        # STEP 4: Generate AI podcast script
        # --------------------------------------------------

        print("\nGenerating podcast script...")

        script = generate_podcast_script(
            source_bundle,
            language=language
        )

        if not script:
            raise ValueError(
                "The AI did not generate a podcast script."
            )

        print("Podcast script generated.")

        # --------------------------------------------------
        # STEP 5: Generate podcast audio
        # --------------------------------------------------

        print(
            f"\nGenerating podcast audio for language: {language}..."
        )

        try:
            audio_filename = generate_podcast_audio(
                script,
                language
            )

            if not audio_filename:
                raise RuntimeError(
                    "The audio provider did not return an audio file."
                )

        except Exception as audio_error:
            print(
                f"Podcast audio generation failed: {audio_error}"
            )

            error_message = str(audio_error)

            # Give a clear message for the known SarvamAI quota issue.
            if language == "or" and (
                "No credits available" in error_message
                or "insufficient_quota_error" in error_message
                or "402" in error_message
            ):
                user_message = (
                    "Your podcast script was generated, but Odia audio "
                    "could not be created because your SarvamAI account "
                    "has no available credits. Add credits to SarvamAI "
                    "or configure another Odia text-to-speech provider."
                )
            else:
                user_message = (
                    "Your podcast script was generated, but audio "
                    f"generation failed: {error_message}"
                )

            # Do not report success when no audio was created.
            return jsonify({
                "success": False,
                "script": script,
                "audio_url": None,
                "audio_unavailable": True,
                "error": user_message,
                "sources": related_sources,
            }), 502

        # --------------------------------------------------
        # STEP 6: Return success only when audio is generated
        # --------------------------------------------------

        print(f"Podcast audio created: {audio_filename}")
        print("Podcast generation completed.")
        print("=" * 60 + "\n")

        return jsonify({
            "success": True,
            "script": script,
            "audio_url": f"/audio/{audio_filename}",
            "audio_unavailable": False,
            "sources": related_sources,
        }), 200

    except Exception as error:
        print(f"\nPodcast generation failed: {error}\n")

        return jsonify({
            "success": False,
            "error": (
                "Podcast generation failed. "
                "Please try again."
            )
        }), 500


# ==========================================================
# AUDIO
# ==========================================================

@app.route("/audio/<path:filename>")
def audio(filename):
    audio_directory = os.path.join(
        app.root_path,
        "audio"
    )

    file_path = os.path.join(
        audio_directory,
        filename
    )

    if not os.path.isfile(file_path):
        return jsonify({
            "error": "Audio file not found."
        }), 404

    return send_from_directory(
        audio_directory,
        filename
    )


# ==========================================================
# ERROR HANDLERS
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):
    return (
        render_template("language.html"),
        404
    )


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": "An internal server error occurred."
    }), 500


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
