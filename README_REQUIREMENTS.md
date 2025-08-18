# Automatic Requirements Installer

This project includes automated scripts to install all Python requirements from multiple `requirements.txt` files across different project directories.

## 📁 Files Created

- `install_requirements.py` - Main Python script that finds and installs all requirements
- `install_requirements.bat` - Windows batch script (for Windows users)
- `install_requirements.sh` - Shell script (for Unix/Linux/macOS users)
- `README_REQUIREMENTS.md` - This documentation file

## 🚀 Quick Start

### Option 1: Using the Python Script Directly

1. **Activate your virtual environment:**
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # Unix/Linux/macOS
   source venv/bin/activate
   ```

2. **Run the installer:**
   ```bash
   python install_requirements.py
   ```

### Option 2: Using Platform-Specific Scripts

#### Windows Users
```bash
# Double-click the file or run in Command Prompt
install_requirements.bat
```

#### Unix/Linux/macOS Users
```bash
# Make the script executable (first time only)
chmod +x install_requirements.sh

# Run the script
./install_requirements.sh
```

## 🔍 What the Script Does

1. **Searches** for all `requirements*.txt` files in the project directory and subdirectories
2. **Lists** all found requirements files
3. **Asks for confirmation** before proceeding
4. **Installs** requirements from each file using `pip install -r <file>`
5. **Provides a summary** of successful and failed installations

## 📋 Requirements Files Found

The script will automatically find and install from these files:

- `Algorithms and Data Structures/Enhanced/requirements_enhanced.txt`
- `Algorithms and Data Structures/flask-algoviz/requirements.txt`
- `Databases/Enhanced/requirements_enhanced.txt`
- `Databases/requirements.txt`
- `Software Design and Engineering/Enhanced/requirements_enhanced.txt`
- `Software Design and Engineering/requirements.txt`

## ⚙️ Features

- ✅ **Automatic discovery** of requirements files
- ✅ **Virtual environment detection** and warning
- ✅ **Error handling** for failed installations
- ✅ **Progress tracking** and detailed output
- ✅ **Cross-platform compatibility**
- ✅ **User confirmation** before installation
- ✅ **Summary report** after completion

## 🛠️ Customization

### Adding New Requirements Files

Simply create new `requirements.txt` files in any subdirectory. The script will automatically find them on the next run.

### Modifying Installation Behavior

Edit `install_requirements.py` to:
- Change the search pattern (currently `requirements*.txt`)
- Add additional pip flags
- Modify the confirmation prompts
- Add custom error handling

## 🔧 Troubleshooting

### Virtual Environment Issues
- Ensure you have a virtual environment created: `python -m venv venv`
- Activate the virtual environment before running the script
- The script will warn you if you're not in a virtual environment

### Permission Issues
- On Unix/Linux/macOS, make the shell script executable: `chmod +x install_requirements.sh`
- Ensure you have write permissions to the project directory

### Installation Failures
- Check the error messages for specific package conflicts
- Some packages may require system-level dependencies
- Try running `pip install --upgrade pip` first

## 📝 Example Output

```
🚀 Automatic Requirements Installer
==================================================

🔍 Searching for requirements files...
📋 Found 6 requirements file(s):
   • Algorithms and Data Structures\Enhanced\requirements_enhanced.txt
   • Algorithms and Data Structures\flask-algoviz\requirements.txt
   • Databases\Enhanced\requirements_enhanced.txt
   • Databases\requirements.txt
   • Software Design and Engineering\Enhanced\requirements_enhanced.txt
   • Software Design and Engineering\requirements.txt

🤔 Ready to install requirements from 6 file(s).
   Proceed with installation? (Y/n): Y

⚙️  Starting installation...

📦 Installing requirements from: Algorithms and Data Structures\Enhanced\requirements_enhanced.txt
   Full path: C:\Users\...\Algorithms and Data Structures\Enhanced\requirements_enhanced.txt
   ✅ Successfully installed requirements from Algorithms and Data Structures\Enhanced\requirements_enhanced.txt

[... more installations ...]

==================================================
📊 Installation Summary:
   ✅ Successful: 6
   ❌ Failed: 0
   📁 Total files processed: 6

🎉 All requirements installed successfully!

💡 Tip: You can run this script anytime to reinstall requirements.
```

## 🔄 Reinstalling Requirements

You can run the script anytime to reinstall all requirements. This is useful when:
- Adding new requirements files
- Updating existing requirements
- Setting up the project on a new machine
- Resolving dependency conflicts

## 📞 Support

If you encounter issues:
1. Check that your virtual environment is activated
2. Ensure all requirements files are valid
3. Try running individual `pip install -r <file>` commands to isolate issues
4. Check the Python and pip versions are compatible
