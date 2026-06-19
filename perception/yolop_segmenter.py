import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

YOLOP_DIR = os.path.join(
    BASE_DIR,
    "yolop"
)

sys.path.append(YOLOP_DIR)

import cv2
import torch
import numpy as np
import torchvision.transforms as transforms

from lib.config import cfg
from lib.models import get_net


normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)

transform = transforms.Compose([
    transforms.ToTensor(),
    normalize,
])


class YOLOPSegmenter:

    def __init__(
        self,
        weights_path="yolop/weights/End-to-end.pth",
        device="cpu"
    ):

        self.device = torch.device(device)

        self.model = get_net(cfg)

        checkpoint = torch.load(
            weights_path,
            map_location=self.device
        )

        self.model.load_state_dict(
            checkpoint["state_dict"]
        )

        self.model = self.model.to(self.device)

        self.model.eval()

    def segment(self, frame):

        original_h, original_w = frame.shape[:2]

        frame_resized = cv2.resize(
            frame,
            (640, 640)
        )

        img = transform(frame_resized)

        img = img.unsqueeze(0)

        img = img.to(self.device)

        with torch.no_grad():

            _, da_seg_out, ll_seg_out = self.model(img)

        _, road_mask = torch.max(
            da_seg_out,
            1
        )

        _, lane_mask = torch.max(
            ll_seg_out,
            1
        )

        road_mask = (
            road_mask
            .squeeze()
            .cpu()
            .numpy()
            .astype(np.uint8)
        )

        lane_mask = (
            lane_mask
            .squeeze()
            .cpu()
            .numpy()
            .astype(np.uint8)
        )

        road_mask = cv2.resize(
            road_mask,
            (original_w, original_h),
            interpolation=cv2.INTER_NEAREST
        )

        lane_mask = cv2.resize(
            lane_mask,
            (original_w, original_h),
            interpolation=cv2.INTER_NEAREST
        )

        return {
            "road_detected": True,
            "lane_detected": True,
            "road_mask": road_mask,
            "lane_mask": lane_mask
        }