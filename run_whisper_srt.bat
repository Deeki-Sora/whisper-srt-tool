@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
pushd "%~dp0"
if errorlevel 1 exit /b 1

call "%~dp0select_python.bat"
if errorlevel 1 goto :missing

echo [WhisperSRT] Using: "%WHISPERSRT_PYTHON%" %WHISPERSRT_PYTHON_ARGS%
"%WHISPERSRT_PYTHON%" %WHISPERSRT_PYTHON_ARGS% -u "%~dp0whisper_srt_cli.py" %*
set "WHISPERSRT_EXIT=%errorlevel%"
if not "%WHISPERSRT_EXIT%"=="0" echo [WhisperSRT] Failed. See the error above.
goto :finish

:missing
echo [WhisperSRT] Dependencies not ready. Run install_whisper_srt.bat first.
set "WHISPERSRT_EXIT=1"

:finish
popd
if not defined WHISPERSRT_NO_PAUSE pause
exit /b %WHISPERSRT_EXIT%

