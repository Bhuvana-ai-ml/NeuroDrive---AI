class TrafficLightRelevanceAgent:

    def filter_relevant(
        self,
        traffic_lights,
        frame_width
    ):

        if len(traffic_lights) == 0:
            return []

        frame_center = frame_width // 2

        best_light = None

        min_distance = float("inf")

        for light in traffic_lights:

            x1, y1, x2, y2 = light["bbox"]

            center_x = (x1 + x2) // 2

            distance = abs(
                center_x - frame_center
            )

            if distance < min_distance:

                min_distance = distance

                best_light = light

        return [best_light]