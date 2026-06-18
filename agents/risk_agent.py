class RiskAssessmentAgent:

    def assess(self, driving_state):

        risk = driving_state["collision_risk"]

        if risk == "critical":

            return {
                "decision": "BRAKE",
                "priority": "HIGH",
                "reason": "Critical collision risk detected."
            }

        elif risk == "danger":

            return {
                "decision": "SLOW_DOWN",
                "priority": "MEDIUM",
                "reason": "Potential collision risk ahead."
            }

        elif risk == "warning":

            return {
                "decision": "CAUTION",
                "priority": "LOW",
                "reason": "Monitor nearby vehicles."
            }

        return {
            "decision": "MAINTAIN_SPEED",
            "priority": "LOW",
            "reason": "Road conditions appear safe."
        }