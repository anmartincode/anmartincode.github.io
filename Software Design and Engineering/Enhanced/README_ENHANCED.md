# Enhanced Animal Shelter Management System

## Overview
This enhanced version of the Animal Shelter Management System provides advanced features including:
- **Real-time analytics and reporting**
- **Machine learning for outcome prediction**
- **Advanced data visualization**
- **RESTful API with authentication**
- **Microservices architecture**
- **Automated testing and CI/CD**
- **Performance monitoring and optimization**

## Enhanced Features

### 1. Advanced Analytics and Reporting
- **Real-time dashboard with interactive charts**
- **Predictive analytics for adoption success**
- **Trend analysis and forecasting**
- **Custom report generation**
- **Data export in multiple formats (CSV, JSON, PDF)**

### 2. Machine Learning Integration
- **Adoption outcome prediction model**
- **Animal behavior analysis**
- **Optimal care recommendations**
- **Resource allocation optimization**
- **Anomaly detection for health monitoring**

### 3. Advanced Data Visualization
- **Interactive charts using Plotly and Dash**
- **Geographic data visualization**
- **Time-series analysis**
- **Comparative analytics**
- **Real-time data streaming**

### 4. RESTful API with Authentication
- **JWT-based authentication**
- **Role-based access control**
- **API rate limiting**
- **Comprehensive API documentation**
- **GraphQL support for complex queries**

### 5. Microservices Architecture
- **Service discovery and load balancing**
- **Message queuing for async operations**
- **Distributed caching with Redis**
- **Container orchestration with Docker**
- **Service monitoring and health checks**

### 6. Performance Optimization
- **Database query optimization**
- **Caching strategies**
- **Connection pooling**
- **Asynchronous processing**
- **Load testing and benchmarking**

## Installation

### Quick Setup (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd "Software Design and Engineering/Enhanced"

# Run the automated setup script
python setup.py

# Start the application (handles port conflicts automatically)
python start_app.py
```

### Manual Setup
```bash
# Clone the repository
git clone <repository-url>
cd "Software Design and Engineering/Enhanced"

# Install dependencies
pip install -r requirements_enhanced.txt

# Set up configuration
cp config.example.py config.py
# Edit config.py with your configuration

# Create necessary directories
mkdir -p logs models data reports uploads

# Start the application
python enhanced_app.py
```

## Usage

### Starting the Enhanced Application
```bash
# Start the main application (recommended - handles port conflicts)
python start_app.py

# Start the analytics dashboard
python start_app.py dashboard

# Run the demo
python start_app.py demo

# Alternative: Start components individually
python enhanced_app.py
python analytics_dashboard.py
```

### API Endpoints

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/refresh` - Refresh JWT token
- `POST /api/auth/logout` - User logout

#### Animal Management
- `GET /api/animals` - Get all animals with filtering
- `POST /api/animals` - Create new animal record
- `GET /api/animals/{id}` - Get specific animal
- `PUT /api/animals/{id}` - Update animal record
- `DELETE /api/animals/{id}` - Delete animal record
- `POST /api/animals/{id}/adopt` - Adopt an animal

#### Analytics
- `GET /api/analytics/dashboard` - Get dashboard data
- `GET /api/analytics/predictions` - Get ML predictions
- `GET /api/analytics/reports` - Generate custom reports
- `GET /api/analytics/trends` - Get trend analysis

#### Health Monitoring
- `GET /api/health` - Service health check
- `GET /api/health/metrics` - Performance metrics
- `GET /api/health/logs` - Application logs

## Configuration

### Setup Configuration
```bash
# Copy the configuration template
cp config.example.py config.py

# Edit config.py with your actual values
# The application will use environment variables if set, otherwise defaults from config.py
```

### Environment Variables
```bash
# Database Configuration
DATABASE_URL=mongodb://localhost:27017/animal_shelter_enhanced
REDIS_URL=redis://localhost:6379

# Authentication
JWT_SECRET_KEY=your-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=86400

# ML Model Configuration
ML_MODEL_PATH=models/adoption_predictor.pkl
ML_FEATURES_PATH=models/feature_scaler.pkl

# API Configuration
API_RATE_LIMIT=100
API_RATE_LIMIT_WINDOW=3600

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
```

### Database Schema
```sql
-- Enhanced animal records with additional fields
CREATE TABLE animals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INTEGER,
    animal_type VARCHAR(50),
    breed VARCHAR(100),
    outcome VARCHAR(50),
    intake_date TIMESTAMP,
    outcome_date TIMESTAMP,
    behavior_score FLOAT,
    health_score FLOAT,
    adoption_probability FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User management
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics events
CREATE TABLE analytics_events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Machine Learning Features

### Adoption Prediction Model
```python
from enhanced_ml import AdoptionPredictor

predictor = AdoptionPredictor()
prediction = predictor.predict_adoption_probability(animal_data)
print(f"Adoption probability: {prediction:.2%}")
```

### Behavior Analysis
```python
from enhanced_ml import BehaviorAnalyzer

analyzer = BehaviorAnalyzer()
behavior_score = analyzer.analyze_behavior(animal_data)
print(f"Behavior score: {behavior_score}")
```

## Performance Monitoring

### Metrics Dashboard
- **Response time monitoring**
- **Error rate tracking**
- **Database performance metrics**
- **Memory and CPU usage**
- **API endpoint analytics**

### Health Checks
```bash
# Check service health
curl http://localhost:5000/api/health

# Get performance metrics
curl http://localhost:5000/api/health/metrics
```

## Testing

### Automated Testing
```bash
# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/

# Run performance tests
python -m pytest tests/performance/

# Generate coverage report
python -m pytest --cov=app tests/
```

### Load Testing
```bash
# Run load tests with Locust
locust -f tests/load/locustfile.py --host=http://localhost:5000
```

## Deployment

### Docker Deployment
```bash
# Build Docker image
docker build -t animal-shelter-enhanced .

# Run with Docker Compose
docker-compose up -d
```

### Kubernetes Deployment
```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl get services
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your enhancement
4. Add tests
5. Update documentation
6. Submit a pull request

## License

MIT License - see LICENSE file for details

## Troubleshooting

### Port Conflicts
If you encounter "Address already in use" errors:
- **macOS**: Disable AirPlay Receiver in System Preferences → General → AirDrop & Handoff
- **Use the start script**: `python start_app.py` automatically finds available ports
- **Manual port change**: Edit `config.py` and change the PORT value

### Common Issues
- **Import errors**: Run `python setup.py` to install dependencies
- **Database errors**: The application will create the database automatically on first run
- **API connection errors**: Ensure the main application is running before starting the dashboard

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation wiki
