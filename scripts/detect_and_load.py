import os
import psycopg2
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)

IMAGES_PATH = "data/raw/telegram_messages/images"

def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
    )
    conn.autocommit = True
    return conn

def create_image_detections_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS fct_image_detections (
                detection_id SERIAL PRIMARY KEY,
                message_id INTEGER NOT NULL,
                detected_object_class TEXT NOT NULL,
                confidence_score FLOAT NOT NULL,
                FOREIGN KEY (message_id) REFERENCES fct_messages(message_id)
            );
        """)

def detect_objects_and_save(conn):
    model = YOLO('yolov8n.pt')  # Use nano model for speed; replace with larger for accuracy
    with conn.cursor() as cur:
        for root, _, files in os.walk(IMAGES_PATH):
            for file in files:
                if file.endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(root, file)

                    # Assuming the image filename contains message_id, e.g. message_123.jpg
                    # Extract message_id from filename (adjust logic to your naming)
                    try:
                        message_id = int(file.split('_')[1].split('.')[0])
                    except Exception:
                        print(f"Skipping {file}, cannot extract message_id")
                        continue

                    results = model(image_path)

                    for r in results:
                        for obj in r.boxes.data.tolist():
                            cls_id = int(obj[5])  # class id
                            conf = float(obj[4])

                            # Map class id to name from model.names
                            class_name = model.names[cls_id]

                            cur.execute("""
                                INSERT INTO fct_image_detections (message_id, detected_object_class, confidence_score)
                                VALUES (%s, %s, %s);
                            """, (message_id, class_name, conf))

if __name__ == "__main__":
    conn = connect_db()
    create_image_detections_table(conn)
    detect_objects_and_save(conn)
    conn.close()
