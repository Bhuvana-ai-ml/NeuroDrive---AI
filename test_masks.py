import cv2

from perception.yolop_segmenter import YOLOPSegmenter

segmenter = YOLOPSegmenter()

cap = cv2.VideoCapture(
    r"C:\Users\Bhuvana P\OneDrive\Desktop\NeuroDrive-AI\data\videos\road.mp4"
)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    result = segmenter.segment(frame)

    road_mask = (
        result["road_mask"] * 255
    ).astype("uint8")

    lane_mask = (
        result["lane_mask"] * 255
    ).astype("uint8")

    cv2.imshow(
        "Road Mask",
        road_mask
    )

    cv2.imshow(
        "Lane Mask",
        lane_mask
    )

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()