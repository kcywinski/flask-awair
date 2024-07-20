import signal
import threading
import time
from datetime import datetime, timedelta
from data_fetcher import DataFetcher
from flask import Flask, render_template
from models import db, Data  # Import db and Data from models.py
import yaml

# Load URL from secrets.yaml
with open('secrets.yml', 'r') as file:
    secrets = yaml.safe_load(file)
    api_url = secrets['url']
    retention_period_in_minutes = secrets['retention_period_in_minutes']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Initialize the SQLAlchemy instance with the Flask app
db.init_app(app)
with app.app_context():
    db.create_all()

data_fetcher = DataFetcher(url=api_url, app=app, retention_period=timedelta(minutes=retention_period_in_minutes))

@app.route('/')
def chart():
    return render_template('chart.html')

@app.route('/data')
def get_data():
    data = Data.query.all()
    return {
        "data": [
            {
                "temp": d.temp,
                "humid": d.humid,
                "co2": d.co2,
                "voc": d.voc,
                "score": d.score,
                "timestamp": d.timestamp
            } for d in data
        ]
    }

def handle_signal(signal, frame):
    print("Stopping...")
    data_fetcher.stop()
    fetch_thread.join()
    print("Stopped.")
    exit(0)

if __name__ == '__main__':
    fetch_thread = threading.Thread(target=data_fetcher.fetch_data)
    fetch_thread.daemon = True
    fetch_thread.start()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        app.run(debug=True, host='0.0.0.0')
    except KeyboardInterrupt:
        handle_signal(signal.SIGINT, None)