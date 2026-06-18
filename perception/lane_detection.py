import cv2
import numpy as np


class LaneDetector:

    def __init__(self):
        pass

    def region_of_interest(self, image):

        height = image.shape[0]
        width = image.shape[1]

        polygon = np.array([
            [
                (100, height),
                (width - 100, height),
                (width//2 + 250, int(height*0.6)),
                (width//2 - 250, int(height*0.6))
            ]
        ], np.int32)

        mask = np.zeros_like(image)

        cv2.fillPoly(mask, polygon, 255)

        return cv2.bitwise_and(image, mask)

    def detect(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(
            blur,
            75,
            200
        )

        roi = self.region_of_interest(edges)

        lines = cv2.HoughLinesP(
            roi,
            rho=2,
            theta=np.pi / 180,
            threshold=50,
            minLineLength=80,
            maxLineGap=50
        )

        return lines

    def draw_lanes(self, frame, lines):

        if lines is None:
            return frame

        for line in lines:

            x1, y1, x2, y2 = line[0]

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                4
            )

        return frame