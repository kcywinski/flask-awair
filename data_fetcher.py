import threading
import requests
from datetime import datetime, timedelta

from models import Data, db

class DataFetcher:
    def __init__(self, url, app, retention_period):
        self.url = url
        self.app = app
        self.latest_data = {}
        self.stop_event = threading.Event()
        self.retention_period = retention_period

    def fetch_data(self):
        while not self.stop_event.is_set():
            try:
                response = requests.get(self.url)
                if response.status_code == 200:
                    self.latest_data = response.json()
                    print(f"Fetched data: {self.latest_data}")
                    with self.app.app_context():
                        self.save_data(self.latest_data)
                        self.purge_old_data()
                else:
                    print(f"Failed to fetch data. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error fetching data: {e}")
            self.stop_event.wait(120)  # Fetch data every 60 seconds or stop if event is set

    def save_data(self, data):
        new_data = Data(
            score=data.get('score'),
            temp=data.get('temp'),
            humid=data.get('humid'),
            co2=data.get('co2'),
            voc=data.get('voc'),
            timestamp=datetime.utcnow()
        )
        db.session.add(new_data)
        db.session.commit()
    
    def purge_old_data(self):
        threshold_date = datetime.utcnow() - self.retention_period
        old_data = Data.query.filter(Data.timestamp < threshold_date).delete()
        db.session.commit()
        print(f"Purged {old_data} old records")

    def stop(self):
        self.stop_event.set()