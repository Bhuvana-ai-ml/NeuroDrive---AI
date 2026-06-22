class DecisionAgent:

    def decide(
        self,
        risk_decision,
        graph_decision,
        rule_decision
    ):

        decisions = [
            risk_decision,
            graph_decision,
            rule_decision
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

        return {
            "decision": "MAINTAIN_SPEED",
            "reason": "All agents agree road is safe."
        }