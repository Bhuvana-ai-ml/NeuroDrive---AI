class DecisionAgent:

    def decide(
        self,
        risk_decision,
        graph_decision,
        rule_decision,
        sign_decision
    ):

        # Highest priority: traffic signs

        if sign_decision == "STOP":

            return {
                "decision": "STOP",
                "reason": "Stop sign detected."
            }

        

        decisions = [
            risk_decision,
            graph_decision,
            rule_decision,
            sign_decision
        ]

        if "STOP" in decisions:

            return {
                "decision": "STOP",
                "reason": "Red traffic light detected."
            }

        if "BRAKE" in decisions:

            return {
                "decision": "BRAKE",
                "reason": "Collision risk detected."
            }

        if "SLOW_DOWN" in decisions:

            return {
                "decision": "SLOW_DOWN",
                "reason": "Potential hazard detected."
            }

        if "CAUTION" in decisions:

            return {
                "decision": "CAUTION",
                "reason": "Knowledge graph recommends caution."
            }

        return {
            "decision": "MAINTAIN_SPEED",
            "reason": "Road conditions safe."
        }