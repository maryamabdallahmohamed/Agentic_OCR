from PIL import Image
import json
from src.ocr_pipeline.model import OCRPredictor
from src.ocr_pipeline.layout import LayoutDetector
from src.ocr_pipeline.preprocessing import pdf_to_images, normalize_arabic, html_to_text
from tqdm import tqdm

ocrpredictor = OCRPredictor()
layoutdetector = LayoutDetector()
def OCR(img): 
    predictions = ocrpredictor.recognition_predictor([img], det_predictor=layoutdetector.get_predictor()) 
    ocr_text = '' 
    for item in predictions: 
        text_lines = item.text_lines 
        for text_line in text_lines: 
            text = text_line.text 
            ocr_text += text + '\n' 
    return ocr_text.strip()


def run_pdf_ocr(pdf_path, limit=None):
    pages = pdf_to_images(pdf_path, dpi=300)
    results = {}
    predictions = []

    for idx, page in tqdm(enumerate(pages, start=1), desc="Running OCR"):
    
        # OCR prediction
        pred_text = OCR(page)
        pred_text = normalize_arabic(pred_text)
        pred_text = html_to_text(pred_text)

        # Save for overall metrics
        predictions.append(pred_text)


        results[idx] = {
            "image": page, 
            "pred": pred_text
        }

    return results

results=run_pdf_ocr("/Users/maryamsaad/Documents/layout_detection/ocr/simplified.pdf")
print(results)