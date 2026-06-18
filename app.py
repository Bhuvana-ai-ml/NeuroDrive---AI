import cv2

from perception.object_detection import ObjectDetector
from perception.driving_state import DrivingState
from perception.distance_estimation import DistanceEstimator
from perception.road_segmenter import RoadSegmenter
from tracking.object_tracker import ObjectTracker
from agents.risk_agent import RiskAssessmentAgent
from agents.explanation_agent import ExplanationAgent
from agents.perception_agent import PerceptionAgent
from agents.traffic_rule_agent import TrafficRuleAgent 
from agents.lane_occupancy_agent import LaneOccupancyAgent
from risk.ttc import TTCEngine

detector = ObjectDetector()

segmenter = RoadSegmenter()

ttc_engine = TTCEngine()

distance_estimator = DistanceEstimator()

tracker = ObjectTracker()

risk_agent = RiskAssessmentAgent()

explanation_agent = ExplanationAgent()

perception_agent = PerceptionAgent()

traffic_rule_agent = TrafficRuleAgent()

lane_agent = LaneOccupancyAgent()

cap = cv2.VideoCapture(r"C:\Users\Bhuvana P\OneDrive\Desktop\NeuroDrive-AI\data\videos\road.mp4")

frame_count = 0

while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    detections = detector.detect(frame)

    road_info = segmenter.segment(frame)


    state = DrivingState()

    state.road_detected = road_info["road_detected"]

    state.lane_detected = road_info["lane_detected"]

    enhanced_detections = []

    for detection in detections:

        track_id = detection["id"]

        object_type = detection["class"]

        bbox = detection["bbox"]

        x1, y1, x2, y2 = bbox

        center_x = (x1+x2)//2
        center_y = (y1+y2)//2

        speed = tracker.update(
            track_id,
            center_x,
            center_y
        )

        distance = distance_estimator.estimate(
            object_type,
            bbox
        )

        # Better TTC calculation
        if speed < 1:

            ttc = 999

            risk = "safe"

        else:

            ttc = ttc_engine.calculate_ttc(
                distance,
                speed
            )

            risk = ttc_engine.risk_level(ttc)

        detection["distance"] = distance
        detection["ttc"] = ttc
        detection["risk"] = risk
        detection["speed"] = speed

        enhanced_detections.append(
            detection
        )
        track_id = detection["id"]


        

        if ttc == 999:
            ttc_text = "N/A"
        else:
            ttc_text = f"{ttc}s"

        label = (
            f"{object_type} "
            f"{distance}m "
            f"TTC:{ttc_text} "
            f"{risk}"
        )

        cv2.rectangle(
            frame,
            (x1,y1),
            (x2,y2),
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            label,
            (x1,y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,0),
            2
        )

        

    

    state.objects = enhanced_detections

    lane_objects = lane_agent.evaluate(
        enhanced_detections,
        frame.shape[1]
    )

    state.lane_objects = lane_objects

    state.road_detected = road_info["road_detected"]

    state.lane_detected = road_info["lane_detected"]

    # ----------------------------
    # Overall Collision Risk
    # ----------------------------

    risks = [obj["risk"] for obj in lane_objects]

    if "critical" in risks:
        state.collision_risk = "critical"

    elif "danger" in risks:
        state.collision_risk = "danger"

    elif "warning" in risks:
        state.collision_risk = "warning"

    else:
        state.collision_risk = "safe"

    
    risk_result = risk_agent.assess(
        state.to_dict()
    )

    rule_result = traffic_rule_agent.evaluate(
        state.to_dict()
    )

    state.rule_triggered = rule_result["rule_triggered"]

    state.rule = rule_result["rule"]

    if rule_result["rule_triggered"]:

        state.decision = rule_result["action"]

        state.priority = "HIGH"

        state.reason = rule_result["rule"]

    else:

        state.decision = risk_result["decision"]

        state.priority = risk_result["priority"]

        state.reason = risk_result["reason"]

    state.decision = risk_result["decision"]

    state.priority = risk_result["priority"]

    state.reason = risk_result["reason"]

    state.explanation = explanation_agent.explain(
        state.to_dict()
    )

    perception_summary = perception_agent.analyze(
        state.to_dict()
    )

    print("\nPERCEPTION SUMMARY")
    print(perception_summary)

    

    


    if frame_count % 30 == 0:

        print("\n========== DRIVING STATE ==========")

        print(state.to_dict())

        print("===================================\n")

    cv2.imshow(
        "NeuroDrive AI",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()