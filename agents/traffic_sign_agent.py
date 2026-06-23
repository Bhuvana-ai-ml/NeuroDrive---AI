class TrafficSignAgent:

    def evaluate(self, detections):

        signs = []

        for obj in detections:

            cls = obj["class"]

            if cls in [
                "stop sign",
                "traffic light"
            ]:

                signs.append(obj)

        return signs