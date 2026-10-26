import time
import streamlit as st

from deep_translator import GoogleTranslator
from deep_translator.exceptions import TooManyRequests


@st.cache_data(show_spinner=False)
def translate_summary(text, language="English"):

    text = str(text).strip()

    if not text:
        return ""

    if language == "English":
        return text

    if language == "Tamil":

        try:
            translator = GoogleTranslator(
                source="en",
                target="ta"
            )

            result = translator.translate(text)

            return result

        except TooManyRequests:
            return (
                "Tamil translation is temporarily unavailable "
                "due to the translation service request limit. "
                "Please try again later."
            )

        except Exception:
            return (
                "Tamil translation is temporarily unavailable. "
                "Please check your internet connection."
            )

    return text


def get_multilingual_summary(summary, language):

    results = []

    for item in summary:

        english_text = item["text"]

        translated = {
            "title": item["title"],
            "page": item["page"],
            "english": english_text,
            "tamil": ""
        }

        if language in ("Tamil", "Both"):

            translated["tamil"] = translate_summary(
                english_text,
                "Tamil"
            )

            # Avoid sending many requests immediately.
            time.sleep(1)

        results.append(translated)

    return results