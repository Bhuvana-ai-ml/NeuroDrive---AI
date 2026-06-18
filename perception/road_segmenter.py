from ultralytics import YOLO
import cv2
import numpy as np


class RoadSegmenter:

    def __init__(self):

        self.road_mask = None
        self.lane_mask = None

    def segment(self, frame):

        h, w = frame.shape[:2]

        road_mask = np.zeros((h, w), dtype=np.uint8)
        lane_mask = np.zeros((h, w), dtype=np.uint8)

        return {
            "road_detected": True,
            "lane_detected": True,
            "road_mask": road_mask,
            "lane_mask": lane_mask
        }