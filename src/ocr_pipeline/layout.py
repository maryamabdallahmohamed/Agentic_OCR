from surya.detection import DetectionPredictor
from utils.settings import detection_conf, Config

class LayoutDetector:
    def __init__(self):
        self.detection_predictor = DetectionPredictor(device=Config.DEVICE)

    def detect_boxes(self, image, threshold=detection_conf):
        results = self.detection_predictor([image])
        det_result = results[0]
        valid_bboxes = [b for b in det_result.bboxes if b.confidence >= threshold]
        return valid_bboxes
    
    def get_predictor(self):
        return self.detection_predictor