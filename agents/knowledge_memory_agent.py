class KnowledgeMemoryAgent:

    def __init__(self):

        self.last_rule = None

    def update(self, rule):

        if rule is not None:
            self.last_rule = rule

        return self.last_rule