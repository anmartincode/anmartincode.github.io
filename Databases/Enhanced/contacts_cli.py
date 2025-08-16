#!/usr/bin/env python3
"""
Contact Management CLI Application
A simple CLI app that reads a JSON file of contacts, loads them into an SQLite database,
and lets you look up, add, and delete contacts.
"""

import json
import sqlite3
import click
from tabulate import tabulate
from colorama import init, Fore, Style
import os
from datetime import datetime

# Initialize colorama for cross-platform colored output
init()

class ContactManager:
    def __init__(self, db_path="contacts.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with the contacts table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def load_from_json(self, json_file):
        """Load contacts from a JSON file into the database."""
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
                        cursor.execute('''
                            INSERT OR REPLACE INTO contacts (name, email, phone, address)
                            VALUES (?, ?, ?, ?)
                        ''', (
                            contact.get('name', ''),
                            contact.get('email', ''),
                            contact.get('phone', ''),
                            contact.get('address', '')
                        ))
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
    
    def lookup_contact(self, search_term):
        """Look up contacts by name or email."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, email, phone, address, created_at, updated_at
                FROM contacts
                WHERE name LIKE ? OR email LIKE ?
                ORDER BY name
            ''', (f'%{search_term}%', f'%{search_term}%'))
            
            contacts = cursor.fetchall()
            return contacts
    
    def add_contact(self, name, email=None, phone=None, address=None):
        """Add a new contact to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO contacts (name, email, phone, address)
                    VALUES (?, ?, ?, ?)
                ''', (name, email, phone, address))
                conn.commit()
                click.echo(f"{Fore.GREEN}Contact '{name}' added successfully!{Style.RESET_ALL}")
                return True
        except sqlite3.IntegrityError:
            click.echo(f"{Fore.RED}Error: Contact with email '{email}' already exists.{Style.RESET_ALL}")
            return False
        except Exception as e:
            click.echo(f"{Fore.RED}Error adding contact: {e}{Style.RESET_ALL}")
            return False
    
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
        """List all contacts in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, email, phone, address, created_at, updated_at
                FROM contacts
                ORDER BY name
            ''')
            contacts = cursor.fetchall()
            return contacts

def display_contacts(contacts, title="Contacts"):
    """Display contacts in a formatted table."""
    if not contacts:
        click.echo(f"{Fore.YELLOW}No contacts found.{Style.RESET_ALL}")
        return
    
    headers = ["ID", "Name", "Email", "Phone", "Address", "Created", "Updated"]
    table = []
    
    for contact in contacts:
        table.append([
            contact[0],
            contact[1],
            contact[2] or "",
            contact[3] or "",
            contact[4] or "",
            contact[5][:10] if contact[5] else "",
            contact[6][:10] if contact[6] else ""
        ])
    
    click.echo(f"\n{Fore.CYAN}{title}{Style.RESET_ALL}")
    click.echo(tabulate(table, headers=headers, tablefmt="grid"))

@click.group()
@click.option('--db', default='contacts.db', help='Database file path')
@click.pass_context
def cli(ctx, db):
    """Contact Management CLI Application"""
    ctx.ensure_object(dict)
    ctx.obj['manager'] = ContactManager(db)

@cli.command()
@click.argument('json_file')
@click.pass_context
def load(ctx, json_file):
    """Load contacts from a JSON file into the database."""
    manager = ctx.obj['manager']
    manager.load_from_json(json_file)

@cli.command()
@click.argument('search_term')
@click.pass_context
def lookup(ctx, search_term):
    """Look up contacts by name or email."""
    manager = ctx.obj['manager']
    contacts = manager.lookup_contact(search_term)
    display_contacts(contacts, f"Search Results for '{search_term}'")

@cli.command()
@click.option('--name', prompt='Contact name', help='Contact name')
@click.option('--email', help='Contact email')
@click.option('--phone', help='Contact phone number')
@click.option('--address', help='Contact address')
@click.pass_context
def add(ctx, name, email, phone, address):
    """Add a new contact."""
    manager = ctx.obj['manager']
    manager.add_contact(name, email, phone, address)

@cli.command()
@click.argument('contact_id', type=int)
@click.pass_context
def delete(ctx, contact_id):
    """Delete a contact by ID."""
    manager = ctx.obj['manager']
    manager.delete_contact(contact_id)

@cli.command()
@click.pass_context
def list(ctx):
    """List all contacts."""
    manager = ctx.obj['manager']
    contacts = manager.list_all_contacts()
    display_contacts(contacts, "All Contacts")

if __name__ == '__main__':
    cli() 