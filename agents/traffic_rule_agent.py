from knowledge_graph.traffic_rules import TRAFFIC_RULES


class TrafficRuleAgent:

    def evaluate(self, driving_state):

        objects = driving_state["objects"]

        for obj in objects:

            obj_class = obj["class"]

            if obj_class in TRAFFIC_RULES:

                rule = TRAFFIC_RULES[obj_class]

                return {
                    "rule_triggered": True,
                    "rule": rule["rule"],
                    "action": rule["action"]
                }

        return {
            "rule_triggered": False,
            "rule": None,
            "action": None
        }