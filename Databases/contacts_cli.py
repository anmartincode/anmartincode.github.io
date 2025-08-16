#!/usr/bin/env python3
"""
Enhanced Contact Management CLI Application
A comprehensive CLI app that reads a JSON file of contacts, loads them into an SQLite database,
and provides advanced features including analytics, backup/restore, and performance monitoring.
"""

import json
import sqlite3
import click
from tabulate import tabulate
from colorama import init, Fore, Style
import os
from datetime import datetime
import csv
import time
import hashlib
import shutil
from collections import defaultdict, Counter

# Initialize colorama for cross-platform colored output
init()

class ContactManager:
    def __init__(self, db_path="contacts.db"):
        self.db_path = db_path
        self.init_database()
        self.performance_stats = {
            'queries_executed': 0,
            'total_query_time': 0,
            'slow_queries': []
        }
    
    def init_database(self):
        """Initialize the SQLite database with the contacts table and indexes."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create contacts table with enhanced schema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    address TEXT,
                    company TEXT,
                    job_title TEXT,
                    notes TEXT,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts(name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_company ON contacts(company)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_created_at ON contacts(created_at)')
            
            # Create triggers for updated_at timestamp
            cursor.execute('''
                CREATE TRIGGER IF NOT EXISTS update_contacts_timestamp 
                AFTER UPDATE ON contacts
                BEGIN
                    UPDATE contacts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
                END
            ''')
            
            conn.commit()
    
    def _measure_performance(self, func):
        """Decorator to measure query performance"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            query_time = end_time - start_time
            self.performance_stats['queries_executed'] += 1
            self.performance_stats['total_query_time'] += query_time
            
            if query_time > 0.1:  # Log slow queries (>100ms)
                self.performance_stats['slow_queries'].append({
                    'function': func.__name__,
                    'time': query_time,
                    'timestamp': datetime.now()
                })
            
            return result
        return wrapper
    
    @_measure_performance
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
                            INSERT OR REPLACE INTO contacts 
                            (name, email, phone, address, company, job_title, notes, tags)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            contact.get('name', ''),
                            contact.get('email', ''),
                            contact.get('phone', ''),
                            contact.get('address', ''),
                            contact.get('company', ''),
                            contact.get('job_title', ''),
                            contact.get('notes', ''),
                            contact.get('tags', '')
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
    
    @_measure_performance
    def lookup_contact(self, search_term):
        """Look up contacts by name, email, company, or tags."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, email, phone, address, company, job_title, notes, tags, created_at, updated_at
                FROM contacts
                WHERE name LIKE ? OR email LIKE ? OR company LIKE ? OR tags LIKE ?
                ORDER BY name
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            
            contacts = cursor.fetchall()
            return contacts
    
    @_measure_performance
    def add_contact(self, name, email=None, phone=None, address=None, company=None, job_title=None, notes=None, tags=None):
        """Add a new contact to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO contacts (name, email, phone, address, company, job_title, notes, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, email, phone, address, company, job_title, notes, tags))
                conn.commit()
                click.echo(f"{Fore.GREEN}Contact '{name}' added successfully!{Style.RESET_ALL}")
                return True
        except sqlite3.IntegrityError:
            click.echo(f"{Fore.RED}Error: Contact with email '{email}' already exists.{Style.RESET_ALL}")
            return False
        except Exception as e:
            click.echo(f"{Fore.RED}Error adding contact: {e}{Style.RESET_ALL}")
            return False
    
    @_measure_performance
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
    
    @_measure_performance
    def list_all_contacts(self):
        """List all contacts in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, email, phone, address, company, job_title, notes, tags, created_at, updated_at
                FROM contacts
                ORDER BY name
            ''')
            contacts = cursor.fetchall()
            return contacts
    
    @_measure_performance
    def update_contact(self, contact_id, **kwargs):
        """Update a contact by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if contact exists
                cursor.execute('SELECT name FROM contacts WHERE id = ?', (contact_id,))
                contact = cursor.fetchone()
                
                if not contact:
                    click.echo(f"{Fore.RED}Error: Contact with ID {contact_id} not found.{Style.RESET_ALL}")
                    return False
                
                # Build update query dynamically
                valid_fields = ['name', 'email', 'phone', 'address', 'company', 'job_title', 'notes', 'tags']
                update_fields = []
                values = []
                
                for field, value in kwargs.items():
                    if field in valid_fields and value is not None:
                        update_fields.append(f"{field} = ?")
                        values.append(value)
                
                if not update_fields:
                    click.echo(f"{Fore.YELLOW}No valid fields to update.{Style.RESET_ALL}")
                    return False
                
                values.append(contact_id)
                query = f"UPDATE contacts SET {', '.join(update_fields)} WHERE id = ?"
                
                cursor.execute(query, values)
                conn.commit()
                
                click.echo(f"{Fore.GREEN}Contact '{contact[0]}' updated successfully!{Style.RESET_ALL}")
                return True
                
        except sqlite3.IntegrityError as e:
            click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            click.echo(f"{Fore.RED}Error updating contact: {e}{Style.RESET_ALL}")
            return False
    
    def export_contacts(self, format='csv', filename=None):
        """Export contacts to CSV or JSON format."""
        contacts = self.list_all_contacts()
        
        if not contacts:
            click.echo(f"{Fore.YELLOW}No contacts to export.{Style.RESET_ALL}")
            return False
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"contacts_export_{timestamp}.{format}"
        
        try:
            if format.lower() == 'csv':
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    headers = ["ID", "Name", "Email", "Phone", "Address", "Company", "Job Title", "Notes", "Tags", "Created", "Updated"]
                    writer = csv.writer(csvfile)
                    writer.writerow(headers)
                    
                    for contact in contacts:
                        writer.writerow([
                            contact[0], contact[1], contact[2] or "", contact[3] or "",
                            contact[4] or "", contact[5] or "", contact[6] or "",
                            contact[7] or "", contact[8] or "", contact[9][:10] if contact[9] else "",
                            contact[10][:10] if contact[10] else ""
                        ])
            
            elif format.lower() == 'json':
                contacts_data = []
                for contact in contacts:
                    contacts_data.append({
                        'id': contact[0],
                        'name': contact[1],
                        'email': contact[2],
                        'phone': contact[3],
                        'address': contact[4],
                        'company': contact[5],
                        'job_title': contact[6],
                        'notes': contact[7],
                        'tags': contact[8],
                        'created_at': contact[9],
                        'updated_at': contact[10]
                    })
                
                with open(filename, 'w', encoding='utf-8') as jsonfile:
                    json.dump(contacts_data, jsonfile, indent=2, default=str)
            
            click.echo(f"{Fore.GREEN}Contacts exported to {filename}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            click.echo(f"{Fore.RED}Error exporting contacts: {e}{Style.RESET_ALL}")
            return False
    
    def backup_database(self, backup_path=None):
        """Create a backup of the database."""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"contacts_backup_{timestamp}.db"
        
        try:
            shutil.copy2(self.db_path, backup_path)
            click.echo(f"{Fore.GREEN}Database backed up to {backup_path}{Style.RESET_ALL}")
            return True
        except Exception as e:
            click.echo(f"{Fore.RED}Error backing up database: {e}{Style.RESET_ALL}")
            return False
    
    def restore_database(self, backup_path):
        """Restore database from backup."""
        if not os.path.exists(backup_path):
            click.echo(f"{Fore.RED}Error: Backup file {backup_path} not found.{Style.RESET_ALL}")
            return False
        
        try:
            # Create a backup of current database before restoring
            current_backup = f"contacts_pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy2(self.db_path, current_backup)
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            
            click.echo(f"{Fore.GREEN}Database restored from {backup_path}{Style.RESET_ALL}")
            click.echo(f"{Fore.YELLOW}Previous database backed up to {current_backup}{Style.RESET_ALL}")
            return True
        except Exception as e:
            click.echo(f"{Fore.RED}Error restoring database: {e}{Style.RESET_ALL}")
            return False
    
    def get_analytics(self):
        """Get analytics about contacts."""
        contacts = self.list_all_contacts()
        
        if not contacts:
            return {
                'total_contacts': 0,
                'companies': {},
                'tags': {},
                'recent_activity': [],
                'email_domains': {}
            }
        
        analytics = {
            'total_contacts': len(contacts),
            'companies': Counter(),
            'tags': Counter(),
            'recent_activity': [],
            'email_domains': Counter()
        }
        
        for contact in contacts:
            # Company statistics
            if contact[5]:  # company
                analytics['companies'][contact[5]] += 1
            
            # Tags statistics
            if contact[8]:  # tags
                tags = [tag.strip() for tag in contact[8].split(',') if tag.strip()]
                for tag in tags:
                    analytics['tags'][tag] += 1
            
            # Email domain statistics
            if contact[2]:  # email
                domain = contact[2].split('@')[-1] if '@' in contact[2] else 'unknown'
                analytics['email_domains'][domain] += 1
            
            # Recent activity (contacts created in last 30 days)
            if contact[9]:  # created_at
                created_date = datetime.strptime(contact[9][:10], '%Y-%m-%d')
                if (datetime.now() - created_date).days <= 30:
                    analytics['recent_activity'].append({
                        'name': contact[1],
                        'created_at': contact[9],
                        'company': contact[5]
                    })
        
        return analytics
    
    def get_performance_stats(self):
        """Get performance statistics."""
        avg_query_time = (self.performance_stats['total_query_time'] / 
                         self.performance_stats['queries_executed'] 
                         if self.performance_stats['queries_executed'] > 0 else 0)
        
        return {
            'queries_executed': self.performance_stats['queries_executed'],
            'average_query_time': avg_query_time,
            'total_query_time': self.performance_stats['total_query_time'],
            'slow_queries_count': len(self.performance_stats['slow_queries']),
            'slow_queries': self.performance_stats['slow_queries'][-5:]  # Last 5 slow queries
        }

def display_contacts(contacts, title="Contacts"):
    """Display contacts in a formatted table."""
    if not contacts:
        click.echo(f"{Fore.YELLOW}No contacts found.{Style.RESET_ALL}")
        return
    
    headers = ["ID", "Name", "Email", "Phone", "Company", "Job Title", "Tags", "Created"]
    table = []
    
    for contact in contacts:
        table.append([
            contact[0],
            contact[1],
            contact[2] or "",
            contact[3] or "",
            contact[5] or "",
            contact[6] or "",
            contact[8] or "",
            contact[9][:10] if contact[9] else ""
        ])
    
    click.echo(f"\n{Fore.CYAN}{title}{Style.RESET_ALL}")
    click.echo(tabulate(table, headers=headers, tablefmt="grid"))

def display_analytics(analytics):
    """Display analytics in a formatted way."""
    click.echo(f"\n{Fore.CYAN}Contact Analytics{Style.RESET_ALL}")
    click.echo("=" * 50)
    
    click.echo(f"Total Contacts: {analytics['total_contacts']}")
    
    if analytics['companies']:
        click.echo(f"\n{Fore.YELLOW}Top Companies:{Style.RESET_ALL}")
        for company, count in analytics['companies'].most_common(5):
            click.echo(f"  {company}: {count}")
    
    if analytics['tags']:
        click.echo(f"\n{Fore.YELLOW}Popular Tags:{Style.RESET_ALL}")
        for tag, count in analytics['tags'].most_common(5):
            click.echo(f"  {tag}: {count}")
    
    if analytics['email_domains']:
        click.echo(f"\n{Fore.YELLOW}Email Domains:{Style.RESET_ALL}")
        for domain, count in analytics['email_domains'].most_common(5):
            click.echo(f"  {domain}: {count}")
    
    if analytics['recent_activity']:
        click.echo(f"\n{Fore.YELLOW}Recent Activity (Last 30 days):{Style.RESET_ALL}")
        for activity in analytics['recent_activity'][:5]:
            click.echo(f"  {activity['name']} ({activity['company']}) - {activity['created_at'][:10]}")

@click.group()
@click.option('--db', default='contacts.db', help='Database file path')
@click.pass_context
def cli(ctx, db):
    """Enhanced Contact Management CLI Application"""
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
    """Look up contacts by name, email, company, or tags."""
    manager = ctx.obj['manager']
    contacts = manager.lookup_contact(search_term)
    display_contacts(contacts, f"Search Results for '{search_term}'")

@cli.command()
@click.option('--name', prompt='Contact name', help='Contact name')
@click.option('--email', help='Contact email')
@click.option('--phone', help='Contact phone number')
@click.option('--address', help='Contact address')
@click.option('--company', help='Contact company')
@click.option('--job-title', help='Contact job title')
@click.option('--notes', help='Contact notes')
@click.option('--tags', help='Contact tags (comma-separated)')
@click.pass_context
def add(ctx, name, email, phone, address, company, job_title, notes, tags):
    """Add a new contact."""
    manager = ctx.obj['manager']
    manager.add_contact(name, email, phone, address, company, job_title, notes, tags)

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

@cli.command()
@click.argument('contact_id', type=int)
@click.option('--name', help='New name')
@click.option('--email', help='New email')
@click.option('--phone', help='New phone')
@click.option('--address', help='New address')
@click.option('--company', help='New company')
@click.option('--job-title', help='New job title')
@click.option('--notes', help='New notes')
@click.option('--tags', help='New tags')
@click.pass_context
def update(ctx, contact_id, name, email, phone, address, company, job_title, notes, tags):
    """Update a contact by ID."""
    manager = ctx.obj['manager']
    update_data = {}
    
    if name:
        update_data['name'] = name
    if email:
        update_data['email'] = email
    if phone:
        update_data['phone'] = phone
    if address:
        update_data['address'] = address
    if company:
        update_data['company'] = company
    if job_title:
        update_data['job_title'] = job_title
    if notes:
        update_data['notes'] = notes
    if tags:
        update_data['tags'] = tags
    
    if update_data:
        manager.update_contact(contact_id, **update_data)
    else:
        click.echo(f"{Fore.YELLOW}No fields specified for update.{Style.RESET_ALL}")

@cli.command()
@click.option('--format', default='csv', type=click.Choice(['csv', 'json']), help='Export format')
@click.option('--filename', help='Output filename')
@click.pass_context
def export(ctx, format, filename):
    """Export contacts to CSV or JSON format."""
    manager = ctx.obj['manager']
    manager.export_contacts(format, filename)

@cli.command()
@click.option('--backup-path', help='Backup file path')
@click.pass_context
def backup(ctx, backup_path):
    """Create a backup of the database."""
    manager = ctx.obj['manager']
    manager.backup_database(backup_path)

@cli.command()
@click.argument('backup_path')
@click.pass_context
def restore(ctx, backup_path):
    """Restore database from backup."""
    manager = ctx.obj['manager']
    manager.restore_database(backup_path)

@cli.command()
@click.pass_context
def analytics(ctx):
    """Show contact analytics."""
    manager = ctx.obj['manager']
    analytics_data = manager.get_analytics()
    display_analytics(analytics_data)

@cli.command()
@click.pass_context
def stats(ctx):
    """Show performance statistics."""
    manager = ctx.obj['manager']
    stats_data = manager.get_performance_stats()
    
    click.echo(f"\n{Fore.CYAN}Performance Statistics{Style.RESET_ALL}")
    click.echo("=" * 50)
    click.echo(f"Queries Executed: {stats_data['queries_executed']}")
    click.echo(f"Average Query Time: {stats_data['average_query_time']:.4f} seconds")
    click.echo(f"Total Query Time: {stats_data['total_query_time']:.4f} seconds")
    click.echo(f"Slow Queries: {stats_data['slow_queries_count']}")
    
    if stats_data['slow_queries']:
        click.echo(f"\n{Fore.YELLOW}Recent Slow Queries:{Style.RESET_ALL}")
        for query in stats_data['slow_queries']:
            click.echo(f"  {query['function']}: {query['time']:.4f}s at {query['timestamp']}")

if __name__ == '__main__':
    cli() 