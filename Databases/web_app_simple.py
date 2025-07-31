#!/usr/bin/env python3
"""
Simplified Enhanced Contact Management Web Application
Uses direct SQLite connection instead of SQLAlchemy for compatibility
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import sqlite3
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Database configuration
DB_PATH = 'contacts_enhanced.db'

def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def validate_email(email):
    """Validate email format."""
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_or_create_tag(tag_name):
    """Get existing tag or create new one."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if tag exists
    cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
    result = cursor.fetchone()
    
    if result:
        tag_id = result['id']
    else:
        # Create new tag
        cursor.execute('INSERT INTO tags (name) VALUES (?)', (tag_name,))
        tag_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return tag_id

# REST API Endpoints
@app.route('/api/contacts', methods=['GET'])
def api_get_contacts():
    """Get all contacts with optional filtering and pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    tag = request.args.get('tag', '')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build query
    query = '''
        SELECT c.id, c.name, c.email, c.phone, c.address, 
               c.metadata, c.created_at, c.updated_at,
               GROUP_CONCAT(t.name) as tags
        FROM contacts c
        LEFT JOIN contact_tags ct ON c.id = ct.contact_id
        LEFT JOIN tags t ON ct.tag_id = t.id
    '''
    
    where_conditions = []
    params = []
    
    if search:
        where_conditions.append('(c.name LIKE ? OR c.email LIKE ? OR c.phone LIKE ?)')
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
    
    if tag:
        query += ' JOIN contact_tags ct2 ON c.id = ct2.contact_id JOIN tags tag2 ON ct2.tag_id = tag2.id'
        where_conditions.append('tag2.name = ?')
        params.append(tag)
    
    if where_conditions:
        query += ' WHERE ' + ' AND '.join(where_conditions)
    
    query += ' GROUP BY c.id ORDER BY c.name'
    
    cursor.execute(query, params)
    contacts = cursor.fetchall()
    
    # Apply pagination
    total = len(contacts)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_contacts = contacts[start:end]
    
    # Convert to list of dicts
    result = []
    for contact in paginated_contacts:
        metadata_dict = json.loads(contact['metadata']) if contact['metadata'] else {}
        tags_list = contact['tags'].split(',') if contact['tags'] else []
        
        result.append({
            'id': contact['id'],
            'name': contact['name'],
            'email': contact['email'],
            'phone': contact['phone'],
            'address': contact['address'],
            'metadata': metadata_dict,
            'tags': tags_list,
            'created_at': contact['created_at'],
            'updated_at': contact['updated_at']
        })
    
    conn.close()
    
    return jsonify({
        'contacts': result,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'has_next': end < total,
            'has_prev': page > 1
        }
    })

@app.route('/api/contacts', methods=['POST'])
def api_create_contact():
    """Create a new contact."""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    if data.get('email') and not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check for duplicate email
    if data.get('email'):
        cursor.execute('SELECT id FROM contacts WHERE email = ?', (data['email'],))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Email already exists'}), 409
    
    # Create contact
    cursor.execute('''
        INSERT INTO contacts (name, email, phone, address, metadata)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['name'],
        data.get('email'),
        data.get('phone'),
        data.get('address'),
        json.dumps(data.get('metadata', {}))
    ))
    
    contact_id = cursor.lastrowid
    
    # Add tags
    for tag_name in data.get('tags', []):
        tag_id = get_or_create_tag(tag_name)
        cursor.execute('INSERT OR IGNORE INTO contact_tags (contact_id, tag_id) VALUES (?, ?)', 
                      (contact_id, tag_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'id': contact_id, 'message': 'Contact created successfully'}), 201

@app.route('/api/contacts/<int:contact_id>', methods=['GET'])
def api_get_contact(contact_id):
    """Get a specific contact."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.id, c.name, c.email, c.phone, c.address, 
               c.metadata, c.created_at, c.updated_at,
               GROUP_CONCAT(t.name) as tags
        FROM contacts c
        LEFT JOIN contact_tags ct ON c.id = ct.contact_id
        LEFT JOIN tags t ON ct.tag_id = t.id
        WHERE c.id = ?
        GROUP BY c.id
    ''', (contact_id,))
    
    contact = cursor.fetchone()
    conn.close()
    
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404
    
    metadata_dict = json.loads(contact['metadata']) if contact['metadata'] else {}
    tags_list = contact['tags'].split(',') if contact['tags'] else []
    
    return jsonify({
        'id': contact['id'],
        'name': contact['name'],
        'email': contact['email'],
        'phone': contact['phone'],
        'address': contact['address'],
        'metadata': metadata_dict,
        'tags': tags_list,
        'created_at': contact['created_at'],
        'updated_at': contact['updated_at']
    })

@app.route('/api/tags', methods=['GET'])
def api_get_tags():
    """Get all tags with contact counts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT t.name, t.color, COUNT(ct.contact_id) as contact_count
        FROM tags t
        LEFT JOIN contact_tags ct ON t.id = ct.tag_id
        GROUP BY t.id
        ORDER BY t.name
    ''')
    
    tags = cursor.fetchall()
    conn.close()
    
    result = []
    for tag in tags:
        result.append({
            'name': tag['name'],
            'color': tag['color'],
            'contact_count': tag['contact_count']
        })
    
    return jsonify(result)

