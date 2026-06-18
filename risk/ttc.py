class TTCEngine:

    def __init__(self):

        self.safe_threshold = 5
        self.warning_threshold = 3
        self.critical_threshold = 1

    def calculate_ttc(
        self,
        distance,
        relative_speed
    ):

        if relative_speed <= 0:
            return float("inf")

        return round(
            distance / relative_speed,
            2
        )

    def risk_level(self, ttc):

        if ttc < 1:
            return "critical"

        elif ttc < 3:
            return "danger"

        elif ttc < 5:
            return "warning"

        return "safe"