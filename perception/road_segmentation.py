from ultralytics import YOLO
import cv2
import numpy as np


class RoadSegmentation:

    def __init__(self):
        self.model = YOLO("yolov8n-seg.pt")

    def segment(self, frame):

        results = self.model(frame, verbose=False)

        return results

    def draw_masks(self, frame, results):

        annotated = frame.copy()

        for result in results:

            if result.masks is None:
                continue

            masks = result.masks.data.cpu().numpy()

            for mask in masks:

                mask = cv2.resize(
                    mask,
                    (frame.shape[1], frame.shape[0])
                )

                overlay = np.zeros_like(frame)

                overlay[:, :, 1] = (mask * 255).astype(np.uint8)

                annotated = cv2.addWeighted(
                    annotated,
                    1.0,
                    overlay,
                    0.3,
                    0
                )

        return annotated