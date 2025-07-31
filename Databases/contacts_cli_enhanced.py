#!/usr/bin/env python3
"""
Enhanced Contact Management CLI Application
Features:
- Normalized schema with JSON metadata
- Tags system with many-to-many relationships
- Smart CLI commands with JSON field updates
- SQLite JSON1 extension support
"""

import json
import sqlite3
import click
from tabulate import tabulate
from colorama import init, Fore, Style
import os
from datetime import datetime
import re
from typing import Dict, List, Optional, Any

# Initialize colorama for cross-platform colored output
init()

class EnhancedContactManager:
    def __init__(self, db_path="contacts_enhanced.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with normalized schema and JSON support."""
        with sqlite3.connect(self.db_path) as conn:
            # Enable JSON1 extension if available
            try:
                conn.enable_load_extension(True)
                conn.load_extension("json1")
            except (AttributeError, sqlite3.OperationalError):
                # JSON1 extension not available, continue without it
                pass
            
            cursor = conn.cursor()
            
            # Create contacts table with JSON metadata
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    address TEXT,
                    metadata TEXT DEFAULT '{}',  -- JSON column for arbitrary metadata
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create tags table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    color TEXT DEFAULT '#007bff',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create contact_tags junction table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contact_tags (
                    contact_id INTEGER,
                    tag_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (contact_id, tag_id),
                    FOREIGN KEY (contact_id) REFERENCES contacts (id) ON DELETE CASCADE,
                    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts (email)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts (name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_contact_tags_contact ON contact_tags (contact_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_contact_tags_tag ON contact_tags (tag_id)')
            
            # Create JSON path indexes if JSON1 is available
            try:
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_birthday ON contacts (json_extract(metadata, "$.birthday"))')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_social ON contacts (json_extract(metadata, "$.social.twitter"))')
            except sqlite3.OperationalError:
                pass
            
            conn.commit()
    
    def load_from_json(self, json_file):
        """Load contacts from a JSON file with enhanced metadata support."""
        if not os.path.exists(json_file):
            click.echo(f"{Fore.RED}Error: File {json_file} not found.{Style.RESET_ALL}")
            return False
        
        try:
            with open(json_file, 'r') as f:
                contacts = json.load(f)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                loaded_count = 0
                
                for contact in contacts:
                    try:
                        # Extract core fields
                        core_fields = {
                            'name': contact.get('name', ''),
                            'email': contact.get('email', ''),
                            'phone': contact.get('phone', ''),
                            'address': contact.get('address', '')
                        }
                        
                        # Extract metadata (everything else)
                        metadata = {k: v for k, v in contact.items() 
                                  if k not in core_fields and v is not None}
                        
                        # Extract tags if present
                        tags = metadata.pop('tags', [])
                        
                        cursor.execute('''
                            INSERT OR REPLACE INTO contacts (name, email, phone, address, metadata)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (
                            core_fields['name'],
                            core_fields['email'],
                            core_fields['phone'],
                            core_fields['address'],
                            json.dumps(metadata)
                        ))
                        
                        contact_id = cursor.lastrowid
                        
                        # Add tags
                        for tag_name in tags:
                            self._ensure_tag_exists(cursor, tag_name)
                            self._add_contact_tag(cursor, contact_id, tag_name)
                        
                        loaded_count += 1
                        
                    except sqlite3.IntegrityError as e:
                        click.echo(f"{Fore.YELLOW}Warning: Skipping duplicate contact {contact.get('name', 'Unknown')}: {e}{Style.RESET_ALL}")
                
                conn.commit()
                click.echo(f"{Fore.GREEN}Successfully loaded {loaded_count} contacts from {json_file}{Style.RESET_ALL}")
                return True
                
        except json.JSONDecodeError:
            click.echo(f"{Fore.RED}Error: Invalid JSON format in {json_file}{Style.RESET_ALL}")
            return False
        except Exception as e:
            click.echo(f"{Fore.RED}Error loading contacts: {e}{Style.RESET_ALL}")
            return False
    
    def _ensure_tag_exists(self, cursor, tag_name):
        """Ensure a tag exists, create if it doesn't."""
        cursor.execute('INSERT OR IGNORE INTO tags (name) VALUES (?)', (tag_name,))
    
    def _add_contact_tag(self, cursor, contact_id, tag_name):
        """Add a tag to a contact."""
        cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
        tag_id = cursor.fetchone()[0]
        cursor.execute('INSERT OR IGNORE INTO contact_tags (contact_id, tag_id) VALUES (?, ?)', 
                      (contact_id, tag_id))
    
    def lookup_contact(self, search_term, include_metadata=True):
        """Look up contacts by name, email, or metadata."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Try to use JSON1 extension for metadata search
            try:
                cursor.execute('''
                    SELECT c.id, c.name, c.email, c.phone, c.address, 
                           c.metadata, c.created_at, c.updated_at,
                           GROUP_CONCAT(t.name) as tags
                    FROM contacts c
                    LEFT JOIN contact_tags ct ON c.id = ct.contact_id
                    LEFT JOIN tags t ON ct.tag_id = t.id
                    WHERE c.name LIKE ? OR c.email LIKE ? 
                       OR json_extract(c.metadata, '$.birthday') LIKE ?
                       OR json_extract(c.metadata, '$.social.twitter') LIKE ?
                    GROUP BY c.id
                    ORDER BY c.name
                ''', (f'%{search_term}%', f'%{search_term}%', 
                      f'%{search_term}%', f'%{search_term}%'))
            except sqlite3.OperationalError:
                # JSON1 not available, fall back to basic search
                cursor.execute('''
                    SELECT c.id, c.name, c.email, c.phone, c.address, 
                           c.metadata, c.created_at, c.updated_at,
                           GROUP_CONCAT(t.name) as tags
                    FROM contacts c
                    LEFT JOIN contact_tags ct ON c.id = ct.contact_id
                    LEFT JOIN tags t ON ct.tag_id = t.id
                    WHERE c.name LIKE ? OR c.email LIKE ? OR c.metadata LIKE ?
                    GROUP BY c.id
                    ORDER BY c.name
                ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            
            contacts = cursor.fetchall()
            return contacts
    
    def add_contact(self, name, email=None, phone=None, address=None, metadata=None, tags=None):
        """Add a new contact with metadata and tags."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                metadata_json = json.dumps(metadata or {})
                
                cursor.execute('''
                    INSERT INTO contacts (name, email, phone, address, metadata)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, email, phone, address, metadata_json))
                
                contact_id = cursor.lastrowid
                
                # Add tags if provided
                if tags:
                    for tag_name in tags:
                        self._ensure_tag_exists(cursor, tag_name)
                        self._add_contact_tag(cursor, contact_id, tag_name)
                
                conn.commit()
                click.echo(f"{Fore.GREEN}Contact '{name}' added successfully!{Style.RESET_ALL}")
                return True
                
        except sqlite3.IntegrityError:
            click.echo(f"{Fore.RED}Error: Contact with email '{email}' already exists.{Style.RESET_ALL}")
            return False
        except Exception as e:
            click.echo(f"{Fore.RED}Error adding contact: {e}{Style.RESET_ALL}")
            return False
    
    def update_contact_metadata(self, contact_id, metadata_updates):
        """Update specific metadata fields for a contact."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get current metadata
                cursor.execute('SELECT metadata FROM contacts WHERE id = ?', (contact_id,))
                result = cursor.fetchone()
                
                if not result:
                    click.echo(f"{Fore.RED}Error: Contact with ID {contact_id} not found.{Style.RESET_ALL}")
                    return False
                
                current_metadata = json.loads(result[0] or '{}')
                current_metadata.update(metadata_updates)
                
                cursor.execute('''
                    UPDATE contacts 
                    SET metadata = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (json.dumps(current_metadata), contact_id))
                
                conn.commit()
                click.echo(f"{Fore.GREEN}Contact metadata updated successfully!{Style.RESET_ALL}")
                return True
                
        except Exception as e:
            click.echo(f"{Fore.RED}Error updating metadata: {e}{Style.RESET_ALL}")
            return False
    
    def add_tag_to_contact(self, contact_id, tag_name):
        """Add a tag to a specific contact."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                self._ensure_tag_exists(cursor, tag_name)
                self._add_contact_tag(cursor, contact_id, tag_name)
                conn.commit()
                click.echo(f"{Fore.GREEN}Tag '{tag_name}' added to contact successfully!{Style.RESET_ALL}")
                return True
        except Exception as e:
            click.echo(f"{Fore.RED}Error adding tag: {e}{Style.RESET_ALL}")
            return False
    
    def search_by_tag(self, tag_name):
        """Search contacts by tag."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.id, c.name, c.email, c.phone, c.address, 
                       c.metadata, c.created_at, c.updated_at,
                       GROUP_CONCAT(t.name) as tags
                FROM contacts c
                JOIN contact_tags ct ON c.id = ct.contact_id
                JOIN tags tag ON ct.tag_id = tag.id
                LEFT JOIN contact_tags ct2 ON c.id = ct2.contact_id
                LEFT JOIN tags t ON ct2.tag_id = t.id
                WHERE tag.name = ?
                GROUP BY c.id
                ORDER BY c.name
            ''', (tag_name,))
            
            contacts = cursor.fetchall()
            return contacts
    
    def list_tags(self):
        """List all available tags with contact counts."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.name, t.color, COUNT(ct.contact_id) as contact_count
                FROM tags t
                LEFT JOIN contact_tags ct ON t.id = ct.tag_id
                GROUP BY t.id
                ORDER BY t.name
            ''')
            
            tags = cursor.fetchall()
            return tags
    
    def delete_contact(self, contact_id):
        """Delete a contact by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM contacts WHERE id = ?', (contact_id,))
            contact = cursor.fetchone()
            
            if not contact:
                click.echo(f"{Fore.RED}Error: Contact with ID {contact_id} not found.{Style.RESET_ALL}")
                return False
            
            cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
            conn.commit()
            click.echo(f"{Fore.GREEN}Contact '{contact[0]}' deleted successfully!{Style.RESET_ALL}")
            return True
    
    def list_all_contacts(self):
        """List all contacts with tags."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.id, c.name, c.email, c.phone, c.address, 
                       c.metadata, c.created_at, c.updated_at,
                       GROUP_CONCAT(t.name) as tags
                FROM contacts c
                LEFT JOIN contact_tags ct ON c.id = ct.contact_id
                LEFT JOIN tags t ON ct.tag_id = t.id
                GROUP BY c.id
                ORDER BY c.name
            ''')
            contacts = cursor.fetchall()
            return contacts

def display_contacts(contacts, title="Contacts", show_metadata=False):
    """Display contacts in a formatted table with enhanced information."""
    if not contacts:
        click.echo(f"{Fore.YELLOW}No contacts found.{Style.RESET_ALL}")
        return
    
    headers = ["ID", "Name", "Email", "Phone", "Address", "Tags", "Created", "Updated"]
    if show_metadata:
        headers.insert(-2, "Metadata")
    
    table = []
    
    for contact in contacts:
        row = [
            contact[0],
            contact[1],
            contact[2] or "",
            contact[3] or "",
            contact[4] or "",
            contact[8] or "",  # tags
        ]
        
        if show_metadata and contact[5]:
            try:
                metadata = json.loads(contact[5])
                metadata_str = ", ".join([f"{k}: {v}" for k, v in metadata.items()])
                row.append(metadata_str[:50] + "..." if len(metadata_str) > 50 else metadata_str)
            except:
                row.append("")
        
        row.extend([
            contact[6][:10] if contact[6] else "",
            contact[7][:10] if contact[7] else ""
        ])
        
        table.append(row)
    
    click.echo(f"\n{Fore.CYAN}{title}{Style.RESET_ALL}")
    click.echo(tabulate(table, headers=headers, tablefmt="grid"))

def display_tags(tags, title="Available Tags"):
    """Display tags in a formatted table."""
    if not tags:
        click.echo(f"{Fore.YELLOW}No tags found.{Style.RESET_ALL}")
        return
    
    headers = ["Tag Name", "Color", "Contact Count"]
    table = [[tag[0], tag[1], tag[2]] for tag in tags]
    
    click.echo(f"\n{Fore.CYAN}{title}{Style.RESET_ALL}")
    click.echo(tabulate(table, headers=headers, tablefmt="grid"))

@click.group()
@click.option('--db', default='contacts_enhanced.db', help='Database file path')
@click.pass_context
def cli(ctx, db):
    """Enhanced Contact Management CLI Application"""
    ctx.ensure_object(dict)
    ctx.obj['manager'] = EnhancedContactManager(db)

@cli.command()
@click.argument('json_file')
@click.pass_context
def load(ctx, json_file):
    """Load contacts from a JSON file with metadata and tags support."""
    manager = ctx.obj['manager']
    manager.load_from_json(json_file)

@cli.command()
@click.argument('search_term')
@click.option('--metadata', is_flag=True, help='Show metadata in results')
@click.pass_context
def lookup(ctx, search_term, metadata):
    """Look up contacts by name, email, or metadata."""
    manager = ctx.obj['manager']
    contacts = manager.lookup_contact(search_term)
    display_contacts(contacts, f"Search Results for '{search_term}'", show_metadata=metadata)

@cli.command()
@click.option('--name', prompt='Contact name', help='Contact name')
@click.option('--email', help='Contact email')
@click.option('--phone', help='Contact phone number')
@click.option('--address', help='Contact address')
@click.option('--birthday', help='Contact birthday (YYYY-MM-DD)')
@click.option('--twitter', help='Twitter handle')
@click.option('--tags', help='Comma-separated list of tags')
@click.pass_context
def add(ctx, name, email, phone, address, birthday, twitter, tags):
    """Add a new contact with metadata and tags."""
    manager = ctx.obj['manager']
    
    # Build metadata
    metadata = {}
    if birthday:
        metadata['birthday'] = birthday
    if twitter:
        metadata['social'] = {'twitter': twitter}
    
    # Parse tags
    tag_list = [tag.strip() for tag in tags.split(',')] if tags else []
    
    manager.add_contact(name, email, phone, address, metadata, tag_list)

@cli.command()
@click.argument('contact_id', type=int)
@click.option('--birthday', help='Update birthday (YYYY-MM-DD)')
@click.option('--twitter', help='Update Twitter handle')
@click.option('--field', help='Update custom field (format: key=value)')
@click.pass_context
def update_metadata(ctx, contact_id, birthday, twitter, field):
    """Update metadata for a contact."""
    manager = ctx.obj['manager']
    
    metadata_updates = {}
    
    if birthday:
        metadata_updates['birthday'] = birthday
    
    if twitter:
        metadata_updates['social'] = {'twitter': twitter}
    
    if field:
        try:
            key, value = field.split('=', 1)
            metadata_updates[key.strip()] = value.strip()
        except ValueError:
            click.echo(f"{Fore.RED}Error: Field must be in format 'key=value'{Style.RESET_ALL}")
            return
    
    if metadata_updates:
        manager.update_contact_metadata(contact_id, metadata_updates)
    else:
        click.echo(f"{Fore.YELLOW}No metadata updates specified.{Style.RESET_ALL}")

@cli.command()
@click.argument('contact_id', type=int)
@click.argument('tag_name')
@click.pass_context
def add_tag(ctx, contact_id, tag_name):
    """Add a tag to a contact."""
    manager = ctx.obj['manager']
    manager.add_tag_to_contact(contact_id, tag_name)

@cli.command()
@click.argument('tag_name')
@click.pass_context
def search_by_tag(ctx, tag_name):
    """Search contacts by tag."""
    manager = ctx.obj['manager']
    contacts = manager.search_by_tag(tag_name)
    display_contacts(contacts, f"Contacts with tag '{tag_name}'")

@cli.command()
@click.pass_context
def tags(ctx):
    """List all available tags."""
    manager = ctx.obj['manager']
    tags = manager.list_tags()
    display_tags(tags)

@cli.command()
@click.argument('contact_id', type=int)
@click.pass_context
def delete(ctx, contact_id):
    """Delete a contact by ID."""
    manager = ctx.obj['manager']
    manager.delete_contact(contact_id)

@cli.command()
@click.option('--metadata', is_flag=True, help='Show metadata in results')
@click.pass_context
def list(ctx, metadata):
    """List all contacts with tags."""
    manager = ctx.obj['manager']
    contacts = manager.list_all_contacts()
    display_contacts(contacts, "All Contacts", show_metadata=metadata)

if __name__ == '__main__':
    cli() 