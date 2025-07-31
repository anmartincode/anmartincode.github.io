#!/usr/bin/env python3
"""
Simple Migration Tool for Enhanced Contact Manager
Handles database schema changes and versioning.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Any

class MigrationManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.migrations_table = "schema_migrations"
        self.init_migrations_table()
    
    def init_migrations_table(self):
        """Initialize the migrations tracking table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    checksum TEXT
                )
            ''')
            conn.commit()
    
    def get_applied_migrations(self) -> List[str]:
        """Get list of applied migration versions."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT version FROM schema_migrations ORDER BY applied_at')
            return [row[0] for row in cursor.fetchall()]
    
    def apply_migration(self, version: str, name: str, sql_commands: List[str], checksum: str = None):
        """Apply a migration."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if migration already applied
            cursor.execute('SELECT version FROM schema_migrations WHERE version = ?', (version,))
            if cursor.fetchone():
                print(f"Migration {version} ({name}) already applied, skipping...")
                return
            
            # Apply migration
            try:
                for command in sql_commands:
                    cursor.execute(command)
                
                # Record migration
                cursor.execute('''
                    INSERT INTO schema_migrations (version, name, checksum)
                    VALUES (?, ?, ?)
                ''', (version, name, checksum))
                
                conn.commit()
                print(f"✓ Applied migration {version} ({name})")
                
            except Exception as e:
                conn.rollback()
                print(f"✗ Failed to apply migration {version} ({name}): {e}")
                raise
    
    def migrate_to_enhanced_schema(self):
        """Migrate from basic schema to enhanced schema."""
        print("Starting migration to enhanced schema...")
        
        # Check if we're migrating from the basic schema
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if basic contacts table exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='contacts'
            """)
            
            if not cursor.fetchone():
                print("No existing contacts table found. Creating new enhanced schema...")
                self.create_enhanced_schema()
                return
            
            # Check if enhanced schema already exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='tags'
            """)
            
            if cursor.fetchone():
                print("Enhanced schema already exists.")
                return
        
        # Migration from basic to enhanced
        migration_commands = [
            # Add metadata column to contacts table
            "ALTER TABLE contacts ADD COLUMN metadata TEXT DEFAULT '{}'",
            
            # Create tags table
            '''CREATE TABLE tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#007bff',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            
            # Create contact_tags junction table
            '''CREATE TABLE contact_tags (
                contact_id INTEGER,
                tag_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (contact_id, tag_id),
                FOREIGN KEY (contact_id) REFERENCES contacts (id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
            )''',
            
            # Create indexes
            "CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts (email)",
            "CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts (name)",
            "CREATE INDEX IF NOT EXISTS idx_contact_tags_contact ON contact_tags (contact_id)",
            "CREATE INDEX IF NOT EXISTS idx_contact_tags_tag ON contact_tags (tag_id)"
        ]
        
        self.apply_migration(
            version="001",
            name="migrate_to_enhanced_schema",
            sql_commands=migration_commands
        )
        
        print("Migration completed successfully!")
    
    def create_enhanced_schema(self):
        """Create the enhanced schema from scratch."""
        print("Creating enhanced schema from scratch...")
        
        migration_commands = [
            # Create contacts table with JSON metadata
            '''CREATE TABLE contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                address TEXT,
                metadata TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            
            # Create tags table
            '''CREATE TABLE tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#007bff',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            
            # Create contact_tags junction table
            '''CREATE TABLE contact_tags (
                contact_id INTEGER,
                tag_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (contact_id, tag_id),
                FOREIGN KEY (contact_id) REFERENCES contacts (id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
            )''',
            
            # Create indexes
            "CREATE INDEX idx_contacts_email ON contacts (email)",
            "CREATE INDEX idx_contacts_name ON contacts (name)",
            "CREATE INDEX idx_contact_tags_contact ON contact_tags (contact_id)",
            "CREATE INDEX idx_contact_tags_tag ON contact_tags (tag_id)"
        ]
        
        self.apply_migration(
            version="001",
            name="create_enhanced_schema",
            sql_commands=migration_commands
        )
        
        print("Enhanced schema created successfully!")
    
    def backup_database(self, backup_path: str = None):
        """Create a backup of the database."""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_contacts_{timestamp}.db"
        
        import shutil
        shutil.copy2(self.db_path, backup_path)
        print(f"Database backed up to: {backup_path}")
        return backup_path
    
    def get_migration_status(self):
        """Get current migration status."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT version, name, applied_at 
                FROM schema_migrations 
                ORDER BY applied_at
            ''')
            migrations = cursor.fetchall()
            
            print("Migration Status:")
            print("=" * 50)
            if migrations:
                for version, name, applied_at in migrations:
                    print(f"✓ {version} - {name} ({applied_at})")
            else:
                print("No migrations applied yet.")
            print("=" * 50)

def main():
    """Main migration function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Contact Manager Migration Tool")
    parser.add_argument('--db', default='contacts_enhanced.db', help='Database file path')
    parser.add_argument('--action', choices=['migrate', 'status', 'backup'], 
                       default='migrate', help='Action to perform')
    parser.add_argument('--backup-path', help='Backup file path')
    
    args = parser.parse_args()
    
    # Create backup before migration
    if args.action == 'migrate':
        manager = MigrationManager(args.db)
        manager.backup_database()
        manager.migrate_to_enhanced_schema()
    elif args.action == 'status':
        manager = MigrationManager(args.db)
        manager.get_migration_status()
    elif args.action == 'backup':
        manager = MigrationManager(args.db)
        manager.backup_database(args.backup_path)

if __name__ == '__main__':
    main() 