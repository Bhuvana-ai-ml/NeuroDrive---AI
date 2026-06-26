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
        self.rule_triggered = False
        self.rule = None
        self.lane_objects = []
        self.emergency_brake = False
        self.knowledge_rule = None
        self.traffic_signs = []
        self.left_lane_free = True
        self.right_lane_free = True

        

    def to_dict(self):

        return {
            "objects": self.objects,
            "road_detected": self.road_detected,
            "lane_detected": self.lane_detected,
            "collision_risk": self.collision_risk,
            "decision": self.decision,
            "priority": self.priority,
            "reason": self.reason,
            "explanation": self.explanation,
            "rule_triggered": self.rule_triggered,
            "rule": self.rule,
            "lane_objects": self.lane_objects,
            "emergency_brake": self.emergency_brake,
            "knowledge_rule": self.knowledge_rule,
            "traffic_signs": self.traffic_signs,
            "left_lane_free": self.left_lane_free,
            "right_lane_free": self.right_lane_free,
        }