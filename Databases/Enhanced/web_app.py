#!/usr/bin/env python3
"""
Enhanced Contact Management Web Application
Features:
- REST API endpoints for CRUD operations
- Web UI with pagination and advanced filtering
- JSON metadata support
- Tags system integration
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
import re
from typing import Dict, List, Optional, Any

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts_enhanced.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    metadata = db.Column(db.Text, default='{}')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with tags
    tags = db.relationship('Tag', secondary='contact_tags', backref=db.backref('contacts', lazy='dynamic'))
    
    def to_dict(self):
        """Convert contact to dictionary with metadata and tags."""
        metadata_dict = json.loads(self.metadata) if self.metadata else {}
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'metadata': metadata_dict,
            'tags': [tag.name for tag in self.tags],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(7), default='#007bff')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Junction table for many-to-many relationship
contact_tags = db.Table('contact_tags',
    db.Column('contact_id', db.Integer, db.ForeignKey('contacts.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

# Utility functions
def validate_email(email):
    """Validate email format."""
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_or_create_tag(tag_name):
    """Get existing tag or create new one."""
    tag = Tag.query.filter_by(name=tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.session.add(tag)
        db.session.commit()
    return tag

# REST API Endpoints
@app.route('/api/contacts', methods=['GET'])
def api_get_contacts():
    """Get all contacts with optional filtering and pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    tag = request.args.get('tag', '')
    
    query = Contact.query
    
    # Apply search filter
    if search:
        query = query.filter(
            db.or_(
                Contact.name.ilike(f'%{search}%'),
                Contact.email.ilike(f'%{search}%'),
                Contact.phone.ilike(f'%{search}%')
            )
        )
    
    # Apply tag filter
    if tag:
        query = query.join(Contact.tags).filter(Tag.name == tag)
    
    # Apply pagination
    pagination = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    contacts = [contact.to_dict() for contact in pagination.items]
    
    return jsonify({
        'contacts': contacts,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
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
    
    # Check for duplicate email
    if data.get('email') and Contact.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409
    
    # Create contact
    contact = Contact(
        name=data['name'],
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address'),
        metadata=json.dumps(data.get('metadata', {}))
    )
    
    # Add tags
    for tag_name in data.get('tags', []):
        tag = get_or_create_tag(tag_name)
        contact.tags.append(tag)
    
    db.session.add(contact)
    db.session.commit()
    
    return jsonify(contact.to_dict()), 201

@app.route('/api/contacts/<int:contact_id>', methods=['GET'])
def api_get_contact(contact_id):
    """Get a specific contact."""
    contact = Contact.query.get_or_404(contact_id)
    return jsonify(contact.to_dict())

@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def api_update_contact(contact_id):
    """Update a contact."""
    contact = Contact.query.get_or_404(contact_id)
    data = request.get_json()
    
    # Validate email if provided
    if data.get('email') and not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Check for duplicate email (excluding current contact)
    if data.get('email'):
        existing = Contact.query.filter_by(email=data['email']).first()
        if existing and existing.id != contact_id:
            return jsonify({'error': 'Email already exists'}), 409
    
    # Update fields
    if 'name' in data:
        contact.name = data['name']
    if 'email' in data:
        contact.email = data['email']
    if 'phone' in data:
        contact.phone = data['phone']
    if 'address' in data:
        contact.address = data['address']
    if 'metadata' in data:
        contact.metadata = json.dumps(data['metadata'])
    
    # Update tags
    if 'tags' in data:
        contact.tags.clear()
        for tag_name in data['tags']:
            tag = get_or_create_tag(tag_name)
            contact.tags.append(tag)
    
    db.session.commit()
    return jsonify(contact.to_dict())

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def api_delete_contact(contact_id):
    """Delete a contact."""
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return '', 204

@app.route('/api/contacts/<int:contact_id>/metadata', methods=['PATCH'])
def api_update_metadata(contact_id):
    """Update specific metadata fields for a contact."""
    contact = Contact.query.get_or_404(contact_id)
    data = request.get_json()
    
    current_metadata = json.loads(contact.metadata) if contact.metadata else {}
    current_metadata.update(data)
    contact.metadata = json.dumps(current_metadata)
    
    db.session.commit()
    return jsonify(contact.to_dict())

@app.route('/api/tags', methods=['GET'])
def api_get_tags():
    """Get all tags with contact counts."""
    tags = Tag.query.all()
    result = []
    
    for tag in tags:
        tag_dict = tag.to_dict()
        tag_dict['contact_count'] = len(tag.contacts)
        result.append(tag_dict)
    
    return jsonify(result)

@app.route('/api/tags', methods=['POST'])
def api_create_tag():
    """Create a new tag."""
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Tag name is required'}), 400
    
    if Tag.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Tag already exists'}), 409
    
    tag = Tag(
        name=data['name'],
        color=data.get('color', '#007bff')
    )
    
    db.session.add(tag)
    db.session.commit()
    
    return jsonify(tag.to_dict()), 201

# Web UI Routes
@app.route('/')
def index():
    """Main contacts page."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    tag = request.args.get('tag', '')
    
    query = Contact.query
    
    if search:
        query = query.filter(
            db.or_(
                Contact.name.ilike(f'%{search}%'),
                Contact.email.ilike(f'%{search}%'),
                Contact.phone.ilike(f'%{search}%')
            )
        )
    
    if tag:
        query = query.join(Contact.tags).filter(Tag.name == tag)
    
    pagination = query.paginate(
        page=page, per_page=10, error_out=False
    )
    
    tags = Tag.query.all()
    
    return render_template('index.html', 
                         contacts=pagination.items,
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
        
        # Create contact
        contact = Contact(
            name=name,
            email=email,
            phone=phone,
            address=address
        )
        
        # Add tags
        for tag_name in tags:
            tag = get_or_create_tag(tag_name)
            contact.tags.append(tag)
        
        db.session.add(contact)
        db.session.commit()
        
        flash('Contact created successfully!', 'success')
        return redirect(url_for('index'))
    
    tags = Tag.query.all()
    return render_template('contact_form.html', contact=None, tags=tags)

@app.route('/contact/<int:contact_id>/edit', methods=['GET', 'POST'])
def edit_contact(contact_id):
    """Edit contact form."""
    contact = Contact.query.get_or_404(contact_id)
    
    if request.method == 'POST':
        # Handle form submission
        contact.name = request.form.get('name')
        contact.email = request.form.get('email')
        contact.phone = request.form.get('phone')
        contact.address = request.form.get('address')
        
        # Update tags
        tags = request.form.get('tags', '').split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]
        contact.tags.clear()
        for tag_name in tags:
            tag = get_or_create_tag(tag_name)
            contact.tags.append(tag)
        
        db.session.commit()
        
        flash('Contact updated successfully!', 'success')
        return redirect(url_for('index'))
    
    tags = Tag.query.all()
    return render_template('contact_form.html', contact=contact, tags=tags)

@app.route('/contact/<int:contact_id>/delete', methods=['POST'])
def delete_contact(contact_id):
    """Delete a contact."""
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000) 