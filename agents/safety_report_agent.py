class SafetyReportAgent:

    def generate(self, driving_state):

        objects = driving_state["objects"]

        safe = 0
        warning = 0
        danger = 0
        critical = 0

        for obj in objects:

            risk = obj["risk"]

            if risk == "safe":
                safe += 1

            elif risk == "warning":
                warning += 1

            elif risk == "danger":
                danger += 1

            elif risk == "critical":
                critical += 1

        return {

            "vehicles_detected":
            len(objects),

            "safe_objects":
            safe,

            "warning_objects":
            warning,

            "danger_objects":
            danger,

            "critical_objects":
            critical,

            "final_decision":
            driving_state["decision"]
        }