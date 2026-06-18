class DrivingState:

    def __init__(self):

        self.objects = []

        self.road_detected = False

        self.lane_detected = False

        self.collision_risk = "unknown"
        self.decision = None
        self.priority = None
        self.reason = None
        self.explanation = None

        

    def to_dict(self):

        return {
            "objects": self.objects,
            "road_detected": self.road_detected,
            "lane_detected": self.lane_detected,
            "collision_risk": self.collision_risk,
            "decision": self.decision,
            "priority": self.priority,
            "reason": self.reason,
            "explanation": self.explanation
        }