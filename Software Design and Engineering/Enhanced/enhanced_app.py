#!/usr/bin/env python3
"""
Enhanced Animal Shelter Management System
Advanced Flask application with ML integration, analytics, and monitoring
"""

import os
import logging
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from functools import wraps

from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
try:
    from config import config
    config_name = os.environ.get('FLASK_CONFIG', 'default')
    app_config = config[config_name]
except ImportError:
    # Fallback configuration if config.py doesn't exist
    class FallbackConfig:
        SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
        JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
        JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///animal_shelter_enhanced.db')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        PORT = int(os.environ.get('PORT', 8080))
        HOST = os.environ.get('HOST', '0.0.0.0')
        DEBUG = True
    
    app_config = FallbackConfig()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = app_config.SECRET_KEY
app.config['JWT_SECRET_KEY'] = app_config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = app_config.JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = app_config.JWT_REFRESH_TOKEN_EXPIRES

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = app_config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = app_config.SQLALCHEMY_TRACK_MODIFICATIONS

# Initialize extensions
CORS(app)
jwt = JWTManager(app)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Redis for caching
redis_client = redis.Redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost:6379'))

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

# Database Models
class User(db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }

class Animal(db.Model):
    """Enhanced animal model with additional fields"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    animal_type = db.Column(db.String(50))
    breed = db.Column(db.String(100))
    outcome = db.Column(db.String(50))
    intake_date = db.Column(db.DateTime)
    outcome_date = db.Column(db.DateTime)
    behavior_score = db.Column(db.Float)
    health_score = db.Column(db.Float)
    adoption_probability = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'animal_type': self.animal_type,
            'breed': self.breed,
            'outcome': self.outcome,
            'intake_date': self.intake_date.isoformat() if self.intake_date else None,
            'outcome_date': self.outcome_date.isoformat() if self.outcome_date else None,
            'behavior_score': self.behavior_score,
            'health_score': self.health_score,
            'adoption_probability': self.adoption_probability,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AnalyticsEvent(db.Model):
    """Analytics events for tracking user interactions"""
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)
    event_data = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Machine Learning Models
class AdoptionPredictor:
    """Machine learning model for predicting adoption probability"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train(self, training_data: List[Dict]):
        """Train the adoption prediction model"""
        if not training_data:
            logger.warning("No training data provided")
            return
        
        # Extract features
        features = []
        labels = []
        
        for record in training_data:
            feature_vector = self._extract_features(record)
            features.append(feature_vector)
            labels.append(1 if record.get('outcome') == 'Adoption' else 0)
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        # Train model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(features_scaled, labels)
        self.is_trained = True
        
        logger.info("Adoption prediction model trained successfully")
    
    def _extract_features(self, animal_data: Dict) -> List[float]:
        """Extract features from animal data"""
        features = [
            animal_data.get('age', 0),
            len(animal_data.get('breed', '')),
            animal_data.get('behavior_score', 0.5),
            animal_data.get('health_score', 0.5),
            # Add more features as needed
        ]
        return features
    
    def predict(self, animal_data: Dict) -> float:
        """Predict adoption probability"""
        if not self.is_trained:
            return 0.5  # Default probability
        
        features = self._extract_features(animal_data)
        features_scaled = self.scaler.transform([features])
        probability = self.model.predict_proba(features_scaled)[0][1]
        return probability

class BehaviorAnalyzer:
    """Analyze animal behavior patterns"""
    
    def __init__(self):
        self.behavior_patterns = {}
    
    def analyze_behavior(self, animal_data: Dict) -> float:
        """Analyze behavior and return a score"""
        # Simple behavior scoring based on various factors
        score = 0.5  # Base score
        
        # Age factor (younger animals tend to be more adoptable)
        age = animal_data.get('age', 0)
        if age < 2:
            score += 0.2
        elif age < 5:
            score += 0.1
        
        # Breed factor (some breeds are more popular)
        breed = animal_data.get('breed', '').lower()
        popular_breeds = ['labrador', 'golden retriever', 'german shepherd', 'bulldog']
        if any(pop in breed for pop in popular_breeds):
            score += 0.1
        
        # Health factor
        health_score = animal_data.get('health_score', 0.5)
        score += health_score * 0.2
        
        return min(1.0, max(0.0, score))

# Initialize ML models
adoption_predictor = AdoptionPredictor()
behavior_analyzer = BehaviorAnalyzer()

