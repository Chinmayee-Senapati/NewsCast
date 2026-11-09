
import requests

TRANSLATION_SERVICE_URL = "http://127.0.0.1:8765"
TIMEOUT_SECONDS = 180
BATCH_SIZE = 16

# Cache translations so repeated UI labels do not need repeated requests.
_translation_cache = {}


def translate_texts(texts, target="hi"):
    """Translate English strings into Hindi or Odia in small batches."""

    if target == "en":
        return list(texts)

    if target not in ("hi", "or"):
        raise ValueError(f"Unsupported translation target: {target}")

    texts = list(texts)
    results = [None] * len(texts)
    missing = []
    missing_indexes = []

    # Reuse cached translations and collect uncached text.
    for index, text in enumerate(texts):
        if not isinstance(text, str) or not text.strip():
            results[index] = text
            continue

        key = (target, text)

        if key in _translation_cache:
            results[index] = _translation_cache[key]
        else:
            missing.append(text)
            missing_indexes.append(index)

    # Translate uncached text in small batches.
    for start in range(0, len(missing), BATCH_SIZE):
        batch = missing[start:start + BATCH_SIZE]
        batch_indexes = missing_indexes[start:start + BATCH_SIZE]

        response = requests.post(
            f"{TRANSLATION_SERVICE_URL}/translate",
            json={
                "texts": batch,
                "target": target,
            },
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()

        translated = response.json().get("translations", [])

        if len(translated) != len(batch):
            raise RuntimeError(
                "Translation service returned an unexpected result."
            )

        # Store translations in their original positions.
        for index, original, translated_text in zip(
            batch_indexes, batch, translated
        ):
            _translation_cache[(target, original)] = translated_text
            results[index] = translated_text

    return results


def translate_text(text, target="hi"):
    """Translate a single English string."""
    return translate_texts([text], target=target)[0]
