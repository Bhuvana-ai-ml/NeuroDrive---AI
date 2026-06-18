class ExplanationAgent:

    def explain(self, driving_state):

        risk = driving_state["collision_risk"]

        decision = driving_state["decision"]

        objects = driving_state["objects"]

        if len(objects) == 0:

            return (
                "No significant obstacles detected. "
                "Maintaining current speed."
            )

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