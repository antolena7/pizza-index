import os
import requests
import logging
from datetime import datetime, timedelta
from app import db
from models import GeopoliticalEvent

logger = logging.getLogger(__name__)

NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'demo_key')
NYT_API_KEY = os.getenv('NYT_API_KEY', 'demo_key')

def get_latest_news():
    """Fetch latest geopolitical news"""
    try:
        # Try to get fresh news from APIs
        fresh_news = fetch_fresh_news()
        if fresh_news:
            return fresh_news
            
        # Fallback to database
        events = GeopoliticalEvent.query\
            .order_by(GeopoliticalEvent.published_date.desc())\
            .limit(4).all()
        
        return [format_event_for_frontend(event) for event in events]
        
    except Exception as e:
        logger.error(f"Error getting latest news: {e}")
        return get_fallback_news()

def fetch_fresh_news():
    """Fetch fresh news from multiple sources"""
    all_news = []
    
    # Fetch from News API
    news_api_articles = fetch_from_news_api()
    all_news.extend(news_api_articles)
    
    # Fetch from NYT API
    nyt_articles = fetch_from_nyt_api()
    all_news.extend(nyt_articles)
    
    # Store new articles in database
    for article in all_news:
        existing = GeopoliticalEvent.query.filter_by(url=article['url']).first()
        if not existing:
            event = GeopoliticalEvent(
                title=article['title'],
                description=article['description'],
                source=article['source'],
                url=article['url'],
                published_date=article['published_date'],
                significance_score=article['significance_score'],
                event_type=article['event_type']
            )
            db.session.add(event)
    
    db.session.commit()
    return all_news[:4]  # Return top 4

def fetch_from_news_api():
    """Fetch from News API"""
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': 'military OR pentagon OR ukraine OR israel OR iran OR russia OR war OR conflict',
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': 10,
            'apiKey': NEWS_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = []
            
            for article in data.get('articles', []):
                if article.get('title') and article.get('url'):
                    articles.append({
                        'title': article['title'].encode('utf-8', 'replace').decode('utf-8'),
                        'description': article.get('description', '').encode('utf-8', 'replace').decode('utf-8') if article.get('description') else '',
                        'source': 'News API',
                        'url': article['url'],
                        'published_date': datetime.fromisoformat(
                            article['publishedAt'].replace('Z', '+00:00')
                        ),
                        'significance_score': calculate_significance(article['title']),
                        'event_type': categorize_event(article['title'])
                    })
            
            return articles
            
    except Exception as e:
        logger.error(f"Error fetching from News API: {e}")
        return []

def fetch_from_nyt_api():
    """Fetch from New York Times API"""
    try:
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
        params = {
            'q': 'military OR pentagon OR ukraine OR israel OR iran OR russia',
            'sort': 'newest',
            'api-key': NYT_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = []
            
            for doc in data.get('response', {}).get('docs', []):
                if doc.get('headline', {}).get('main'):
                    articles.append({
                        'title': doc['headline']['main'].encode('utf-8', 'replace').decode('utf-8'),
                        'description': doc.get('abstract', '').encode('utf-8', 'replace').decode('utf-8') if doc.get('abstract') else '',
                        'source': 'NY Times',
                        'url': doc['web_url'],
                        'published_date': datetime.fromisoformat(
                            doc['pub_date'].replace('Z', '+00:00')
                        ),
                        'significance_score': calculate_significance(doc['headline']['main']),
                        'event_type': categorize_event(doc['headline']['main'])
                    })
            
            return articles
            
    except Exception as e:
        logger.error(f"Error fetching from NYT API: {e}")
        return []

def calculate_significance(title):
    """Calculate significance score based on keywords"""
    high_impact_keywords = ['war', 'attack', 'strike', 'military', 'pentagon', 'nuclear']
    medium_impact_keywords = ['conflict', 'tension', 'sanctions', 'diplomatic']
    
    title_lower = title.lower()
    score = 50  # Base score
    
    for keyword in high_impact_keywords:
        if keyword in title_lower:
            score += 20
    
    for keyword in medium_impact_keywords:
        if keyword in title_lower:
            score += 10
    
    return min(100, score)

def categorize_event(title):
    """Categorize event type based on title"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['war', 'attack', 'strike', 'military']):
        return 'military'
    elif any(word in title_lower for word in ['diplomatic', 'negotiations', 'talks']):
        return 'diplomatic'
    elif any(word in title_lower for word in ['conflict', 'tension', 'crisis']):
        return 'conflict'
    else:
        return 'general'

def format_event_for_frontend(event):
    """Format database event for frontend display"""
    return {
        'title': event.title,
        'description': event.description,
        'source': event.source,
        'url': event.url,
        'published_date': event.published_date.strftime('%m/%d/%Y'),
        'significance_score': event.significance_score,
        'event_type': event.event_type
    }

def get_fallback_news():
    """Fallback news data based on the actual website content"""
    return [
        {
            'title': 'Russia Distracts Its Citizens From Ukraine War With Nonstop Festivals',
            'description': 'This event is significant for global geopolitical stability and may influence regional policies.',
            'source': 'NY Times',
            'url': 'https://www.nytimes.com/2025/08/30/world/europe/russia-ukraine-war-summer-in-moscow.html',
            'published_date': '8/30/2025',
            'significance_score': 75,
            'event_type': 'conflict'
        },
        {
            'title': 'Over 15 Killed in Gaza City, One Day After Israel Ends Daily Pauses for Aid',
            'description': 'Key developments here could affect international relations and military strategies.',
            'source': 'NY Times',
            'url': 'https://www.nytimes.com/2025/08/30/world/middleeast/gaza-israel-deadly-strikes.html',
            'published_date': '8/30/2025',
            'significance_score': 85,
            'event_type': 'military'
        },
        {
            'title': 'Houthis confirm their prime minister killed in Israeli strike',
            'description': 'This event is significant for global geopolitical stability and may influence regional policies.',
            'source': 'BBC',
            'url': 'https://www.bbc.com/news/articles/c620ykrxedwo?at_medium=RSS&at_campaign=rss',
            'published_date': '8/30/2025',
            'significance_score': 90,
            'event_type': 'military'
        },
        {
            'title': 'Prominent Ukrainian politician Andriy Parubiy shot dead in Lviv',
            'description': 'Key developments here could affect international relations and military strategies.',
            'source': 'BBC',
            'url': 'https://www.bbc.com/news/articles/cjw6ep37469o?at_medium=RSS&at_campaign=rss',
            'published_date': '8/30/2025',
            'significance_score': 80,
            'event_type': 'conflict'
        }
    ]
