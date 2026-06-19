import cv2
from perception.yolop_segmenter import YOLOPSegmenter

segmenter = YOLOPSegmenter()

cap = cv2.VideoCapture(
    r"C:\Users\Bhuvana P\OneDrive\Desktop\NeuroDrive-AI\data\videos\road.mp4"
)

ret, frame = cap.read()

print("Frame Shape:", frame.shape)
result = segmenter.segment(frame)

print(result.keys())

cap.release()