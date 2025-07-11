import os
import json
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)

RAW_DATA_PATH = "data/raw/telegram_messages"

def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
    )
    conn.autocommit = True
    return conn

def create_raw_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS raw;
            CREATE TABLE IF NOT EXISTS raw.telegram_messages (
                id SERIAL PRIMARY KEY,
                channel_name TEXT,
                message_date TIMESTAMP,
                raw_data JSONB
            );
        """)

def load_json_to_db(conn):
    with conn.cursor() as cur:
        for root, _, files in os.walk(RAW_DATA_PATH):
            for file in files:
                if file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    with open(full_path, 'r', encoding='utf-8') as f:
                        messages = json.load(f)
                        for msg in messages:
                            # Extract message_date and channel_name from your JSON structure accordingly
                            msg_date = msg.get("date")
                            channel_name = msg.get("channel") or os.path.basename(root)
                            cur.execute("""
                                INSERT INTO raw.telegram_messages (channel_name, message_date, raw_data)
                                VALUES (%s, %s, %s);
                            """, (channel_name, msg_date, Json(msg)))

if __name__ == "__main__":
    conn = connect_db()
    create_raw_table(conn)
    load_json_to_db(conn)
    conn.close()
