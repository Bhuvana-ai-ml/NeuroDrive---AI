from perception.yolop_segmenter import YOLOPSegmenter


class RoadSegmenter:

    def __init__(self):

        self.yolop = YOLOPSegmenter()

    def segment(self, frame):

        result = self.yolop.segment(frame)

        result["road_detected"] = bool(
            result["road_mask"].sum() > 1000
        )

        result["lane_detected"] = bool(
            result["lane_mask"].sum() > 100
        )

        return result