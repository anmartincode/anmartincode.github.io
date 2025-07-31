# Contact Management CLI Application

A simple Command Line Interface (CLI) application for managing contacts. The application reads contacts from a JSON file, loads them into an SQLite database, and provides functionality to look up, add, and delete contacts.

## Features

- **Load contacts** from JSON files into SQLite database
- **Look up contacts** by name or email
- **Add new contacts** with name, email, phone, and address
- **Delete contacts** by ID
- **List all contacts** in a formatted table
- **Colored output** for better user experience
- **Error handling** with informative messages

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Make the script executable (optional):**
   ```bash
   chmod +x contacts_cli.py
   ```

## Usage

### Basic Commands

```bash
# Show help
python contacts_cli.py --help

# Load contacts from JSON file
python contacts_cli.py load sample_contacts.json

# List all contacts
python contacts_cli.py list

# Look up contacts by name or email
python contacts_cli.py lookup "John"

# Add a new contact
python contacts_cli.py add --name "New Contact" --email "new@example.com" --phone "+1-555-000-0000"

# Delete a contact by ID
python contacts_cli.py delete 1
```

### Command Options

- `--db DATABASE`: Specify a custom database file path (default: contacts.db)
- `--name NAME`: Contact name (required for add command)
- `--email EMAIL`: Contact email address
- `--phone PHONE`: Contact phone number
- `--address ADDRESS`: Contact address

### Examples

1. **Load sample contacts:**
   ```bash
   python contacts_cli.py load sample_contacts.json
   ```

2. **Search for contacts:**
   ```bash
   python contacts_cli.py lookup "jane"
   python contacts_cli.py lookup "example.com"
   ```

3. **Add a contact interactively:**
   ```bash
   python contacts_cli.py add
   # The command will prompt for name, email, phone, and address
   ```

4. **Add a contact with all details:**
   ```bash
   python contacts_cli.py add --name "Alice Cooper" --email "alice@example.com" --phone "+1-555-111-2222" --address "123 Rock St, Music City, USA"
   ```

## Database Schema

The application creates an SQLite database with the following schema:

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## File Structure

```
.
├── contacts_cli.py          # Main CLI application
├── requirements.txt         # Python dependencies
├── sample_contacts.json     # Sample contact data
├── README.md               # This file
└── contacts.db             # SQLite database (created when first used)
```

## Error Handling

The application includes comprehensive error handling for:
- Invalid JSON files
- Duplicate email addresses
- Non-existent contact IDs
- Database connection issues
- File not found errors

## Future Enhancements

Based on the project plan, future enhancements could include:

1. **Schema Improvements:**
   - Add JSON column for arbitrary metadata
   - Implement tags system with many-to-many relationships
   - Leverage SQLite's JSON1 Extension

2. **CLI Enhancements:**
   - Lookup by tags
   - Update individual JSON fields
   - Advanced search filters

3. **Web UI:**
   - Flask backend with REST API
   - Frontend with paginated contact table
   - Advanced filtering capabilities

4. **Automation & Hardening:**
   - Database migration system
   - Automated backups
   - Input validation and sanitization

## Requirements

- Python 3.6+
- SQLite3 (included with Python)
- Dependencies listed in `requirements.txt`

## License

This project is for educational purposes as part of a database course assignment. 