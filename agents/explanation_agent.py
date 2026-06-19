class ExplanationAgent:
    def explain(self, driving_state):

        

        risk = driving_state["collision_risk"]

        decision = driving_state["decision"]

        lane_objects = driving_state["lane_objects"]

        

        if len(lane_objects) == 0:

            return (
                f"The vehicle decided to {decision}. "
                "No obstacles detected in the driving lane."
            )

        objects = lane_objects

        nearest = min(
            objects,
            key=lambda x: x["distance"]
        )

        if nearest["ttc"] == 999:
            ttc_text = "not applicable"
        else:
            ttc_text = f"{nearest['ttc']} seconds"

        return (
            f"The vehicle decided to {decision}. "
            f"A {nearest['class']} was detected "
            f"{nearest['distance']} meters ahead. "
            f"TTC is {ttc_text}. "
            f"Overall risk level is {risk}."
        )