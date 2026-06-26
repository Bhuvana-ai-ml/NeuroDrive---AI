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
from agents.emergency_brake_agent import EmergencyBrakeAgent
from agents.safety_report_agent import SafetyReportAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.risk_memory_agent import RiskMemoryAgent
from agents.knowledge_memory_agent import KnowledgeMemoryAgent
from agents.graph_rag_agent import GraphRAGAgent
from agents.reasoning_agent import ReasoningAgent
from agents.decision_fusion_agent import (
    DecisionFusionAgent
)
from agents.lane_memory_agent import LaneMemoryAgent
from agents.lane_change_agent import LaneChangeAgent
from agents.decision_agent import DecisionAgent
from agents.traffic_sign_agent import (
    TrafficSignAgent
)
from agents.traffic_rule_graph_agent import (
    TrafficRuleGraphAgent
)
from agents.traffic_light_memory_agent import (
    TrafficLightMemoryAgent
)
from agents.traffic_light_state_agent import (
    TrafficLightStateAgent
)
from agents.traffic_light_relevance_agent import (
    TrafficLightRelevanceAgent
)
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

emergency_brake_agent = EmergencyBrakeAgent()

safety_agent = SafetyReportAgent()

knowledge_agent = KnowledgeAgent()

risk_memory_agent = RiskMemoryAgent()

knowledge_memory_agent = KnowledgeMemoryAgent()

graph_rag_agent = GraphRAGAgent()

reasoning_agent = ReasoningAgent()

fusion_agent = DecisionFusionAgent()

lane_memory_agent = LaneMemoryAgent()

decision_agent = DecisionAgent()

lane_change_agent = LaneChangeAgent()

traffic_sign_agent = (
    TrafficSignAgent()
)

traffic_graph_agent = (
    TrafficRuleGraphAgent()
)

traffic_light_memory_agent = (
    TrafficLightMemoryAgent()
)

traffic_light_state_agent = (
    TrafficLightStateAgent()
)

traffic_light_relevance_agent = (
    TrafficLightRelevanceAgent()
)

cap = cv2.VideoCapture(r"C:\Users\Bhuvana P\OneDrive\Desktop\NeuroDrive-AI\data\videos\road.mp4")

frame_count = 0

