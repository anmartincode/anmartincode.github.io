#!/usr/bin/env python3
"""
Start script for Enhanced Animal Shelter Management System
Handles port conflicts and provides easy startup options
"""

import os
import sys
import subprocess
import socket
import time
from pathlib import Path

def check_port(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False

def find_available_port(start_port=8080):
    """Find an available port starting from start_port"""
    port = start_port
    while port < start_port + 100:  # Try up to 100 ports
        if check_port(port):
            return port
        port += 1
    return None

def update_config_port(port):
    """Update the port in config.py if it exists"""
    config_file = Path('config.py')
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                content = f.read()
            
            # Update the PORT line
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'PORT = int(os.getenv(' in line:
                    lines[i] = f"    PORT = int(os.getenv('PORT', {port}))"
                    break
            
            with open(config_file, 'w') as f:
                f.write('\n'.join(lines))
            
            print(f"✅ Updated config.py to use port {port}")
            return True
        except Exception as e:
            print(f"⚠️  Could not update config.py: {e}")
            return False
    return False

def start_application():
    """Start the main application"""
    print("🚀 Starting Enhanced Animal Shelter Management System")
    print("=" * 60)
    
    # Check if config.py exists, if not create it
    config_file = Path('config.py')
    if not config_file.exists():
        config_example = Path('config.example.py')
        if config_example.exists():
            import shutil
            shutil.copy(config_example, config_file)
            print("📝 Created config.py from template")
        else:
            print("❌ config.example.py not found. Please run setup.py first.")
            return False
    
    # Find available port
    print("🔍 Checking port availability...")
    default_port = 8080
    available_port = find_available_port(default_port)
    
    if available_port is None:
        print("❌ No available ports found in range 8080-8179")
        return False
    
    if available_port != default_port:
        print(f"⚠️  Port {default_port} is in use, using port {available_port} instead")
        update_config_port(available_port)
    else:
        print(f"✅ Port {available_port} is available")
    
    # Set environment variable for the port
    os.environ['PORT'] = str(available_port)
    
    print(f"\n🌐 Starting application on http://localhost:{available_port}")
    print("📊 Analytics dashboard will be available on http://localhost:8050")
    print("\nPress Ctrl+C to stop the application")
    print("=" * 60)
    
    try:
        # Start the application
        subprocess.run([sys.executable, "enhanced_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Application failed to start: {e}")
        return False
    
    return True

def start_analytics_dashboard():
    """Start the analytics dashboard"""
    print("📊 Starting Analytics Dashboard...")
    print("Make sure the main application is running first!")
    
    try:
        subprocess.run([sys.executable, "analytics_dashboard.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Analytics dashboard stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Analytics dashboard failed to start: {e}")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "dashboard":
            start_analytics_dashboard()
        elif command == "demo":
            print("🎭 Starting Demo...")
            subprocess.run([sys.executable, "demo_enhanced.py"])
        elif command == "setup":
            print("⚙️  Running setup...")
            subprocess.run([sys.executable, "setup.py"])
        elif command == "help":
            print_help()
        else:
            print(f"❌ Unknown command: {command}")
            print_help()
    else:
        start_application()

def print_help():
    """Print help information"""
    print("Enhanced Animal Shelter Management System - Start Script")
    print("=" * 60)
    print("Usage:")
    print("  python start_app.py              - Start main application")
    print("  python start_app.py dashboard    - Start analytics dashboard")
    print("  python start_app.py demo         - Run demo")
    print("  python start_app.py setup        - Run setup")
    print("  python start_app.py help         - Show this help")
    print("\nNote: The analytics dashboard requires the main application to be running.")

if __name__ == "__main__":
    main()
