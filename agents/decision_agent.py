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

        if "BRAKE" in decisions:

            return {
                "decision": "BRAKE",
                "reason": "One or more agents requested braking."
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

        if "MONITOR" in decisions:

            return {
                "decision": "MONITOR",
                "reason": "Continue monitoring the environment."
            }

        return {
            "decision": "MAINTAIN_SPEED",
            "reason": "All agents agree road is safe."
        }