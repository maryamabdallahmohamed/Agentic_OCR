from PIL import Image
from surya.foundation import FoundationPredictor
from surya.recognition import RecognitionPredictor

class OCRPredictor:
    def __init__(self):
        self.foundation_predictor = FoundationPredictor()
        self.recognition_predictor = RecognitionPredictor(self.foundation_predictor)

    def predict(self, images, detection_predictor):
        return self.recognition_predictor(images, det_predictor=detection_predictor)