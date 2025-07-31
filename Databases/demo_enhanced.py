#!/usr/bin/env python3
"""
Enhanced Contact Management System Demo
This script demonstrates all the enhanced features of the contact management system.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(command, description):
    """Run a command and display the result."""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"Command: {command}")
    print("-" * 60)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Warnings/Errors: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def demo_enhanced_features():
    """Demonstrate all enhanced features."""
    print("🚀 Enhanced Contact Management System Demo")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("contacts_cli_enhanced.py"):
        print("❌ Error: Please run this script from the Databases directory")
        return False
    
    # Step 1: Run migration
    print("\n📋 Step 1: Database Migration")
    success = run_command(
        "python migration_tool.py --action migrate",
        "Migrating database to enhanced schema"
    )
    if not success:
        print("❌ Migration failed")
        return False
    
    # Step 2: Load enhanced sample data
    print("\n📋 Step 2: Load Enhanced Sample Data")
    success = run_command(
        "python contacts_cli_enhanced.py load sample_contacts_enhanced.json",
        "Loading contacts with metadata and tags"
    )
    if not success:
        print("❌ Failed to load sample data")
        return False
    
    # Step 3: Demonstrate CLI features
    print("\n📋 Step 3: Enhanced CLI Features")
    
    # List all contacts with metadata
    run_command(
        "python contacts_cli_enhanced.py list --metadata",
        "List all contacts with metadata display"
    )
    
    # Search with metadata
    run_command(
        "python contacts_cli_enhanced.py lookup tech --metadata",
        "Search for contacts with 'tech' in any field including metadata"
    )
    
    # Show tags
    run_command(
        "python contacts_cli_enhanced.py tags",
        "Display all available tags with contact counts"
    )
    
    # Search by tag
    run_command(
        "python contacts_cli_enhanced.py search-by-tag work",
        "Search contacts by tag 'work'"
    )
    
    # Step 4: Add a new contact with metadata
    print("\n📋 Step 4: Add Contact with Metadata")
    success = run_command(
        'python contacts_cli_enhanced.py add --name "Demo User" --email "demo@example.com" --phone "+1-555-999-8888" --birthday "1995-01-15" --twitter "@demouser" --tags "demo,test,enhanced"',
        "Adding a new contact with metadata and tags"
    )
    
    # Step 5: Update metadata
    print("\n📋 Step 5: Update Metadata")
    run_command(
        'python contacts_cli_enhanced.py update-metadata 1 --field "company=Demo Corp" --field "position=Demo Engineer"',
        "Update metadata for existing contact"
    )
    
    # Step 6: Show final state
    print("\n📋 Step 6: Final State")
    run_command(
        "python contacts_cli_enhanced.py list --metadata",
        "Show final state with all contacts and metadata"
    )
    
    # Step 7: Migration status
    print("\n📋 Step 7: Migration Status")
    run_command(
        "python migration_tool.py --action status",
        "Check migration status"
    )
    
    print("\n" + "="*60)
    print("🎉 Demo completed successfully!")
    print("="*60)
    print("\n📚 Next Steps:")
    print("1. Start the web application: python web_app.py")
    print("2. Open http://localhost:5000 in your browser")
    print("3. Explore the modern web interface")
    print("4. Try the REST API endpoints")
    print("5. Check the README_ENHANCED.md for full documentation")
    
    return True

def demo_web_interface():
    """Demonstrate the web interface."""
    print("\n🌐 Web Interface Demo")
    print("=" * 60)
    print("Starting web server...")
    print("Open http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run(["python", "web_app.py"])
    except KeyboardInterrupt:
        print("\nWeb server stopped.")

def main():
    """Main demo function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Contact Management System Demo")
    parser.add_argument('--web-only', action='store_true', help='Only start the web interface')
    parser.add_argument('--cli-only', action='store_true', help='Only run CLI demo')
    
    args = parser.parse_args()
    
    if args.web_only:
        demo_web_interface()
    elif args.cli_only:
        demo_enhanced_features()
    else:
        # Run full demo
        if demo_enhanced_features():
            print("\n" + "="*60)
            print("Would you like to start the web interface? (y/n): ", end="")
            try:
                response = input().lower().strip()
                if response in ['y', 'yes']:
                    demo_web_interface()
            except KeyboardInterrupt:
                print("\nDemo ended.")

if __name__ == '__main__':
    main() 