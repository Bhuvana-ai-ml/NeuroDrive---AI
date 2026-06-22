class KnowledgeMemoryAgent:

    def __init__(self):

        self.last_rule = None
        self.cooldown = 0

    def update(self, rule):

        if rule is not None:

            self.last_rule = rule
            self.cooldown = 5

            return rule

        if self.cooldown > 0:

            self.cooldown -= 1

            return self.last_rule

        self.last_rule = None

        return None