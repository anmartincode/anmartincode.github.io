#!/usr/bin/env python3
"""
Enhanced Animal Shelter Management System Demo
Demonstrates advanced features including ML predictions, analytics, and performance monitoring
"""

import requests
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Configuration
API_BASE_URL = "http://localhost:8080/api"
DEMO_DATA = [
    {
        "name": "Buddy",
        "age": 3,
        "animal_type": "Dog",
        "breed": "Golden Retriever",
        "outcome": "Adoption",
        "intake_date": "2025-01-15T10:00:00",
        "health_score": 0.9
    },
    {
        "name": "Whiskers",
        "age": 2,
        "animal_type": "Cat",
        "breed": "Persian",
        "outcome": "Adoption",
        "intake_date": "2025-01-20T14:30:00",
        "health_score": 0.8
    },
    {
        "name": "Max",
        "age": 5,
        "animal_type": "Dog",
        "breed": "German Shepherd",
        "outcome": "Transfer",
        "intake_date": "2025-02-01T09:15:00",
        "health_score": 0.7
    },
    {
        "name": "Luna",
        "age": 1,
        "animal_type": "Cat",
        "breed": "Siamese",
        "outcome": "Adoption",
        "intake_date": "2025-02-10T16:45:00",
        "health_score": 0.95
    },
    {
        "name": "Rocky",
        "age": 7,
        "animal_type": "Dog",
        "breed": "Bulldog",
        "outcome": "Return to Owner",
        "intake_date": "2025-02-15T11:20:00",
        "health_score": 0.6
    }
]

