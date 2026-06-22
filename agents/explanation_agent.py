class ExplanationAgent:

    def explain(self, driving_state):

        risk = driving_state["collision_risk"]

        decision = driving_state["decision"]

        lane_objects = driving_state["lane_objects"]

        rule = driving_state.get("knowledge_rule")

        # No objects in lane
        if len(lane_objects) == 0:

            if rule:

                return (
                    f"The vehicle decided to {decision}. "
                    f"No obstacles detected in the driving lane. "
                    f"Retrieved rule: {rule['reason']}. "
                    f"Recommended action: {rule['action']}."
                )

            return (
                f"The vehicle decided to {decision}. "
                "No obstacles detected in the driving lane."
            )

        # Focus only on lane objects
        objects = lane_objects

        critical_objects = [
            obj
            for obj in objects
            if obj["risk"] == "critical"
        ]

        danger_objects = [
            obj
            for obj in objects
            if obj["risk"] == "danger"
        ]

        if len(critical_objects) > 0:

            nearest = min(
                critical_objects,
                key=lambda x: x["distance"]
            )

        elif len(danger_objects) > 0:

            nearest = min(
                danger_objects,
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

            ttc_text = (
                f"{nearest['ttc']} seconds"
            )

        explanation = (
            f"The vehicle decided to {decision}. "
            f"A {nearest['class']} was detected "
            f"{nearest['distance']} meters ahead "
            f"in the driving lane. "
            f"TTC is {ttc_text}. "
            f"Overall risk level is {risk}."
        )

        if rule:

            explanation += (
                f" Retrieved rule: "
                f"{rule['reason']}. "
                f"Recommended action: "
                f"{rule['action']}."
            )

        return explanation