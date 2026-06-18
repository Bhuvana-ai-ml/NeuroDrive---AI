from ultralytics import YOLO
import cv2
import numpy as np




class RoadSegmenter:

    def __init__(self):

        self.road_mask = None
        self.lane_mask = None

    def segment(self, frame):

        """
        Placeholder

        Later this function will call
        YOLOP inference directly.
        """

        return {
            "road_detected": True,
            "lane_detected": True
        }