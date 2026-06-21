class ExplanationAgent:
    def explain(self, driving_state):

        

        risk = driving_state["collision_risk"]

        decision = driving_state["decision"]

        lane_objects = driving_state["lane_objects"]

        

        if len(lane_objects) == 0 and len(driving_state["objects"]) == 0:

            return (
                f"The vehicle decided to {decision}. "
                "No obstacles detected in the driving lane."
            )

        objects = driving_state["objects"]

        critical_objects = [
            obj
            for obj in objects
            if obj["risk"] == "critical"
        ]

        if len(critical_objects) > 0:

            nearest = min(
                critical_objects,
                key=lambda x: x["distance"]
            )

        else:

            nearest = min(
                objects,
                key=lambda x: x["distance"]
            )

        if nearest["ttc"] == 999:
            ttc_text = "not applicable"
        else:
            ttc_text = f"{nearest['ttc']} seconds"

        rule = driving_state.get("knowledge_rule")

        if rule:

            return (
                f"The vehicle decided to {decision}. "
                f"A {nearest['class']} was detected "
                f"{nearest['distance']} meters ahead. "
                f"TTC is {ttc_text}. "
                f"Overall risk level is {risk}. "
                f"Retrieved rule: {rule['reason']}. "
                f"Recommended action: {rule['action']}."
            )

        return (
            f"The vehicle decided to {decision}. "
            f"A {nearest['class']} was detected "
            f"{nearest['distance']} meters ahead. "
            f"TTC is {ttc_text}. "
            f"Overall risk level is {risk}."
        )