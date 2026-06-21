class DecisionFusionAgent:

    def decide(
        self,
        risk_decision,
        graph_decision,
        rule_decision
    ):

        votes = [
            risk_decision,
            graph_decision,
            rule_decision
        ]

        if "BRAKE" in votes:
            return "BRAKE"

        if "SLOW_DOWN" in votes:
            return "SLOW_DOWN"

        if "CAUTION" in votes:
            return "CAUTION"

        return "MAINTAIN_SPEED"