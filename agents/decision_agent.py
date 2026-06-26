class DecisionAgent:

    def decide(
        self,
        risk_decision,
        graph_decision,
        rule_decision,
        sign_decision,
        lane_change_decision
    ):

        decisions = [
            risk_decision,
            graph_decision,
            rule_decision,
            sign_decision,
            lane_change_decision
        ]

        # 1. Emergency collision avoidance
        if "BRAKE" in decisions:

            return {
                "decision": "BRAKE",
                "reason": "Emergency collision risk detected."
            }

        if "CHANGE_LEFT" in decisions:

            return {
                "decision": "CHANGE_LEFT",
                "reason": "Safe left lane available."
            }

        if "CHANGE_RIGHT" in decisions:

            return {
                "decision": "CHANGE_RIGHT",
                "reason": "Safe right lane available."
            }

        # 2. Traffic signals/signs
        if "STOP" in decisions:

            return {
                "decision": "STOP",
                "reason": "Traffic signal requires stopping."
            }

        # 3. High-risk situations
        if "SLOW_DOWN" in decisions:

            return {
                "decision": "SLOW_DOWN",
                "reason": "Potential hazard detected."
            }

        # 4. Advisory warnings
        if "CAUTION" in decisions:

            return {
                "decision": "CAUTION",
                "reason": "Proceed carefully."
            }

        return {
            "decision": "MAINTAIN_SPEED",
            "reason": "Road conditions appear safe."
        }