# Web UI Routes
@app.route('/')
def index():
    """Main contacts page."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    tag = request.args.get('tag', '')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get contacts
    query = '''
        SELECT c.id, c.name, c.email, c.phone, c.address, 
               c.metadata, c.created_at, c.updated_at,
               GROUP_CONCAT(t.name) as tags
        FROM contacts c
        LEFT JOIN contact_tags ct ON c.id = ct.contact_id
        LEFT JOIN tags t ON ct.tag_id = t.id
    '''
    
    where_conditions = []
    params = []
    
    if search:
        where_conditions.append('(c.name LIKE ? OR c.email LIKE ? OR c.phone LIKE ?)')
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
    
    if tag:
        query += ' JOIN contact_tags ct2 ON c.id = ct2.contact_id JOIN tags tag2 ON ct2.tag_id = tag2.id'
        where_conditions.append('tag2.name = ?')
        params.append(tag)
    
    if where_conditions:
        query += ' WHERE ' + ' AND '.join(where_conditions)
    
    query += ' GROUP BY c.id ORDER BY c.name'
    
    cursor.execute(query, params)
    contacts = cursor.fetchall()
    
    # Get all tags for sidebar
    cursor.execute('SELECT name FROM tags ORDER BY name')
    tags = [row['name'] for row in cursor.fetchall()]
    
    conn.close()
    
    # Apply pagination
    per_page = 10
    total = len(contacts)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_contacts = contacts[start:end]
    
    # Create pagination object
    pagination = {
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': (total + per_page - 1) // per_page,
        'has_next': end < total,
        'has_prev': page > 1,
        'iter_pages': lambda: range(1, (total + per_page - 1) // per_page + 1)
    }
    
    return render_template('index.html', 
                         contacts=paginated_contacts,
                         pagination=pagination,
                         search=search,
                         selected_tag=tag,
                         tags=tags)

@app.route('/contact/new', methods=['GET', 'POST'])
def new_contact():
    """Create new contact form."""
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        tags = request.form.get('tags', '').split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        # Validate
        if not name:
            flash('Name is required', 'error')
            return redirect(url_for('new_contact'))
        
        if email and not validate_email(email):
            flash('Invalid email format', 'error')
            return redirect(url_for('new_contact'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create contact
        cursor.execute('''
            INSERT INTO contacts (name, email, phone, address)
            VALUES (?, ?, ?, ?)
        ''', (name, email, phone, address))
        
        contact_id = cursor.lastrowid
        
        # Add tags
        for tag_name in tags:
            tag_id = get_or_create_tag(tag_name)
            cursor.execute('INSERT OR IGNORE INTO contact_tags (contact_id, tag_id) VALUES (?, ?)', 
                          (contact_id, tag_id))
        
        conn.commit()
        conn.close()
        
        flash('Contact created successfully!', 'success')
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM tags ORDER BY name')
    tags = [row['name'] for row in cursor.fetchall()]
    conn.close()
    
    return render_template('contact_form.html', contact=None, tags=tags)

@app.route('/contact/<int:contact_id>/delete', methods=['POST'])
def delete_contact(contact_id):
    """Delete a contact."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT name FROM contacts WHERE id = ?', (contact_id,))
    contact = cursor.fetchone()
    
    if contact:
        cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
        conn.commit()
        flash(f'Contact "{contact["name"]}" deleted successfully!', 'success')
    else:
        flash('Contact not found', 'error')
    
    conn.close()
    return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 