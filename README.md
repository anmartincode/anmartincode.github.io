# Andy Martinez - Computer Science ePortfolio

## Overview

This ePortfolio showcases my growth and development throughout my Computer Science program at SNHU. It demonstrates proficiency across three key domains: Software Design & Engineering, Algorithms & Data Structures, and Databases. Each artifact has been enhanced to show advanced skills and professional development practices.

## 🚀 Live Portfolio

**GitHub Pages URL**: [https://anmartincode.github.io](https://anmartincode.github.io)

## 📁 Project Structure

```
anmartincode.github.io/
├── index.html                 # Main portfolio homepage
├── styles.css                 # Portfolio styling
├── script.js                  # Interactive features
├── narratives/                # Written narratives for each artifact
│   ├── software-design-narrative.md
│   ├── algorithms-narrative.md
│   └── databases-narrative.md
├── Software Design and Engineering/
│   ├── main.py               # Enhanced MongoDB CRUD operations
│   ├── app.py                # Flask REST API
│   └── requirements.txt      # Python dependencies
├── Algorithms and Data Structures/
│   └── flask-algoviz/        # Interactive algorithm visualizer
│       ├── app/
│       │   ├── algorithms/
│       │   │   ├── avl_tree.py    # Complete AVL tree implementation
│       │   │   ├── graph.py       # Graph algorithms (BFS, DFS, Dijkstra)
│       │   │   └── heap.py        # Min/Max heap implementation
│       │   └── routes.py          # Flask routes
│       └── requirements.txt
└── Databases/
    ├── contacts_cli.py       # Enhanced contact management system
    ├── requirements.txt      # Python dependencies
    └── sample_contacts.json  # Sample data
```

## 🎯 Enhanced Artifacts

### 1. Software Design & Engineering
**Animal Shelter Management System**

- **Original**: Basic MongoDB CRUD operations
- **Enhanced**: 
  - RESTful API with Flask
  - Advanced data validation with JSON schema
  - Comprehensive error handling and logging
  - Performance optimization
  - Security best practices

**Key Features:**
- Complete CRUD operations with MongoDB
- RESTful API endpoints
- Data validation and sanitization
- Structured logging
- Error handling and recovery
- Performance monitoring

### 2. Algorithms & Data Structures
**Interactive Algorithm Visualizer**

- **Original**: Basic placeholder implementations
- **Enhanced**:
  - Complete AVL tree with balancing
  - Graph algorithms (BFS, DFS, Dijkstra)
  - Min/Max heap with full operations
  - Step-by-step visualization
  - Performance benchmarking

**Key Features:**
- AVL tree with insert, delete, search operations
- Graph traversal and pathfinding algorithms
- Heap operations (insert, extract, heapify)
- Real-time algorithm visualization
- Performance metrics and analysis

### 3. Databases
**Contact Management System**

- **Original**: Basic SQLite CLI application
- **Enhanced**:
  - Advanced database schema with indexes
  - Performance monitoring and optimization
  - Data analytics and reporting
  - Backup and restore functionality
  - Export capabilities (CSV, JSON)

**Key Features:**
- Enhanced SQLite database with indexes
- Performance monitoring and slow query detection
- Contact analytics and reporting
- Database backup and restore
- Data export in multiple formats
- Advanced search and filtering

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Git
- Web browser

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/anmartincode/anmartincode.github.io.git
   cd anmartincode.github.io
   ```

2. **Software Design & Engineering Setup**
   ```bash
   cd "Software Design and Engineering"
   pip install -r requirements.txt
   python app.py
   ```
   - API will be available at `http://localhost:5000`
   - Health check: `http://localhost:5000/api/health`

3. **Algorithms & Data Structures Setup**
   ```bash
   cd "Algorithms and Data Structures/flask-algoviz"
   pip install -r requirements.txt
   python -m flask run
   ```
   - Visualizer will be available at `http://localhost:5000`

4. **Databases Setup**
   ```bash
   cd Databases
   pip install -r requirements.txt
   python contacts_cli.py --help
   ```

### Usage Examples

#### Animal Shelter API
```bash
# Create an animal
curl -X POST http://localhost:5000/api/animals \
  -H "Content-Type: application/json" \
  -d '{"name":"Buddy","age":3,"animal_type":"Dog","breed":"Golden Retriever","outcome":"Adopted"}'

# Get all animals
curl http://localhost:5000/api/animals

# Search animals
curl "http://localhost:5000/api/animals/search?q=dog&min_age=1&max_age=5"
```

#### Contact Management
```bash
# Load sample data
python contacts_cli.py load sample_contacts.json

# Add a contact
python contacts_cli.py add --name "John Doe" --email "john@example.com" --company "Tech Corp"

# Search contacts
python contacts_cli.py lookup "john"

# View analytics
python contacts_cli.py analytics

# Export data
python contacts_cli.py export --format csv
```

#### Algorithm Visualizer
- Open `http://localhost:5000` in your browser
- Select an algorithm (AVL Tree, Graph, or Heap)
- Use the interactive controls to visualize operations

## 📊 Course Outcomes Demonstrated

### CS-340 (Client/Server Development)
- ✅ Design and develop client/server applications
- ✅ Implement database connectivity and data access patterns
- ✅ Apply security principles to client/server applications
- ✅ Implement proper error handling and logging

### CS-260 (Data Structures and Algorithms)
- ✅ Analyze and implement fundamental data structures
- ✅ Design and implement efficient algorithms
- ✅ Analyze algorithm complexity and performance
- ✅ Apply data structures and algorithms to solve real-world problems

### Professional Skills
- ✅ Team collaboration and communication
- ✅ Stakeholder communication
- ✅ Software engineering best practices
- ✅ Database design and optimization
- ✅ Security implementation
- ✅ Performance monitoring and optimization

## 🎥 Code Review Video

A comprehensive code review video has been created that covers:
- Current functionality walkthrough for each artifact
- Code analysis identifying areas for improvement
- Enhancement plans and skills demonstrated
- Technical implementation details

## 📝 Written Narratives

Detailed narratives for each artifact are available in the `narratives/` directory:
- [Software Design & Engineering Narrative](narratives/software-design-narrative.md)
- [Algorithms & Data Structures Narrative](narratives/algorithms-narrative.md)
- [Databases Narrative](narratives/databases-narrative.md)

## 🔧 Technical Enhancements

### Performance Optimizations
- Database indexing for faster queries
- Algorithm complexity analysis
- Query performance monitoring
- Memory-efficient data structures

### Security Improvements
- Input validation and sanitization
- SQL injection prevention
- Data encryption considerations
- Access control implementation

### User Experience
- Interactive visualizations
- Comprehensive error messages
- Intuitive command-line interfaces
- Responsive web design

## 📈 Growth Demonstration

This portfolio demonstrates quantifiable growth through:
- **Complexity**: From basic implementations to production-ready systems
- **Functionality**: From single-purpose tools to comprehensive applications
- **Architecture**: From simple scripts to well-structured, maintainable code
- **Performance**: From basic operations to optimized, scalable solutions
- **Security**: From basic functionality to security-conscious implementations

## 🤝 Contact Information

- **GitHub**: [github.com/anmartincode](https://github.com/anmartincode)
- **LinkedIn**: [linkedin.com/in/andymartinez](https://www.linkedin.com/in/andy-martinez-478427b9/)


## 📄 License

This project is part of my academic portfolio for SNHU's Computer Science program. All code is original work demonstrating my technical skills and growth throughout the program.

---

**Note**: This ePortfolio represents my journey through the Computer Science program, showcasing both foundational knowledge and advanced skills developed through continuous learning and practical application.
