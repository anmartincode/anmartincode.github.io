# Enhanced Contact Management System

A comprehensive contact management solution with normalized database schema, JSON metadata support, tags system, and modern web interface.

## 🚀 Features

### Core Enhancements
- **Normalized Schema**: Proper database design with separate tables for contacts, tags, and relationships
- **JSON Metadata**: Flexible metadata storage for birthdays, social handles, company info, and custom fields
- **Tags System**: Many-to-many relationship for organizing contacts with tags
- **Smart CLI**: Enhanced command-line interface with metadata operations
- **Web UI**: Modern Flask-based web application with REST API
- **Migration Tool**: Automated database schema migration and versioning
- **Backup System**: Automated database backups and recovery

### Technical Features
- **SQLite JSON1 Extension**: Leverages SQLite's JSON capabilities for efficient metadata queries
- **Indexed Queries**: Optimized database performance with strategic indexes
- **REST API**: Full CRUD operations via HTTP endpoints
- **Pagination**: Efficient handling of large contact lists
- **Search & Filtering**: Advanced search across all fields and metadata
- **Validation**: Email format validation and duplicate prevention

## 📁 Project Structure

```
Databases/
├── contacts_cli.py              # Original CLI application
├── contacts_cli_enhanced.py     # Enhanced CLI with metadata & tags
├── web_app.py                   # Flask web application
├── migration_tool.py            # Database migration utility
├── sample_contacts.json         # Original sample data
├── sample_contacts_enhanced.json # Enhanced sample data with metadata
├── requirements.txt             # Original dependencies
├── requirements_enhanced.txt    # Enhanced dependencies
├── templates/                   # Web UI templates
│   ├── base.html
│   ├── index.html
│   ├── contact_form.html
│   ├── 404.html
│   └── 500.html
├── README.md                    # Original documentation
└── README_ENHANCED.md          # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- SQLite 3.35+ (for JSON1 extension support)

### Setup
1. **Clone or navigate to the project directory**
   ```bash
   cd /path/to/Databases
   ```

2. **Install enhanced dependencies**
   ```bash
   pip install -r requirements_enhanced.txt
   ```

3. **Run database migration**
   ```bash
   python migration_tool.py --action migrate
   ```

## 🎯 Usage

### Enhanced CLI Application

The enhanced CLI provides all original functionality plus metadata and tags support:

```bash
# Load enhanced sample data
python contacts_cli_enhanced.py load sample_contacts_enhanced.json

# Add contact with metadata and tags
python contacts_cli_enhanced.py add --name "John Doe" --email "john@example.com" \
    --birthday "1990-05-15" --twitter "@johndoe" --tags "work,tech,friend"

# Search with metadata
python contacts_cli_enhanced.py lookup "tech" --metadata

# Update metadata for existing contact
python contacts_cli_enhanced.py update-metadata 1 --birthday "1990-05-15" --field "company=Tech Corp"

# Add tag to contact
python contacts_cli_enhanced.py add-tag 1 "conference"

# Search by tag
python contacts_cli_enhanced.py search-by-tag "work"

# List all tags
python contacts_cli_enhanced.py tags

# List all contacts with metadata
python contacts_cli_enhanced.py list --metadata
```

### Web Application

Start the web server:
```bash
python web_app.py
```

Access the application at: `http://localhost:5000`

#### Web UI Features
- **Modern Interface**: Bootstrap 5 responsive design
- **Contact Cards**: Visual contact display with metadata preview
- **Advanced Search**: Search across name, email, phone, and metadata
- **Tag Filtering**: Filter contacts by tags with visual indicators
- **Pagination**: Handle large contact lists efficiently
- **Form Validation**: Real-time validation and error handling
- **Mobile Responsive**: Works on all device sizes

#### REST API Endpoints

```bash
# Get all contacts (with pagination and filtering)
GET /api/contacts?page=1&per_page=10&search=john&tag=work

# Create new contact
POST /api/contacts
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-555-123-4567",
  "metadata": {
    "birthday": "1990-05-15",
    "company": "Tech Corp",
    "social": {"twitter": "@johndoe"}
  },
  "tags": ["work", "tech"]
}

# Get specific contact
GET /api/contacts/1

# Update contact
PUT /api/contacts/1

# Update metadata only
PATCH /api/contacts/1/metadata
{
  "birthday": "1990-05-15",
  "company": "New Company"
}

# Delete contact
DELETE /api/contacts/1

# Get all tags
GET /api/tags

# Create new tag
POST /api/tags
{
  "name": "new-tag",
  "color": "#ff6b6b"
}
```

### Migration Tool

