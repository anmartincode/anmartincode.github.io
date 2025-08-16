# Configuration template for Enhanced Animal Shelter Management System
# Copy this file to config.py and update with your actual values

import os
from datetime import timedelta

class Config:
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/animal_shelter_enhanced')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # Authentication
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 86400))
    
    # ML Model Configuration
    ML_MODEL_PATH = os.getenv('ML_MODEL_PATH', 'models/adoption_predictor.pkl')
    ML_FEATURES_PATH = os.getenv('ML_FEATURES_PATH', 'models/feature_scaler.pkl')
    
    # API Configuration
    API_RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', 100))
    API_RATE_LIMIT_WINDOW = int(os.getenv('API_RATE_LIMIT_WINDOW', 3600))
    
    # Monitoring
    PROMETHEUS_PORT = int(os.getenv('PROMETHEUS_PORT', 9090))
    GRAFANA_PORT = int(os.getenv('GRAFANA_PORT', 3000))
    
    # Application Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('PORT', 8080))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'mongodb://localhost:27017/animal_shelter_test'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
