# app/image_detection/detect_objects.py

import os
import json
from ultralytics import YOLO
import cv2
from datetime import datetime
import uuid

# Directory where images were saved in Task 1
IMAGE_DIR = "data/images"
OUTPUT_DIR = "data/detections"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the pre-trained YOLOv8n model
model = YOLO("yolov8n.pt")

def run_detection():
    results_list = []

    for filename in os.listdir(IMAGE_DIR):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        image_path = os.path.join(IMAGE_DIR, filename)
        print(f"Processing: {image_path}")

        results = model(image_path)

        for r in results:
            for box in r.boxes:
                cls = model.names[int(box.cls)]
                confidence = float(box.conf)

                results_list.append({
                    "message_id": filename.split(".")[0],  # assuming filename is message_id.jpg
                    "detected_object_class": cls,
                    "confidence_score": round(confidence, 4),
                    "detected_at": datetime.now().isoformat()
                })

    # Save detections to JSON
    output_file = os.path.join(OUTPUT_DIR, f"detections_{uuid.uuid4()}.json")
    with open(output_file, "w") as f:
        json.dump(results_list, f, indent=2)

    print(f"\n✅ Detections saved to: {output_file}")

if __name__ == "__main__":
    run_detection()