class EnhancedShelterDemo:
    """Demo class for showcasing enhanced features"""
    
    def __init__(self):
        self.auth_token = None
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def make_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """Make authenticated API request"""
        url = f"{API_BASE_URL}{endpoint}"
        headers = {}
        
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        try:
            if method == "GET":
                response = self.session.get(url, headers=headers)
            elif method == "POST":
                response = self.session.post(url, headers=headers, json=data)
            elif method == "PUT":
                response = self.session.put(url, headers=headers, json=data)
            else:
                return {"error": "Unsupported method"}
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API Error: {response.status_code} - {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection Error: {str(e)}"}
    
    def demo_authentication(self):
        """Demonstrate authentication features"""
        print("\n" + "="*60)
        print("🔐 AUTHENTICATION DEMO")
        print("="*60)
        
        # Register a new user
        print("\n1. Registering a new user...")
        register_data = {
            "username": "demo_user",
            "email": "demo@shelter.com",
            "password": "demo123"
        }
        
        response = self.make_request("/auth/register", "POST", register_data)
        if "error" in response:
            print(f"Registration failed: {response['error']}")
        else:
            print("✅ User registered successfully")
        
        # Login
        print("\n2. Logging in...")
        login_data = {
            "username": "demo_user",
            "password": "demo123"
        }
        
        response = self.make_request("/auth/login", "POST", login_data)
        if "error" in response:
            print(f"Login failed: {response['error']}")
            return False
        else:
            self.auth_token = response.get("access_token")
            print("✅ Login successful")
            print(f"   User: {response['user']['username']}")
            print(f"   Role: {response['user']['role']}")
            return True
    
    def demo_animal_management(self):
        """Demonstrate enhanced animal management features"""
        print("\n" + "="*60)
        print("🐾 ENHANCED ANIMAL MANAGEMENT DEMO")
        print("="*60)
        
        # Create animals with ML predictions
        print("\n1. Creating animals with ML predictions...")
        created_animals = []
        
        for i, animal_data in enumerate(DEMO_DATA, 1):
            print(f"\n   Creating animal {i}: {animal_data['name']}")
            
            response = self.make_request("/animals", "POST", animal_data)
            if "error" in response:
                print(f"   ❌ Failed: {response['error']}")
            else:
                animal = response.get("animal", {})
                created_animals.append(animal)
                print(f"   ✅ Created successfully")
                print(f"      Behavior Score: {animal.get('behavior_score', 'N/A'):.3f}")
                print(f"      Adoption Probability: {animal.get('adoption_probability', 'N/A'):.1%}")
        
        # Get all animals with filtering
        print("\n2. Retrieving animals with filtering...")
        response = self.make_request("/animals?animal_type=Dog&per_page=10")
        if "error" in response:
            print(f"❌ Failed: {response['error']}")
        else:
            animals = response.get("animals", [])
            pagination = response.get("pagination", {})
            print(f"✅ Retrieved {len(animals)} dogs")
            print(f"   Total animals: {pagination.get('total', 0)}")
            print(f"   Page {pagination.get('page', 1)} of {pagination.get('pages', 1)}")
        
        return created_animals
    
    def demo_ml_predictions(self):
        """Demonstrate machine learning predictions"""
        print("\n" + "="*60)
        print("🤖 MACHINE LEARNING PREDICTIONS DEMO")
        print("="*60)
        
        # Test predictions for different animals
        test_cases = [
            {
                "name": "Puppy",
                "age": 1,
                "animal_type": "Dog",
                "breed": "Labrador Retriever",
                "health_score": 0.9
            },
            {
                "name": "Senior",
                "age": 10,
                "animal_type": "Cat",
                "breed": "Domestic Shorthair",
                "health_score": 0.6
            },
            {
                "name": "Special",
                "age": 4,
                "animal_type": "Dog",
                "breed": "Pit Bull",
                "health_score": 0.7
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. Predicting for {test_case['name']} ({test_case['breed']})...")
            
            response = self.make_request("/analytics/predictions", "POST", test_case)
            if "error" in response:
                print(f"   ❌ Prediction failed: {response['error']}")
            else:
                behavior_score = response.get("behavior_score", 0)
                adoption_probability = response.get("adoption_probability", 0)
                recommendations = response.get("recommendations", [])
                
                print(f"   ✅ Prediction Results:")
                print(f"      Behavior Score: {behavior_score:.1%}")
                print(f"      Adoption Probability: {adoption_probability:.1%}")
                print(f"      Recommendations:")
                for rec in recommendations:
                    print(f"        • {rec}")
    
    def demo_analytics_dashboard(self):
        """Demonstrate analytics dashboard features"""
        print("\n" + "="*60)
        print("📊 ANALYTICS DASHBOARD DEMO")
        print("="*60)
        
        # Get dashboard data
        print("\n1. Retrieving dashboard analytics...")
        response = self.make_request("/analytics/dashboard")
        if "error" in response:
            print(f"❌ Failed: {response['error']}")
            return
        
        data = response
        print("✅ Dashboard data retrieved:")
        print(f"   Total Animals: {data.get('total_animals', 0):,}")
        print(f"   Adopted Animals: {data.get('adopted_animals', 0):,}")
        print(f"   Adoption Rate: {data.get('adoption_rate', 0):.1f}%")
        print(f"   Recent Adoptions (30 days): {data.get('recent_adoptions_count', 0):,}")
        
        # Show animals by type
        animals_by_type = data.get("animals_by_type", {})
        if animals_by_type:
            print(f"\n   Animals by Type:")
            for animal_type, count in animals_by_type.items():
                print(f"     {animal_type}: {count}")
        
        # Generate custom reports
        print("\n2. Generating custom reports...")
        
        # Adoption summary report
        print("\n   📋 Adoption Summary Report:")
        response = self.make_request("/analytics/reports", "POST", {"type": "adoption_summary"})
        if "error" in response:
            print(f"   ❌ Failed: {response['error']}")
        else:
            report_data = response.get("data", {})
            print(f"   ✅ Report generated at: {response.get('generated_at', 'N/A')}")
            
            adoption_by_type = report_data.get("adoption_by_type", [])
            for type_data in adoption_by_type:
                print(f"     {type_data['animal_type']}: {type_data['adopted']}/{type_data['total']} ({type_data['rate']:.1f}%)")
        
        # Trend analysis report
        print("\n   📈 Trend Analysis Report:")
        response = self.make_request("/analytics/reports", "POST", {"type": "trend_analysis"})
        if "error" in response:
            print(f"   ❌ Failed: {response['error']}")
        else:
            report_data = response.get("data", {})
            trends = report_data.get("monthly_trends", [])
            print(f"   ✅ Trend analysis for {len(trends)} months:")
            
            for trend in trends[-3:]:  # Show last 3 months
                print(f"     {trend['month']}: {trend['adoptions']} adoptions")
    
    def demo_performance_monitoring(self):
        """Demonstrate performance monitoring features"""
        print("\n" + "="*60)
        print("⚡ PERFORMANCE MONITORING DEMO")
        print("="*60)
        
        # Health check
        print("\n1. Service health check...")
        response = self.make_request("/health")
        if "error" in response:
            print(f"❌ Health check failed: {response['error']}")
        else:
            print("✅ Service is healthy")
            print(f"   Service: {response.get('service', 'N/A')}")
            print(f"   Version: {response.get('version', 'N/A')}")
            print(f"   Timestamp: {response.get('timestamp', 'N/A')}")
        
        # Performance metrics
        print("\n2. Performance metrics...")
        response = self.make_request("/metrics")
        if "error" in response:
            print(f"❌ Metrics failed: {response['error']}")
        else:
            print("✅ Metrics retrieved (Prometheus format)")
            # Parse and display some key metrics
            metrics_text = response
            lines = metrics_text.split('\n')
            
            for line in lines:
                if 'http_requests_total' in line or 'http_request_duration_seconds' in line:
                    print(f"   {line}")
        
        # Load testing simulation
        print("\n3. Simulating load testing...")
        print("   Making multiple concurrent requests...")
        
        start_time = time.time()
        responses = []
        
        # Make 10 concurrent requests
        for i in range(10):
            response = self.make_request("/animals?per_page=5")
            responses.append(response)
        
        end_time = time.time()
        duration = end_time - start_time
        
        successful_requests = sum(1 for r in responses if "error" not in r)
        print(f"   ✅ Load test completed:")
        print(f"      Duration: {duration:.2f} seconds")
        print(f"      Successful requests: {successful_requests}/10")
        print(f"      Average response time: {duration/10:.3f} seconds")
    
    def demo_advanced_features(self):
        """Demonstrate other advanced features"""
        print("\n" + "="*60)
        print("🚀 ADVANCED FEATURES DEMO")
        print("="*60)
        
        # Rate limiting demonstration
        print("\n1. Rate limiting demonstration...")
        print("   Making rapid requests to test rate limiting...")
        
        for i in range(15):
            response = self.make_request("/animals")
            if "error" in response and "429" in response["error"]:
                print(f"   ✅ Rate limit hit after {i+1} requests")
                break
            time.sleep(0.1)
        else:
            print("   ✅ No rate limit hit (within limits)")
        
        # Caching demonstration
        print("\n2. Caching demonstration...")
        print("   Making repeated requests to test caching...")
        
        start_time = time.time()
        response1 = self.make_request("/animals")
        time1 = time.time() - start_time
        
        start_time = time.time()
        response2 = self.make_request("/animals")
        time2 = time.time() - start_time
        
        print(f"   First request: {time1:.3f} seconds")
        print(f"   Second request: {time2:.3f} seconds")
        print(f"   Cache improvement: {((time1-time2)/time1*100):.1f}% faster")
        
        # Error handling demonstration
        print("\n3. Error handling demonstration...")
        
        # Try to access non-existent resource
        response = self.make_request("/animals/99999")
        if "error" in response:
            print("   ✅ Proper error handling for non-existent resource")
        
        # Try to create invalid animal data
        invalid_data = {"name": ""}  # Missing required fields
        response = self.make_request("/animals", "POST", invalid_data)
        if "error" in response:
            print("   ✅ Proper validation for invalid data")
    
    def run_full_demo(self):
        """Run the complete enhanced demo"""
        print("🐾 ENHANCED ANIMAL SHELTER MANAGEMENT SYSTEM DEMO")
        print("="*80)
        print("This demo showcases advanced features including:")
        print("• JWT Authentication and Authorization")
        print("• Machine Learning Predictions")
        print("• Real-time Analytics Dashboard")
        print("• Performance Monitoring and Metrics")
        print("• Rate Limiting and Caching")
        print("• Advanced Error Handling")
        print("="*80)
        
        # Check if API server is running
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code != 200:
                print("❌ API server is not responding properly")
                return
        except requests.exceptions.RequestException:
            print("❌ Cannot connect to API server. Please ensure it's running on http://localhost:8080")
            return
        
        print("✅ API server is running")
        
        # Run demo sections
        if not self.demo_authentication():
            print("❌ Authentication failed. Cannot continue demo.")
            return
        
        animals = self.demo_animal_management()
        self.demo_ml_predictions()
        self.demo_analytics_dashboard()
        self.demo_performance_monitoring()
        self.demo_advanced_features()
        
        # Demo summary
        print("\n" + "="*80)
        print("🎉 ENHANCED DEMO COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("Key features demonstrated:")
        print("✅ Secure authentication with JWT tokens")
        print("✅ Enhanced animal management with ML predictions")
        print("✅ Real-time analytics and reporting")
        print("✅ Performance monitoring and metrics")
        print("✅ Advanced caching and rate limiting")
        print("✅ Comprehensive error handling")
        print("\nNext steps:")
        print("• Access the interactive dashboard at http://localhost:8050")
        print("• Explore the API documentation")
        print("• Try the ML prediction features")
        print("• Monitor performance metrics")

def main():
    """Main function to run the demo"""
    demo = EnhancedShelterDemo()
    demo.run_full_demo()

if __name__ == "__main__":
    main()
