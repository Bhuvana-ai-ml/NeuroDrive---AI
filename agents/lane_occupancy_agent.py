class LaneOccupancyAgent:

    def evaluate(
        self,
        detections,
        lane_mask
    ):

        lane_objects = []

        mask_h, mask_w = lane_mask.shape

        for obj in detections:

            x1, y1, x2, y2 = obj["bbox"]

            center_x = (x1 + x2) // 2

            bottom_y = y2

            center_x = min(
                max(center_x, 0),
                mask_w - 1
            )

            bottom_y = min(
                max(bottom_y, 0),
                mask_h - 1
            )

            if lane_mask[bottom_y, center_x] > 0:

                obj["in_lane"] = True

                lane_objects.append(obj)

            else:

                obj["in_lane"] = False

        return lane_objects