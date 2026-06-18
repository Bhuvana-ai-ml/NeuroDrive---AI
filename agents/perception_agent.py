class PerceptionAgent:

    def analyze(self, driving_state):

        objects = driving_state["objects"]

        if len(objects) == 0:

            return {
                "num_objects": 0,
                "nearest_object": None,
                "nearest_distance": None,
                "critical_objects": 0
            }

        nearest = min(
            objects,
            key=lambda x: x["distance"]
        )

        critical_count = sum(
            1
            for obj in objects
            if obj["risk"] == "critical"
        )

        return {
            "num_objects": len(objects),
            "nearest_object": nearest["class"],
            "nearest_distance": nearest["distance"],
            "critical_objects": critical_count
        }