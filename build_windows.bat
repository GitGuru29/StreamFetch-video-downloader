@echo off
rem Activate virtual environment if needed
call venv\Scripts\activate.bat

pyinstaller --noconfirm --clean --onefile --windowed ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --hidden-import "engineio.async_drivers.threading" ^
    --name "StreamFetch" ^
    desktop_app.py
