@echo off

:: Function to check if Chocolatey is installed
:check_chocolatey
where choco >nul 2>nul
if %errorlevel%==0 (
    echo Chocolatey is already installed.
) else (
    echo Chocolatey is not installed. Installing Chocolatey...
    @powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
)

:: Function to check if Python is installed
:check_python
where python >nul 2>nul
if %errorlevel%==0 (
    echo Python is already installed.
) else (
    echo Python is not installed. Installing Python using Chocolatey...
    choco install -y python
)

:: Function to create a virtual environment, install packages, run the script, and delete the environment
:run_script
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing required packages...
pip install requests tqdm

echo Running the script...
python Linux_Downgrader.py

echo Deactivating and removing virtual environment...
call venv\Scripts\deactivate
rmdir /s /q venv

echo Script execution completed.
exit /b 0

:: Main script execution
call :check_chocolatey
call :check_python
call :run_script