# Middleware for request tracking
@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    # Record metrics
    duration = time.time() - g.start_time
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint,
        status=response.status_code
    ).inc()
    REQUEST_LATENCY.observe(duration)
    
    # Add response headers
    response.headers['X-Response-Time'] = str(duration)
    return response

# Authentication decorators
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# Cache decorator
def cache_response(timeout=300):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f"cache:{request.path}:{request.query_string.decode()}"
            cached_response = redis_client.get(cache_key)
            
            if cached_response:
                return json.loads(cached_response)
            
            response = f(*args, **kwargs)
            redis_client.setex(cache_key, timeout, json.dumps(response))
            return response
        return decorated_function
    return decorator

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Enhanced Animal Shelter Management System',
        'version': '2.0.0',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/api/auth/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409
        
        # Create new user (in production, hash the password)
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=data['password'],  # Should be hashed in production
            role='user'
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['username', 'password']):
            return jsonify({'error': 'Missing username or password'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or user.password_hash != data['password']:  # Should verify hash in production
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/animals', methods=['GET'])
@cache_response(timeout=60)
def get_animals():
    """Get all animals with filtering and pagination"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        animal_type = request.args.get('animal_type')
        breed = request.args.get('breed')
        outcome = request.args.get('outcome')
        
        # Build query
        query = Animal.query
        
        if animal_type:
            query = query.filter(Animal.animal_type == animal_type)
        if breed:
            query = query.filter(Animal.breed.ilike(f'%{breed}%'))
        if outcome:
            query = query.filter(Animal.outcome == outcome)
        
        # Paginate results
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        animals = [animal.to_dict() for animal in pagination.items]
        
        return jsonify({
            'animals': animals,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving animals: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/animals', methods=['POST'])
@jwt_required()
@limiter.limit("100 per hour")
def create_animal():
    """Create a new animal record"""
    try:
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        # Analyze behavior and predict adoption probability
        behavior_score = behavior_analyzer.analyze_behavior(data)
        adoption_probability = adoption_predictor.predict(data)
        
        animal = Animal(
            name=data['name'],
            age=data.get('age'),
            animal_type=data.get('animal_type'),
            breed=data.get('breed'),
            outcome=data.get('outcome'),
            intake_date=datetime.fromisoformat(data['intake_date']) if data.get('intake_date') else None,
            behavior_score=behavior_score,
            health_score=data.get('health_score', 0.5),
            adoption_probability=adoption_probability
        )
        
        db.session.add(animal)
        db.session.commit()
        
        # Clear cache
        redis_client.delete('cache:/api/animals:*')
        
        return jsonify({
            'message': 'Animal created successfully',
            'animal': animal.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating animal: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/animals/<int:animal_id>', methods=['GET'])
@cache_response(timeout=300)
def get_animal(animal_id):
    """Get a specific animal by ID"""
    try:
        animal = Animal.query.get_or_404(animal_id)
        return jsonify(animal.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error retrieving animal {animal_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/animals/<int:animal_id>', methods=['PUT'])
@jwt_required()
def update_animal(animal_id):
    """Update an animal record"""
    try:
        animal = Animal.query.get_or_404(animal_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields
        for field, value in data.items():
            if hasattr(animal, field) and field not in ['id', 'created_at']:
                if field in ['intake_date', 'outcome_date'] and value:
                    setattr(animal, field, datetime.fromisoformat(value))
                else:
                    setattr(animal, field, value)
        
        # Recalculate scores
        animal.behavior_score = behavior_analyzer.analyze_behavior(animal.to_dict())
        animal.adoption_probability = adoption_predictor.predict(animal.to_dict())
        animal.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Clear cache
        redis_client.delete('cache:/api/animals:*')
        
        return jsonify({
            'message': 'Animal updated successfully',
            'animal': animal.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating animal {animal_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/analytics/dashboard', methods=['GET'])
@jwt_required()
@cache_response(timeout=300)
def get_dashboard_data():
    """Get dashboard analytics data"""
    try:
        # Get basic statistics
        total_animals = Animal.query.count()
        adopted_animals = Animal.query.filter_by(outcome='Adoption').count()
        adoption_rate = (adopted_animals / total_animals * 100) if total_animals > 0 else 0
        
        # Get animals by type
        animals_by_type = db.session.query(
            Animal.animal_type, db.func.count(Animal.id)
        ).group_by(Animal.animal_type).all()
        
        # Get recent adoptions
        recent_adoptions = Animal.query.filter_by(outcome='Adoption')\
            .order_by(Animal.outcome_date.desc())\
            .limit(10).all()
        
        # Get adoption trends (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_adoptions_count = Animal.query.filter(
            Animal.outcome == 'Adoption',
            Animal.outcome_date >= thirty_days_ago
        ).count()
        
        return jsonify({
            'total_animals': total_animals,
            'adopted_animals': adopted_animals,
            'adoption_rate': round(adoption_rate, 2),
            'animals_by_type': dict(animals_by_type),
            'recent_adoptions': [animal.to_dict() for animal in recent_adoptions],
            'recent_adoptions_count': recent_adoptions_count
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting dashboard data: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/analytics/predictions', methods=['POST'])
@jwt_required()
def get_predictions():
    """Get ML predictions for animal data"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Get predictions
        behavior_score = behavior_analyzer.analyze_behavior(data)
        adoption_probability = adoption_predictor.predict(data)
        
        return jsonify({
            'behavior_score': round(behavior_score, 3),
            'adoption_probability': round(adoption_probability, 3),
            'recommendations': _generate_recommendations(data, behavior_score, adoption_probability)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting predictions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def _generate_recommendations(animal_data: Dict, behavior_score: float, adoption_probability: float) -> List[str]:
    """Generate recommendations based on ML predictions"""
    recommendations = []
    
    if adoption_probability < 0.3:
        recommendations.append("Consider special promotion or reduced adoption fees")
        recommendations.append("Focus on highlighting unique qualities")
    
    if behavior_score < 0.4:
        recommendations.append("Consider additional training or socialization")
        recommendations.append("Highlight positive behavior traits")
    
    if animal_data.get('age', 0) > 7:
        recommendations.append("Consider senior pet promotion programs")
        recommendations.append("Highlight benefits of adopting older animals")
    
    if not recommendations:
        recommendations.append("Animal shows good adoption potential")
    
    return recommendations

@app.route('/api/analytics/reports', methods=['POST'])
@jwt_required()
@admin_required
def generate_report():
    """Generate custom analytics report"""
    try:
        data = request.get_json()
        report_type = data.get('type', 'adoption_summary')
        
        if report_type == 'adoption_summary':
            # Generate adoption summary report
            report_data = _generate_adoption_summary()
        elif report_type == 'trend_analysis':
            # Generate trend analysis report
            report_data = _generate_trend_analysis()
        else:
            return jsonify({'error': 'Invalid report type'}), 400
        
        return jsonify({
            'report_type': report_type,
            'generated_at': datetime.utcnow().isoformat(),
            'data': report_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def _generate_adoption_summary():
    """Generate adoption summary report"""
    total_animals = Animal.query.count()
    adopted_animals = Animal.query.filter_by(outcome='Adoption').count()
    
    # Get adoption rates by animal type
    adoption_by_type = db.session.query(
        Animal.animal_type,
        db.func.count(Animal.id).label('total'),
        db.func.sum(db.case([(Animal.outcome == 'Adoption', 1)], else_=0)).label('adopted')
    ).group_by(Animal.animal_type).all()
    
    return {
        'total_animals': total_animals,
        'adopted_animals': adopted_animals,
        'adoption_rate': round((adopted_animals / total_animals * 100), 2) if total_animals > 0 else 0,
        'adoption_by_type': [
            {
                'animal_type': row.animal_type,
                'total': row.total,
                'adopted': row.adopted,
                'rate': round((row.adopted / row.total * 100), 2) if row.total > 0 else 0
            }
            for row in adoption_by_type
        ]
    }

def _generate_trend_analysis():
    """Generate trend analysis report"""
    # Get monthly adoption trends for the last 12 months
    trends = []
    for i in range(12):
        start_date = datetime.utcnow() - timedelta(days=30 * (i + 1))
        end_date = datetime.utcnow() - timedelta(days=30 * i)
        
        monthly_adoptions = Animal.query.filter(
            Animal.outcome == 'Adoption',
            Animal.outcome_date >= start_date,
            Animal.outcome_date < end_date
        ).count()
        
        trends.append({
            'month': start_date.strftime('%Y-%m'),
            'adoptions': monthly_adoptions
        })
    
    return {
        'monthly_trends': list(reversed(trends)),
        'total_trend_period': 12
    }

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def ratelimit_handler(error):
    return jsonify({'error': 'Rate limit exceeded'}), 429

# Initialize database
def init_database():
    """Initialize the database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@shelter.com',
                password_hash='admin123',  # Should be hashed in production
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            logger.info("Admin user created")

if __name__ == '__main__':
    init_database()
    app.run(
        debug=app_config.DEBUG, 
        host=app_config.HOST, 
        port=app_config.PORT
    )
