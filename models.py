from app import db
from datetime import datetime
from sqlalchemy import Text, Float, Integer, String, DateTime, Boolean

class PizzaOutlet(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(200), nullable=False)
    address = db.Column(String(500), nullable=False)
    latitude = db.Column(Float, nullable=False)
    longitude = db.Column(Float, nullable=False)
    place_id = db.Column(String(200), unique=True, nullable=False)
    phone = db.Column(String(50))
    rating = db.Column(Float)
    price_level = db.Column(Integer)
    is_active = db.Column(Boolean, default=True)
    created_at = db.Column(DateTime, default=datetime.utcnow)

class PizzaActivity(db.Model):
    id = db.Column(Integer, primary_key=True)
    outlet_id = db.Column(Integer, db.ForeignKey('pizza_outlet.id'), nullable=False)
    timestamp = db.Column(DateTime, default=datetime.utcnow)
    busy_level = db.Column(String(50))  # 'not busy', 'less busy', 'a bit busier', 'busier than usual'
    activity_score = db.Column(Float)  # Normalized activity score 0-100
    raw_data = db.Column(Text)  # JSON string of raw API response
    
    outlet = db.relationship('PizzaOutlet', backref=db.backref('activities', lazy=True))

class GeopoliticalEvent(db.Model):
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(500), nullable=False)
    description = db.Column(Text)
    source = db.Column(String(100), nullable=False)
    url = db.Column(String(1000))
    published_date = db.Column(DateTime, nullable=False)
    significance_score = db.Column(Float)  # 0-100 relevance to military/pentagon activity
    event_type = db.Column(String(100))  # 'military', 'diplomatic', 'conflict', etc.
    created_at = db.Column(DateTime, default=datetime.utcnow)

class Correlation(db.Model):
    id = db.Column(Integer, primary_key=True)
    event_id = db.Column(Integer, db.ForeignKey('geopolitical_event.id'), nullable=False)
    date = db.Column(DateTime, nullable=False)
    pizza_spike_percentage = db.Column(Float)
    description = db.Column(Text)
    is_featured = db.Column(Boolean, default=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    event = db.relationship('GeopoliticalEvent', backref=db.backref('correlations', lazy=True))
