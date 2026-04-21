@echo off
echo ==========================================
echo Setting up virtual environment...
echo ==========================================

:: Create a virtual environment
python -m venv .venv

:: Set CONAN_HOME environment variable in the activate script
echo set CONAN_HOME=%CD%\.conan2>>.venv\Scripts\activate.bat

:: Activate the virtual environment
call .venv\Scripts\activate.bat

:: Upgrade pip
python -m pip install --upgrade pip

:: Install the required packages (resolved relative to this script's location)
pip install -r "%~dp0..\requirements.txt"

:: Install pre-commit hooks
pre-commit install

echo "=========================================="
echo "Virtual environment '.venv' is now active."
echo "=========================================="

:: scripts/env/setup.bat
