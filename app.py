import cv2

from perception.object_detection import ObjectDetector
from perception.lane_detection import LaneDetector


detector = ObjectDetector()
lane_detector = LaneDetector()

cap = cv2.VideoCapture("data/videos/road.mp4")

while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        break

    detections = detector.detect(frame)
    for d in detections:
        print(d)

    frame = detector.draw_detections(
        frame,
        detections
    )

    lane_lines = lane_detector.detect(frame)

    frame = lane_detector.draw_lanes(
        frame,
        lane_lines
    )

    cv2.imshow("NeuroDrive", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()