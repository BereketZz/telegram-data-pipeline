from dagster import op
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "app/main.py"], check=True)
