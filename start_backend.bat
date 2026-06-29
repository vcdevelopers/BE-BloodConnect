@echo off
echo ====================================================================
echo               MumbaiBloodConnect Django Backend Starter             
echo ====================================================================
echo.

cd %~dp0

:: Check if virtual environment exists
if not exist "venv" (
    echo [System] Creating Python virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo [System] Activating virtual environment...
call venv\Scripts\activate

:: Install/Verify requirements
echo [System] Checking dependencies...
pip install -r requirements.txt

:: Run Django Migrations
echo [System] Preparing database migrations...
python manage.py makemigrations api

echo [System] Applying database migrations...
python manage.py migrate

:: Seed the database
echo [System] Seeding database and running initial live scrape...
python api/seed_db.py

:: Run Server
echo.
echo ====================================================================
echo  Backend server is starting at http://127.0.0.1:8000/
echo  Interactive API Documentation is available at http://127.0.0.1:8000/api/
echo  Press Ctrl+C to stop the server.
echo ====================================================================
echo.

python manage.py runserver 127.0.0.1:8000

pause
