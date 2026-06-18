class LaneOccupancyAgent:

    def evaluate(
        self,
        detections,
        frame_width
    ):

        lane_objects = []

        center_min = int(frame_width * 0.35)
        center_max = int(frame_width * 0.65)

        for obj in detections:

            x1, y1, x2, y2 = obj["bbox"]

            object_center = (x1 + x2) // 2

            if center_min <= object_center <= center_max:

                obj["in_lane"] = True
                lane_objects.append(obj)

            else:

                obj["in_lane"] = False

        return lane_objects