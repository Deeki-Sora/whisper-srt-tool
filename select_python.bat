@echo off
rem Internal helper. The caller provides SETLOCAL.
rem Keep this file ASCII with CRLF line endings.
set "WHISPERSRT_PYTHON="
set "WHISPERSRT_PYTHON_ARGS="
set "WHISPERSRT_CHECK_ARGS=--quiet"
if "%~1"=="--python-only" set "WHISPERSRT_CHECK_ARGS=--quiet --python-only"

call :try_python "python" ""
if defined WHISPERSRT_PYTHON exit /b 0
call :try_python "py" "-3.11"
if defined WHISPERSRT_PYTHON exit /b 0
call :try_python "py" "-3"
if defined WHISPERSRT_PYTHON exit /b 0
call :try_python "%~dp0.venv\Scripts\python.exe" ""
if defined WHISPERSRT_PYTHON exit /b 0
exit /b 1

:try_python
"%~1" %~2 "%~dp0check_environment.py" %WHISPERSRT_CHECK_ARGS% >nul 2>&1
if errorlevel 1 exit /b 0
set "WHISPERSRT_PYTHON=%~1"
set "WHISPERSRT_PYTHON_ARGS=%~2"
exit /b 0
