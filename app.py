import cv2

from perception.object_detection import ObjectDetector
from perception.driving_state import DrivingState
from perception.distance_estimation import DistanceEstimator
from perception.road_segmenter import RoadSegmenter
from tracking.object_tracker import ObjectTracker
from risk.ttc import TTCEngine

detector = ObjectDetector()

segmenter = RoadSegmenter()

ttc_engine = TTCEngine()

distance_estimator = DistanceEstimator()


tracker = ObjectTracker()

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

        relative_speed = max(speed, 1)

        ttc = ttc_engine.calculate_ttc(
            distance,
            relative_speed
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


        

        label = (
        f"{object_type} "
        f"{distance}m "
        f"TTC:{ttc}s "
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

    state.road_detected = road_info["road_detected"]

    state.lane_detected = road_info["lane_detected"]

    # ----------------------------
    # Overall Collision Risk
    # ----------------------------

    risks = [obj["risk"] for obj in enhanced_detections]

    if "critical" in risks:
        state.collision_risk = "critical"

    elif "danger" in risks:
        state.collision_risk = "danger"

    elif "warning" in risks:
        state.collision_risk = "warning"

    else:
        state.collision_risk = "safe"


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