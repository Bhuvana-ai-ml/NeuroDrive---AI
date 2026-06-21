class RiskMemoryAgent:

    def __init__(self):

        self.last_risk = "safe"

        self.safe_counter = 0

    def update(self, current_risk):

        if current_risk in ["critical", "danger"]:

            self.last_risk = current_risk

            self.safe_counter = 0

            return current_risk

        self.safe_counter += 1

        if self.safe_counter < 5:

            return self.last_risk

        self.last_risk = "safe"

        return "safe"