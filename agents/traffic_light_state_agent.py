import cv2
import numpy as np


class TrafficLightStateAgent:

    def classify(self, frame, traffic_lights):

        results = []

        for light in traffic_lights:

            x1, y1, x2, y2 = light["bbox"]

            roi = frame[y1:y2, x1:x2]

            if roi.size == 0:
                continue

            hsv = cv2.cvtColor(
                roi,
                cv2.COLOR_BGR2HSV
            )

            red1 = cv2.inRange(
                hsv,
                (0, 70, 50),
                (10, 255, 255)
            )

            red2 = cv2.inRange(
                hsv,
                (170, 70, 50),
                (180, 255, 255)
            )

            red = red1 + red2

            green = cv2.inRange(
                hsv,
                (40, 50, 50),
                (90, 255, 255)
            )

            yellow = cv2.inRange(
                hsv,
                (15, 80, 80),
                (35, 255, 255)
            )

            red_pixels = cv2.countNonZero(red)
            green_pixels = cv2.countNonZero(green)
            yellow_pixels = cv2.countNonZero(yellow)

            state = "UNKNOWN"

            if red_pixels > green_pixels and red_pixels > yellow_pixels:
                state = "RED"

            elif green_pixels > red_pixels and green_pixels > yellow_pixels:
                state = "GREEN"

            elif yellow_pixels > red_pixels and yellow_pixels > green_pixels:
                state = "YELLOW"

            light["light_state"] = state

            results.append(light)

        return results