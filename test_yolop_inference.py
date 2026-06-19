import cv2
import torch

from perception.yolop_segmenter import YOLOPSegmenter
from perception.yolop_segmenter import transform

segmenter = YOLOPSegmenter()

cap = cv2.VideoCapture(
    r"C:\Users\Bhuvana P\OneDrive\Desktop\NeuroDrive-AI\data\videos\road.mp4"
)

ret, frame = cap.read()

frame_resized = cv2.resize(
    frame,
    (640, 640)
)

img = transform(frame_resized)

img = img.unsqueeze(0)

with torch.no_grad():

    det_out, da_seg_out, ll_seg_out = (
        segmenter.model(img)
    )

print("Road Output Shape:")
print(da_seg_out.shape)

print("Lane Output Shape:")
print(ll_seg_out.shape)

cap.release()