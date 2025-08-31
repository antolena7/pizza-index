import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from services.pizza_tracker import get_pizza_data
from services.news_feed import fetch_fresh_news

logger = logging.getLogger(__name__)

scheduler = None

def init_scheduler():
    """Initialize background scheduler for data collection"""
    global scheduler
    
    if scheduler is not None:
        return
    
    scheduler = BackgroundScheduler()
    
    # Schedule pizza data collection every 15 minutes
    scheduler.add_job(
        func=collect_pizza_data,
        trigger=IntervalTrigger(minutes=15),
        id='pizza_data_collection',
        name='Collect pizza activity data',
        replace_existing=True
    )
    
    # Schedule news data collection every 30 minutes
    scheduler.add_job(
        func=collect_news_data,
        trigger=IntervalTrigger(minutes=30),
        id='news_data_collection',
        name='Collect news data',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Background scheduler initialized")

def collect_pizza_data():
    """Background job to collect pizza data"""
    try:
        logger.info("Starting pizza data collection")
        data = get_pizza_data()
        logger.info(f"Collected data for {len(data)} pizza outlets")
    except Exception as e:
        logger.error(f"Error in pizza data collection: {e}")

def collect_news_data():
    """Background job to collect news data"""
    try:
        logger.info("Starting news data collection")
        news = fetch_fresh_news()
        logger.info(f"Collected {len(news) if news else 0} news articles")
    except Exception as e:
        logger.error(f"Error in news data collection: {e}")
