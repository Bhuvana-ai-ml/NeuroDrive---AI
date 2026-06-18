import cv2

from perception.road_segmentation import RoadSegmentation

segmenter = RoadSegmentation()

cap = cv2.VideoCapture("data/videos/road.mp4")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = segmenter.segment(frame)

    frame = segmenter.draw_masks(
        frame,
        results
    )

    cv2.imshow("Road Segmentation", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()