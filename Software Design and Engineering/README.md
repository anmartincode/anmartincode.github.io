# Animal Shelter Management System

A comprehensive CRUD (Create, Read, Update, Delete) application for managing animal shelter data using MongoDB and Flask. This system provides both a backend API and data management capabilities for animal shelter operations.

## 📁 Project Structure

```
Software Design and Engineering/
├── app.py                 # Flask web application with REST API
├── main.py               # Core AnimalShelter class with MongoDB operations
├── crud.py               # Alternative CRUD implementation
├── requirements.txt      # Python dependencies
├── aac_shelter_outcomes.csv  # Sample animal shelter data
├── grazioso-logo.png     # Application logo
├── ProjectTwoDashboard.ipynb  # Jupyter notebook for data analysis
├── test_crud.ipynb       # Testing notebook for CRUD operations
└── Enhanced/             # Enhanced version of the application
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- MongoDB database access
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd "Software Design and Engineering"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MongoDB connection:**
   The application is configured to connect to a MongoDB instance. Update the connection details in `main.py` if needed:
   ```python
   USER = 'your_username'
   PASS = 'your_password'
   HOST = 'your_host'
   PORT = your_port
   ```

## 📋 Core Components

### 1. main.py - AnimalShelter Class

The core class that handles all database operations with MongoDB.

**Key Features:**
- JSON schema validation for animal data
- Structured logging
- Error handling for MongoDB operations
- CRUD operations (Create, Read, Update, Delete)

**Usage Example:**
```python
from main import AnimalShelter

# Initialize the shelter
shelter = AnimalShelter()

# Create a new animal
animal_data = {
    "name": "Buddy",
    "age": 3,
    "animal_type": "Dog",
    "breed": "Golden Retriever",
    "outcome": "Adoption"
}
success = shelter.create(animal_data)

# Read animals
dogs = shelter.read({"animal_type": "Dog"})

# Update animals
updated_count = shelter.update(
    {"name": "Buddy"}, 
    {"age": 4}
)

# Delete animals
deleted_count = shelter.delete({"name": "Buddy"})
```

### 2. app.py - Flask Web Application

A RESTful API that provides HTTP endpoints for animal shelter operations.

**Available Endpoints:**

- `GET /api/health` - Health check
- `POST /api/animals` - Create a new animal
- `GET /api/animals` - Get all animals or search by criteria
- `GET /api/animals/<animal_id>` - Get specific animal by ID
- `PUT /api/animals/<animal_id>` - Update an animal
- `DELETE /api/animals/<animal_id>` - Delete an animal
- `POST /api/animals/bulk` - Create multiple animals
- `GET /api/animals/statistics` - Get animal statistics
- `GET /api/animals/search` - Advanced search with pagination

**Running the API:**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### 3. crud.py - Alternative CRUD Implementation

An alternative implementation of the AnimalShelter class with different connection parameters.

**Usage:**
```python
from crud import AnimalShelter

# Initialize with custom connection parameters
shelter = AnimalShelter(
    host='localhost',
    port=27017,
    username='your_username',
    password='your_password'
)
```

## 📊 Data Structure

The system expects animal data with the following schema:

```json
{
    "name": "string",
    "age": "number",
    "animal_type": "string",
    "breed": "string",
    "outcome": "string"
}
```

**Required Fields:**
- `name`: Animal's name
- `age`: Animal's age in years
- `animal_type`: Type of animal (e.g., "Dog", "Cat")
- `breed`: Animal's breed
- `outcome`: Outcome status (e.g., "Adoption", "Transfer", "Return to Owner")

## 📈 Sample Data

The `aac_shelter_outcomes.csv` file contains sample animal shelter data with the following columns:
- `age_upon_outcome`: Age when outcome occurred
- `animal_id`: Unique animal identifier
- `animal_type`: Type of animal
- `breed`: Animal breed
- `color`: Animal color
- `date_of_birth`: Birth date
- `datetime`: Outcome date and time
- `name`: Animal name
- `outcome_type`: Type of outcome
- `sex_upon_outcome`: Sex of animal
- And more...

## 🧪 Testing

### Using Jupyter Notebooks

1. **test_crud.ipynb** - Test CRUD operations
2. **ProjectTwoDashboard.ipynb** - Data analysis and visualization

### API Testing

You can test the API endpoints using curl or any API client:

```bash
# Health check
curl http://localhost:5000/api/health

# Create an animal
curl -X POST http://localhost:5000/api/animals \
  -H "Content-Type: application/json" \
  -d '{"name":"Buddy","age":3,"animal_type":"Dog","breed":"Golden Retriever","outcome":"Adoption"}'

# Get all animals
curl http://localhost:5000/api/animals

# Search animals
curl "http://localhost:5000/api/animals?animal_type=Dog&breed=Golden%20Retriever"
```

## 🔧 Configuration

### Environment Variables

The application supports the following environment variables:
- `PORT`: Port number for the Flask app (default: 5000)

### MongoDB Connection

Update the connection parameters in `main.py`:
```python
USER = 'your_username'
PASS = 'your_password'
HOST = 'your_host'
PORT = your_port
DB = 'your_database'
COL = 'your_collection'
```

## 📝 Logging

The application uses structured logging with the following features:
- Log level: INFO
- Format: Timestamp, Level, Message
- Automatic logging of all CRUD operations
- Error logging for failed operations

## 🚨 Error Handling

The application includes comprehensive error handling:
- JSON schema validation errors
- MongoDB connection errors
- Invalid input data
- HTTP error responses with appropriate status codes

## 🔄 Enhanced Version

The `Enhanced/` directory contains an improved version of the application with additional features:
- Analytics dashboard
- Configuration management
- Enhanced logging
- Data migration tools
- Web interface templates

## 📚 Dependencies

- **Flask**: Web framework for the API
- **Flask-CORS**: Cross-origin resource sharing support
- **pymongo**: MongoDB driver for Python
- **jsonschema**: JSON schema validation
- **python-dotenv**: Environment variable management
- **gunicorn**: WSGI HTTP Server for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the CS499 Software Design and Engineering coursework.

## 🆘 Support

For issues or questions:
1. Check the logs for error messages
2. Verify MongoDB connection settings
3. Ensure all required fields are provided in data
4. Review the API documentation above

---

**Note:** This is a base implementation. For production use, consider implementing additional security measures, input sanitization, and proper authentication/authorization.
