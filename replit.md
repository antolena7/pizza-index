# Pizza Index Tracker

## Overview

The Pizza Index Tracker is an OSINT (Open Source Intelligence) web application that monitors pizza delivery activity near the Pentagon and correlates it with geopolitical events. The concept is based on the theory that increased late-night food orders at government facilities may indicate heightened activity during significant events. The application tracks real-time pizza outlet activity, collects geopolitical news, and identifies correlations between food delivery spikes and major world events.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web application with SQLAlchemy ORM for database operations
- **Database**: SQLite for development (configurable via DATABASE_URL environment variable)
- **Models**: Four main entities - PizzaOutlet, PizzaActivity, GeopoliticalEvent, and Correlation
- **Background Processing**: APScheduler for automated data collection every 15-30 minutes
- **API Integration**: Google Places API for pizza outlet data, News API and NYT API for geopolitical events

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive UI
- **Mapping**: Leaflet.js for interactive map visualization of pizza outlets around Pentagon
- **Styling**: Dark OSINT-themed CSS with custom styling for surveillance aesthetic
- **Real-time Updates**: JavaScript-based auto-refresh for live pizza activity data

### Data Collection Services
- **Pizza Tracker**: Monitors activity levels at pizza outlets using Google Places API
- **News Feed**: Aggregates geopolitical news from multiple sources with relevance scoring
- **Scheduler**: Background job system for automated data collection and correlation analysis

### Database Schema
- **PizzaOutlet**: Stores pizza restaurant locations, contact info, and ratings
- **PizzaActivity**: Time-series data of busy levels and activity scores for each outlet
- **GeopoliticalEvent**: News articles with significance scoring and categorization
- **Correlation**: Links pizza activity spikes to specific geopolitical events

## External Dependencies

### APIs and Services
- **Google Places API**: For pizza outlet discovery and real-time activity data
- **News API**: Primary source for current geopolitical news articles
- **New York Times API**: Secondary news source for high-quality journalism
- **OpenStreetMap**: Map tiles for the surveillance map interface

### Frontend Libraries
- **Bootstrap 5**: Responsive CSS framework for UI components
- **Leaflet.js**: Interactive mapping library for geographic visualization
- **Font Awesome**: Icon library for enhanced visual elements

### Python Packages
- **Flask**: Core web framework with SQLAlchemy extension
- **APScheduler**: Background job scheduling for automated data collection
- **Requests**: HTTP client for external API communications
- **Werkzeug**: WSGI utilities including proxy fix for deployment

### Development Tools
- **SQLite**: Default database for development and testing
- **Environment Variables**: Configuration management for API keys and database URLs
- **Logging**: Built-in Python logging for debugging and monitoring