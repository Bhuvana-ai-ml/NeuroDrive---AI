class ReasoningAgent:

    def reason(
        self,
        graph_context
    ):

        if (
            "car critical" in graph_context
            and
            "car in lane" in graph_context
        ):

            return {
                "decision": "BRAKE",
                "reason":
                "Critical vehicle detected in ego lane."
            }

        return {
            "decision": "MONITOR",
            "reason":
            "No immediate threat."
        }