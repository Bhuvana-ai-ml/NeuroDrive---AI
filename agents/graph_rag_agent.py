class GraphRAGAgent:

    def retrieve(self, driving_state):

        facts = []

        objects = driving_state["lane_objects"]

        for obj in objects:

            if obj["risk"] == "critical":

                facts.append(
                    f"{obj['class']} critical"
                )

            elif obj["risk"] == "danger":

                facts.append(
                    f"{obj['class']} danger"
                )

            facts.append(
                f"{obj['class']} in lane"
            )

        return list(dict.fromkeys(facts))