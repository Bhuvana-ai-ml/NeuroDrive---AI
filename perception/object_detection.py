from ultralytics import YOLO
import cv2


class ObjectDetector:
    def __init__(self, model_path="yolov8s.pt"):
        self.model = YOLO(model_path)

        self.target_classes = {
            "car",
            "truck",
            "bus",
            "motorcycle",
            "bicycle",
            "person",
            "traffic light"
        }

    def detect(self, frame):

        results = self.model.track(
            frame,
            persist=True,
            conf=0.25
        )
        detections = []

        for result in results:

            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                class_name = self.model.names[class_id]

                if class_name not in self.target_classes:
                    continue

                if box.id is None:
                    continue

                track_id = int(box.id.item())

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({
                    "id": track_id,
                    "class": class_name,
                    "confidence": round(confidence, 2),
                    "bbox": [x1, y1, x2, y2]
                })
        print("\nYOLO DETECTIONS")
        for det in detections:

            print(
                det["class"],
                det["confidence"]
            )


        return detections

    def draw_detections(self, frame, detections):

        for detection in detections:

            x1, y1, x2, y2 = detection["bbox"]

            label = (
                f"ID:{detection['id']} "
                f"{detection['class']} "
                f"{detection['confidence']:.2f}"
            )
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        return frame