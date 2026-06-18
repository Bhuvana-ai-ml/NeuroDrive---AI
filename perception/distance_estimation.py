class DistanceEstimator:

    def __init__(self):

        self.known_widths = {
            "car": 1.8,
            "truck": 2.5,
            "bus": 2.7,
            "person": 0.5,
            "motorcycle": 0.8,
            "bicycle": 0.6
        }

        self.focal_length = 700

    def estimate(self, object_type, bbox):

        x1, y1, x2, y2 = bbox

        pixel_width = x2 - x1

        if pixel_width <= 0:
            return None

        known_width = self.known_widths.get(
            object_type,
            1.0
        )

        distance = (
            known_width * self.focal_length
        ) / pixel_width

        return round(distance, 2)