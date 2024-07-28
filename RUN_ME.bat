@echo off
python3 = %USERPROFILE%\AppData\Local\Microsoft\WindowsApps\python3.exe
:: Function to check if Python3 is installed
python3 -m install venv
:: Function to create a virtual environment, install packages, run the script, and delete the environment
echo Creating virtual environment...
python3 -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing required packages...
pip install requests tqdm pillow

echo Running the script...
python3 "%~dp0Windows_Downgrader.py"
if %errorlevel% neq 0 (
    echo Python script failed with error code %errorlevel%. Exiting...
    call venv\Scripts\deactivate
    rmdir /s /q venv
    pause
    exit /b %errorlevel%
)

echo Deactivating and removing virtual environment...
call venv\Scripts\deactivate
rmdir /s /q venv

echo Script execution completed.

:: Main script execution

pause
exit /b 0