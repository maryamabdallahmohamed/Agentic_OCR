import os
from tqdm import tqdm
from pdf2image import convert_from_path
import re
from bs4 import BeautifulSoup

def pdf_to_images(pdf_paths, dpi=300):
    if isinstance(pdf_paths, str):
        pdf_paths = [pdf_paths]
    elif not isinstance(pdf_paths, (list, tuple)):
        raise TypeError("pdf_paths must be a string or a list/tuple of paths")

    images = []

    for path in tqdm(pdf_paths, desc="Converting PDFs"):
        if not os.path.isfile(path):
            print(f"Skipping missing file: {path}")
            continue

        if not path.lower().endswith(".pdf"):
            print(f"Skipping non-PDF file: {path}")
            continue

        images.extend(convert_from_path(path, dpi=dpi))

    return images

def remove_tashkeel(text):
    tashkeel_pattern = re.compile(r'[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]')
    return tashkeel_pattern.sub('', text)

def normalize_arabic(text):
    """
    Normalize Arabic text.
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
    text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text)
    text = re.sub(r'[A-Za-z0-9]+', '', text)
    text=text.replace("[غير واضح]", "")
    text=text.replace("<>", "")
    text=text.replace(">", "")
    text=text.replace(">", "")
    text=text.replace("\n", " ")
    text=remove_tashkeel(text)
    return text.strip()

def html_to_text(text):
    """
    Convert HTML content to plain text.
    """
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(separator=" ")
    return text

