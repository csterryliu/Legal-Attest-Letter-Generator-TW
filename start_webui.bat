@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

rem Quick launcher for the Web UI. Tries the vendored PyPDF2 + reportlab
rem (dep/) first for a fully offline, zero-install run; if that fails to
rem load (e.g. Python 3.12+ removed the "imp" module reportlab needs),
rem falls back to a pip-installed reportlab automatically. See README.md.

set PYTHONPATH=%~dp0dep\PyPDF2;%~dp0dep\reportlab\src
python tw-lal-generator-webui.py %*
if errorlevel 1 (
    echo.
    echo [提示] 內建 reportlab 載入失敗，改用系統已安裝的 reportlab 重試...
    echo.
    set PYTHONPATH=%~dp0dep\PyPDF2
    python tw-lal-generator-webui.py %*
)

pause
endlocal
