@echo off
REM Automatic Requirements Installer for Windows
REM This script activates the virtual environment and runs the requirements installer

echo 🚀 Starting Automatic Requirements Installer...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo  Virtual environment not found!
    echo    Please create a virtual environment first by running:
    echo    python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Run the Python installer script
echo.
echo  Running requirements installer...
python install_requirements.py

REM Keep the window open if there was an error
if errorlevel 1 (
    echo.
    echo   Installation completed with errors.
    pause
) else (
    echo.
    echo  Installation completed successfully!
    timeout /t 3 >nul
)
