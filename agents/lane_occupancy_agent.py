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

            # Larger region around vehicle bottom
            x_start = max(center_x - 40, 0)
            x_end = min(center_x + 40, mask_w)

            y_start = max(bottom_y - 20, 0)
            y_end = min(bottom_y + 20, mask_h)

            region = lane_mask[
                y_start:y_end,
                x_start:x_end
            ]

            if region.size == 0:

                obj["in_lane"] = False

                continue

            lane_pixels = (
                region > 0
            ).sum()

            print(
                "Lane Pixels:",
                lane_pixels,
                obj["class"]
            )

            if lane_pixels > 5:

                obj["in_lane"] = True

                lane_objects.append(obj)

            else:

                obj["in_lane"] = False

        return lane_objects