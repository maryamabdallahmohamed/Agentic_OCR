from typing import List, Union, Optional, Dict, Any
import os
import re
from utils.get_logger import get_logger
from PIL import Image
from pdf2image import convert_from_path
from tqdm import tqdm
from surya.foundation import FoundationPredictor
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor
from src.ocr.text_normalization import normalize_arabic, html_to_text

# -----------------------------
# Text normalization utilities
# -----------------------------
logger = get_logger('ocr_pipeline')


class OCRPipeline:
    """
    Encapsulates Surya predictors and provides OCR helpers for images and PDFs.
    """

    def __init__(self, device: Optional[str] = "mps") -> None:
        logger.info("Initializing Surya predictors (device=%s)", device)
        self.foundation_predictor = FoundationPredictor(device=device) if device else FoundationPredictor()
        self.recognition_predictor = RecognitionPredictor(self.foundation_predictor)
        self.detection_predictor = DetectionPredictor()

    # -----------------------------
    # PDF -> Image conversion
    # -----------------------------
    def pdf_to_images(self, pdf_paths: Union[str, List[str]], dpi: int = 300) -> List[Image.Image]:
        """
        Convert one or more PDF files to PIL Images.
        - If `pdf_paths` is a string path, returns images for that single PDF.
        - If `pdf_paths` is a list of paths, returns concatenated images for all.
        """
        images: List[Image.Image] = []

        if isinstance(pdf_paths, str):
            if os.path.isfile(pdf_paths):
                logger.info("Converting single PDF to images: %s", pdf_paths)
                return convert_from_path(pdf_paths, dpi=dpi)
            raise ValueError("Single path provided, but file does not exist.")

        if isinstance(pdf_paths, list):
            for pdf_path in tqdm(pdf_paths, desc="Converting PDFs"):
                if os.path.isfile(pdf_path) and pdf_path.lower().endswith(".pdf"):
                    imgs = convert_from_path(pdf_path, dpi=dpi)
                    images.extend(imgs)
                else:
                    logger.warning("Skipping invalid PDF: %s", pdf_path)
            return images

        raise TypeError("pdf_paths must be a string or a list of PDF paths")

    # -----------------------------
    # Image OCR
    # -----------------------------
    def ocr_image(self, img: Image.Image) -> str:
        """Run OCR on a single PIL Image and return normalized text."""
        predictions = self.recognition_predictor([img], det_predictor=self.detection_predictor)
        lines: List[str] = []
        for item in predictions:
            text_lines = getattr(item, "text_lines", [])
            for text_line in text_lines:
                lines.append(text_line.text)
        raw_text = "\n".join(lines).strip()
        cleaned = normalize_arabic(raw_text)
        cleaned = html_to_text(cleaned)
        return cleaned

    # -----------------------------
    # PDF OCR end-to-end
    # -----------------------------


    def run_pdf_ocr( self, pdf_path_or_paths: Union[str, List[str]],dpi: int = 300,) -> Dict[int, Dict[str, Any]]:
        """
        Convert PDF(s) to images and run OCR page by page.
        Returns a dict keyed by page index with the OCR result.
        """
        pages = self.pdf_to_images(pdf_path_or_paths, dpi=dpi)
        results: Dict[int, Dict[str, Any]] = {}

        for idx, img in tqdm(enumerate(pages, start=1), desc="Running OCR"):
            pred_text = self.ocr_image(img)
            results[idx] = {
                "pred": pred_text,
            }
        return results
