@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul

set "PYTHON_EXE="
python check_environment.py --quiet >nul 2>&1
if not errorlevel 1 set "PYTHON_EXE=python"

if not defined PYTHON_EXE if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe check_environment.py --quiet >nul 2>&1
    if not errorlevel 1 set "PYTHON_EXE=.venv\Scripts\python.exe"
)

if not defined PYTHON_EXE (
    echo 鏈娴嬪埌瀹屾暣渚濊禆銆傝鍏堣繍琛?install_whisper_srt.bat銆?    pause
    exit /b 1
)

%PYTHON_EXE% whisper_srt_cli.py %*
if errorlevel 1 (
    echo.
    echo 澶勭悊澶辫触銆傝鏌ョ湅涓婃柟閿欒淇℃伅锛屾垨鍏堣繍琛?install_whisper_srt.bat銆?)
pause

