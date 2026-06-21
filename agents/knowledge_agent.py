import json


class KnowledgeAgent:

    def __init__(self):

        with open(
            "knowledge/traffic_rules.json",
            "r"
        ) as f:

            self.rules = json.load(f)

    def retrieve(self, rule_name):

        return self.rules.get(rule_name)

    def retrieve_related(self, rule_name):

        rule = self.rules.get(rule_name)

        if not rule:
            return []

        related = []

        for item in rule.get(
            "related_rules",
            []
        ):

            related.append(
                self.rules.get(item)
            )

        return related