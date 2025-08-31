from flask import render_template, jsonify, request
from app import app, db
from models import PizzaOutlet, PizzaActivity, GeopoliticalEvent, Correlation
from services.pizza_tracker import get_pizza_data
from services.news_feed import get_latest_news
from datetime import datetime, timedelta
import json

@app.route('/')
def index():
    # Get recent pizza activities
    recent_activities = db.session.query(PizzaActivity, PizzaOutlet)\
        .join(PizzaOutlet)\
        .order_by(PizzaActivity.timestamp.desc())\
        .limit(10).all()
    
    # Get latest geopolitical events
    latest_events = GeopoliticalEvent.query\
        .order_by(GeopoliticalEvent.published_date.desc())\
        .limit(4).all()
    
    # Get featured correlations
    featured_correlations = Correlation.query\
        .filter_by(is_featured=True)\
        .join(GeopoliticalEvent)\
        .order_by(Correlation.created_at.desc())\
        .limit(5).all()
    
    # Get all pizza outlets for map
    pizza_outlets = PizzaOutlet.query.filter_by(is_active=True).all()
    
    return render_template('index.html', 
                         recent_activities=recent_activities,
                         latest_events=latest_events,
                         featured_correlations=featured_correlations,
                         pizza_outlets=pizza_outlets,
                         datetime=datetime)

@app.route('/api/pizza-data')
def api_pizza_data():
    """API endpoint for real-time pizza data updates"""
    try:
        data = get_pizza_data()
        return jsonify(data)
    except Exception as e:
        app.logger.error(f"Error fetching pizza data: {e}")
        return jsonify({"error": "Failed to fetch pizza data"}), 500

@app.route('/api/news-feed')
def api_news_feed():
    """API endpoint for latest news updates"""
    try:
        news = get_latest_news()
        return jsonify(news)
    except Exception as e:
        app.logger.error(f"Error fetching news: {e}")
        return jsonify({"error": "Failed to fetch news"}), 500

@app.route('/api/outlets')
def api_outlets():
    """API endpoint for pizza outlets data"""
    outlets = PizzaOutlet.query.filter_by(is_active=True).all()
    outlets_data = []
    
    for outlet in outlets:
        # Get latest activity
        latest_activity = PizzaActivity.query\
            .filter_by(outlet_id=outlet.id)\
            .order_by(PizzaActivity.timestamp.desc())\
            .first()
        
        outlet_data = {
            'id': outlet.id,
            'name': outlet.name,
            'address': outlet.address,
            'latitude': outlet.latitude,
            'longitude': outlet.longitude,
            'rating': outlet.rating,
            'latest_activity': {
                'busy_level': latest_activity.busy_level if latest_activity else 'unknown',
                'timestamp': latest_activity.timestamp.isoformat() if latest_activity else None,
                'activity_score': latest_activity.activity_score if latest_activity else 0
            }
        }
        outlets_data.append(outlet_data)
    
    return jsonify(outlets_data)
