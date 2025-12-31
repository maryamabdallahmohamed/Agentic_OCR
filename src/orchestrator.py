from typing import Union, List, Optional, Dict, Any
import os
import json
from utils.get_logger import get_logger
from utils.settings import Config
from src.ocr.pipeline import OCRPipeline

logging = get_logger('orchestrator')

class Orchestrator:
    """Coordinates OCR runs and handles outputs."""

    def __init__(self, device: Optional[str] = "mps", output_dir: str = "output") -> None:
        self.pipeline = OCRPipeline(device=device)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def run( self,input_path: Union[str, List[str]],output_filename: str = "_ocr.json",) -> Dict[int, Dict[str, Any]]:
        """
        Run OCR for the given input (single PDF path or list of paths).
        Writes a JSON file to `output_dir/output_filename` and returns the results.
        """
        logging.info("Starting OCR run ")
        results = self.pipeline.run_pdf_ocr(input_path)
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        logging.info("OCR results written to %s", output_path)
        return results




if __name__ == "__main__":
    path='/Users/maryamsaad/Documents/layout_detection/single_col_test.pdf'
    orch = Orchestrator(device=Config.DEVICE, output_dir=Config.OUTPUT_DIR)
    results=orch.run(path , output_filename='single_col_test_ocr.json')