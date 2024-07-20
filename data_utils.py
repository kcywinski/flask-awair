from datetime import datetime, timedelta
from models import db, Data  # Import db and Data from models.py

def save_data(data):
    new_data = Data(
        temp=data.get('temp'),
        humid=data.get('humid'),
        co2=data.get('co2'),
        voc=data.get('voc')
    )
    db.session.add(new_data)
    db.session.commit()
    delete_old_data()

def delete_old_data():
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
    Data.query.filter(Data.timestamp < five_minutes_ago).delete()
    db.session.commit()