while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    detections = detector.detect(frame)

    road_info = segmenter.segment(frame)
    print(road_info.keys())


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

    traffic_signs = (
        traffic_sign_agent.evaluate(
            enhanced_detections
        )
    )

    print("\nTRAFFIC SIGNS")
    print(traffic_signs)

    state.traffic_signs = (
        traffic_signs
    )

    traffic_lights = (
        traffic_light_state_agent.classify(
            frame,
            traffic_signs
        )
    )

    print("\nTRAFFIC LIGHT STATES")

    traffic_lights = (
        traffic_light_relevance_agent
        .filter_relevant(
            traffic_lights,
            frame.shape[1]
        )
    )

    print("\nRELEVANT TRAFFIC LIGHT")

    for light in traffic_lights:

        print(
            light["light_state"],
            light["bbox"]
        )

    for light in traffic_lights:

        print(
            light["light_state"],
            light["confidence"]
        )

    sign_rules = (
        traffic_graph_agent.retrieve(
            traffic_signs
        )
    )


    
    

    relevant_light = None

    if len(traffic_lights) > 0:

        relevant_light = traffic_lights[0]


    if relevant_light:
        sign_rules = (
            traffic_graph_agent.retrieve(
                [relevant_light]
            )
        )
    else:
        sign_rules = []


    print("\nTRAFFIC GRAPH")
    print(sign_rules)


    lane_change_result = lane_change_agent.decide(
        state.to_dict()
    )

    print("\nLANE CHANGE")
    print(lane_change_result)


    sign_decision = None
    if len(sign_rules) > 0:

        sign_decision = (
            sign_rules[0]["action"]
        )
    print(
        "SIGN DECISION:",
        sign_decision
    )



    traffic_lights = [
        obj
        for obj in enhanced_detections
        if obj["class"] == "traffic light"
    ]

    traffic_light_visible = (
        traffic_light_memory_agent.update(
            traffic_lights
        )
    )

    print(
        "Traffic Light Visible:",
        traffic_light_visible
    )



    lane_objects = lane_agent.evaluate(
        enhanced_detections,
        road_info["lane_mask"]
    )


    for obj in enhanced_detections:

        track_id = obj["id"]

        obj["in_lane"] = lane_memory_agent.update(
            track_id,
            obj["in_lane"]
        )

    lane_objects = [
        obj
        for obj in enhanced_detections
        if obj["in_lane"]
    ]

    state.lane_objects = lane_objects

    print("\nLANE MEMORY OUTPUT")

    for obj in lane_objects:

        print(
            obj["id"],
            obj["class"],
            obj["in_lane"]
        )

    print("\nLANE OBJECTS")
    print(lane_objects)

    graph_context = graph_rag_agent.retrieve(
        state.to_dict()
    )

    print("\nGRAPH CONTEXT")
    print(graph_context)


    reasoning_result = (
        reasoning_agent.reason(
            graph_context
        )
    )

    print("\nREASONING")
    print(reasoning_result)

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

    


    if state.collision_risk == "critical":

        rule_name = "critical_collision"

    elif state.collision_risk == "danger":

        rule_name = "danger_collision"

    elif state.collision_risk == "warning":

        rule_name = "warning_collision"

    else:

        rule_name = None


    rule = None

    if rule_name:

        rule = knowledge_agent.retrieve(
            rule_name
        )

        related = knowledge_agent.retrieve_related(
            rule_name
        )

        print("\nMAIN RULE")
        print(rule)

        print("\nRELATED RULES")
        print(related)

    state.knowledge_rule = (
        knowledge_memory_agent.update(rule)
    )
        
    print("\nSAVED KNOWLEDGE RULE")
    print(state.knowledge_rule)


    state.collision_risk = risk_memory_agent.update(
        state.collision_risk
    )

    print("Current Risk:", state.collision_risk)

    
    risk_result = risk_agent.assess(
        state.to_dict()
    )

    risk_decision = risk_result["decision"]

    graph_decision = (
        reasoning_result["decision"]
    )

    # Default value
    rule_decision = "MAINTAIN_SPEED"

    if state.knowledge_rule:

        action = state.knowledge_rule["action"]

        if action == "BRAKE":

            rule_decision = "BRAKE"

        elif action == "SLOW_DOWN":

            rule_decision = "SLOW_DOWN"

        elif action == "CAUTION":

            rule_decision = "CAUTION"


    sign_decision = None

    if len(traffic_lights) > 0:

        state_name = (
            traffic_lights[0]["light_state"]
        )

        if state_name == "RED":

            sign_decision = "STOP"

        elif state_name == "YELLOW":

            sign_decision = "SLOW_DOWN"

        elif state_name == "GREEN":

            sign_decision = "MAINTAIN_SPEED"



    if len(sign_rules) > 0:

        sign_decision = (
            sign_rules[0]["action"]
        )


    fusion_result = decision_agent.decide(
        risk_decision,
        graph_decision,
        rule_decision, 
        sign_decision
    )

    state.decision = (
        fusion_result["decision"]
    )

    state.reason = (
        fusion_result["reason"]
)

    print("\nFUSION RESULT")
    print(fusion_result["decision"])




    risks = [obj["risk"] for obj in lane_objects]

    
    rule_result = traffic_rule_agent.evaluate(
        state.to_dict()
    )

    state.rule_triggered = rule_result["rule_triggered"]

    state.rule = rule_result["rule"]



    state.decision = fusion_result["decision"]

    state.reason = fusion_result["reason"]



    if state.emergency_brake:

        state.priority = "HIGH"

    elif state.collision_risk == "critical":

        state.priority = "HIGH"

    elif state.collision_risk == "danger":

        state.priority = "MEDIUM"

    elif state.decision in ["STOP", "SLOW_DOWN"]:

        state.priority = "MEDIUM"

    else:

        state.priority = "LOW"



    print("\nBEFORE EXPLANATION")
    print(state.knowledge_rule)

    state.explanation = explanation_agent.explain(
        state.to_dict()
    )

    perception_summary = perception_agent.analyze(
        state.to_dict()
    )

    

    print("\nPERCEPTION SUMMARY")
    print(perception_summary)

    state.emergency_brake = (
        emergency_brake_agent.should_brake(
            state.to_dict()
        )
    )

    
    if frame_count % 30 == 0:

        print("\n========== DRIVING STATE ==========")

        print(state.to_dict())
        print("Knowledge Rule:", state.knowledge_rule)

        print("===================================\n")

        report = safety_agent.generate(
            state.to_dict()
        )

        print("\n===== SAFETY REPORT =====")
        print(report)
        print("=========================\n")

    cv2.imshow(
        "NeuroDrive AI",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()