```bash
# Migrate existing database to enhanced schema
python migration_tool.py --action migrate

# Check migration status
python migration_tool.py --action status

# Create backup
python migration_tool.py --action backup --backup-path my_backup.db
```

## 📊 Database Schema

### Enhanced Schema Design

```sql
-- Contacts table with JSON metadata
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    metadata TEXT DEFAULT '{}',  -- JSON column for flexible metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tags table
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    color TEXT DEFAULT '#007bff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Many-to-many relationship
CREATE TABLE contact_tags (
    contact_id INTEGER,
    tag_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (contact_id, tag_id),
    FOREIGN KEY (contact_id) REFERENCES contacts (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_contacts_email ON contacts (email);
CREATE INDEX idx_contacts_name ON contacts (name);
CREATE INDEX idx_contact_tags_contact ON contact_tags (contact_id);
CREATE INDEX idx_contact_tags_tag ON contact_tags (tag_id);
```

### Metadata Examples

```json
{
  "birthday": "1990-05-15",
  "company": "Tech Corp",
  "position": "Software Engineer",
  "social": {
    "twitter": "@johndoe",
    "linkedin": "linkedin.com/in/johndoe",
    "github": "github.com/johndoe"
  },
  "interests": ["programming", "music", "travel"],
  "notes": "Met at conference 2023",
  "custom_field": "custom_value"
}
```

## 🔧 Configuration

### Environment Variables
```bash
# Flask configuration
export FLASK_ENV=development
export FLASK_DEBUG=1

# Database configuration
export DATABASE_URL=sqlite:///contacts_enhanced.db
```

### Database Configuration
- **Default Database**: `contacts_enhanced.db`
- **Backup Location**: `backup_contacts_YYYYMMDD_HHMMSS.db`
- **Migration Tracking**: `schema_migrations` table

## 🧪 Testing

### CLI Testing
```bash
# Test enhanced CLI functionality
python contacts_cli_enhanced.py load sample_contacts_enhanced.json
python contacts_cli_enhanced.py list --metadata
python contacts_cli_enhanced.py lookup "tech" --metadata
```

### Web UI Testing
```bash
# Start web server
python web_app.py

# Test in browser
open http://localhost:5000
```

### API Testing
```bash
# Test REST API endpoints
curl http://localhost:5000/api/contacts
curl http://localhost:5000/api/tags
```

## 🔒 Security Features

- **Input Validation**: Email format validation and SQL injection prevention
- **Duplicate Prevention**: Unique constraints on emails and tags
- **Error Handling**: Graceful error handling with user-friendly messages
- **Data Integrity**: Foreign key constraints and cascading deletes

## 📈 Performance Optimizations

- **Database Indexes**: Strategic indexing for common queries
- **JSON Path Indexes**: Indexed JSON metadata queries (when JSON1 extension available)
- **Pagination**: Efficient handling of large datasets
- **Lazy Loading**: Optimized relationship loading in web UI

## 🚀 Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements_enhanced.txt

# Run migration
python migration_tool.py --action migrate

# Start web server
python web_app.py
```

### Production Deployment
```bash
# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app

# Set up automated backups
crontab -e
# Add: 0 2 * * * python /path/to/migration_tool.py --action backup
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information
4. Include error messages and system information

## 🔄 Migration from Original

If you have an existing contacts database:

1. **Backup your data**
   ```bash
   cp contacts.db contacts_backup.db
   ```

2. **Run migration**
   ```bash
   python migration_tool.py --action migrate
   ```

3. **Verify migration**
   ```bash
   python migration_tool.py --action status
   ```

4. **Test enhanced features**
   ```bash
   python contacts_cli_enhanced.py list --metadata
   ```

The migration tool will:
- Preserve all existing contact data
- Add metadata column to contacts table
- Create tags and contact_tags tables
- Add performance indexes
- Track migration history

## 🎉 What's New

### Enhanced Features
- ✅ **Normalized Database Schema**: Proper relational design
- ✅ **JSON Metadata Support**: Flexible custom fields
- ✅ **Tags System**: Organize contacts with multiple tags
- ✅ **Web Interface**: Modern, responsive UI
- ✅ **REST API**: Programmatic access
- ✅ **Migration Tool**: Safe schema upgrades
- ✅ **Backup System**: Automated data protection
- ✅ **Advanced Search**: Search across all fields and metadata
- ✅ **Pagination**: Handle large contact lists
- ✅ **Validation**: Input validation and error handling

### Technical Improvements
- ✅ **Performance**: Optimized queries and indexes
- ✅ **Scalability**: Efficient handling of large datasets
- ✅ **Maintainability**: Clean code structure and documentation
- ✅ **Extensibility**: Easy to add new features
- ✅ **Security**: Input validation and SQL injection prevention 