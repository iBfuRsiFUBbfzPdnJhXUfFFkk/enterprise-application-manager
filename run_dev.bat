@echo off
REM Local development server runner for Enterprise Application Manager (Windows)

REM Set Django settings to local environment
set DJANGO_SETTINGS_MODULE=core.settings.local

REM Check if virtual environment exists
if not exist ".venv" (
    echo Error: Virtual environment not found at .venv/
    echo Please create the virtual environment first.
    exit /b 1
)

REM Clean Python bytecode cache
echo Cleaning Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc >nul 2>&1

REM Run the development server
echo Starting Django development server...
echo Settings: %DJANGO_SETTINGS_MODULE%
echo Access the application at: http://127.0.0.1:50478
echo.

.venv\Scripts\python.exe manage.py runserver 50478
