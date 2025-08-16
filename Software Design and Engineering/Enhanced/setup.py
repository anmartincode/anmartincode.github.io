#!/usr/bin/env python3
"""
Setup script for Enhanced Animal Shelter Management System
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        'logs',
        'models',
        'data',
        'reports',
        'uploads'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")

def setup_config():
    """Set up configuration file"""
    config_file = Path('config.py')
    config_example = Path('config.example.py')
    
    if not config_file.exists():
        if config_example.exists():
            shutil.copy(config_example, config_file)
            print("📝 Created config.py from template")
            print("⚠️  Please edit config.py with your actual configuration values")
        else:
            print("❌ config.example.py not found")
            return False
    else:
        print("📝 config.py already exists")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    requirements_file = Path('requirements_enhanced.txt')
    if requirements_file.exists():
        return run_command(
            f"{sys.executable} -m pip install -r requirements_enhanced.txt",
            "Installing Python dependencies"
        )
    else:
        print("❌ requirements_enhanced.txt not found")
        return False

def check_system_requirements():
    """Check if system requirements are met"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if pip is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
        print("✅ pip is available")
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up Enhanced Animal Shelter Management System")
    print("=" * 60)
    
    # Check system requirements
    if not check_system_requirements():
        print("❌ System requirements not met. Please install Python 3.8+ and pip.")
        sys.exit(1)
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Setup configuration
    print("\n⚙️  Setting up configuration...")
    if not setup_config():
        print("❌ Configuration setup failed")
        sys.exit(1)
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_dependencies():
        print("❌ Dependency installation failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit config.py with your configuration values")
    print("2. Run: python enhanced_app.py")
    print("3. Run: python analytics_dashboard.py")
    print("\n📚 For more information, see README_ENHANCED.md")

if __name__ == "__main__":
    main()
