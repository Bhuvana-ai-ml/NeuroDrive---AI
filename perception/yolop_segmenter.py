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


    def segment(self, img, pad_h, pad_w, height, width, ratio):

        det_out, da_seg_out, ll_seg_out = self.model(img)

        da_predict = da_seg_out[
            :,
            :,
            pad_h:(height-pad_h),
            pad_w:(width-pad_w)
        ]

        da_seg_mask = torch.nn.functional.interpolate(
            da_predict,
            scale_factor=int(1/ratio),
            mode='bilinear'
        )

        _, da_seg_mask = torch.max(da_seg_mask, 1)

        da_seg_mask = (
            da_seg_mask
            .int()
            .squeeze()
            .cpu()
            .numpy()
        )

        ll_predict = ll_seg_out[
            :,
            :,
            pad_h:(height-pad_h),
            pad_w:(width-pad_w)
        ]

        ll_seg_mask = torch.nn.functional.interpolate(
            ll_predict,
            scale_factor=int(1/ratio),
            mode='bilinear'
        )

        _, ll_seg_mask = torch.max(ll_seg_mask, 1)

        ll_seg_mask = (
            ll_seg_mask
            .int()
            .squeeze()
            .cpu()
            .numpy()
        )

        cv2.imshow(
            "road Mask",
            da_seg_mask.astype("uint8") * 255
        )

        cv2.imshow(
            "lane Mask",
            ll_seg_mask.astype("uint8") * 255
        )

        return {
            "road_mask": da_seg_mask,
            "lane_mask": ll_seg_mask
        }