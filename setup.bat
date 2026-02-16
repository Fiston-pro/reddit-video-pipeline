@echo off
echo ========================================
echo  Reddit Video Generator - Setup
echo ========================================
echo.

:: Check if venv exists
if exist "venv\" (
    echo Virtual environment already exists.
    echo.
) else (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

:: Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

:: Fix imageio-ffmpeg if needed
echo.
echo Fixing imageio-ffmpeg...
pip uninstall imageio-ffmpeg -y
pip install imageio-ffmpeg>=0.5.0

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Test AI enhancement: python test_ai_enhancement.py
echo 2. Generate video: python src\generators\video_generator.py e6dd307b-caa4-4de7-bbb0-6fd650c2a32a
echo.
echo Virtual environment is now activated.
echo To activate it again later: venv\Scripts\activate.bat
echo.
pause
