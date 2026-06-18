class EmergencyBrakeAgent:

    def should_brake(self, driving_state):

        if driving_state["collision_risk"] == "critical":
            return True

        return False