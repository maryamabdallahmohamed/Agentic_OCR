import re
from bs4 import BeautifulSoup
_tashkeel_pattern = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]")

def remove_tashkeel(text: str) -> str:
    return _tashkeel_pattern.sub("", text)


def normalize_arabic(text: str) -> str:
    """
    Normalizes Arabic characters and removes OCR artifacts.
    Mirrors the transformations used in the notebook.
    """
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "و", text)
    text = re.sub("ئ", "ي", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("  ", " ", text)
    text = re.sub("[ًٌٍَُِّْ]", "", text)
    text = re.sub(r"[\|\)\(\:\-\;\\\/]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\b(\w+)\s+\1\b", r"\1", text)
    text = re.sub(r"[A-Za-z0-9]+", "", text)
    text = text.replace("[غير واضح]", "")
    text = text.replace("<>", "")
    text = text.replace(">", "")
    text = text.replace("\n", " ")
    text = remove_tashkeel(text)
    return text.strip()


def html_to_text(html_str: str) -> str:
    """Converts HTML content to plain text, preserving spaces between elements."""
    soup = BeautifulSoup(html_str, "html.parser")
    text = soup.get_text(separator=" ")
    return text
