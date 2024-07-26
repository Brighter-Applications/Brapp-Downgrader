@echo off


:: Function to check if Chocolatey is installed
:check_chocolatey
where choco >nul 2>nul
if %errorlevel%==0 (
    echo Chocolatey is already installed.
) else (
    echo Chocolatey is not installed or is incompletely installed. Attempting to fix...
    if exist "C:\ProgramData\chocolatey" (
        echo Removing existing Chocolatey directory...
        rmdir /s /q "C:\ProgramData\chocolatey"
    )
    echo Installing Chocolatey...
    @powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    if %errorlevel% neq 0 (
        echo Failed to install Chocolatey. Please resolve the issue manually.
        pause
        exit /b 1
    )
    echo Chocolatey installed successfully. Please close and reopen the terminal to continue.
    echo. > "%FLAG_FILE%"
    echo @echo off > continue.bat
    echo call Downgrade.bat continue >> continue.bat
    start cmd /k continue.bat
    exit /b 0
)

:: Function to check if Python is installed
:check_python
where python >nul 2>nul
if %errorlevel%==0 (
    echo Python is already installed.
) else (
    echo Python is not installed. Installing Python using Chocolatey...
    choco install -y python
    if %errorlevel% neq 0 (
        echo Failed to install Python. Please resolve the issue manually.
        pause
        exit /b 1
    )
)

:: Function to create a virtual environment, install packages, run the script, and delete the environment
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing required packages...
pip install requests tqdm

echo Running the script...
python "%~dp0Windows_Downgrader.py"
if %errorlevel% neq 0 (
    echo Python script failed with error code %errorlevel%. Exiting...
    call venv\Scripts\deactivate
    rmdir /s /q venv
    exit /b %errorlevel%
)

echo Deactivating and removing virtual environment...
call venv\Scripts\deactivate
rmdir /s /q venv

echo Script execution completed.

:: Main script execution

pause
exit /b 0


:: Keep the terminal open
pause