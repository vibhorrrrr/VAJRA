@echo off
echo Starting VAJRA CLI Legal Assistant...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Run setup first
echo Running setup...
python setup_cli.py
if errorlevel 1 (
    echo Setup failed. Please check the errors above.
    pause
    exit /b 1
)

echo.
echo Starting VAJRA...
python run_cli.py

pause