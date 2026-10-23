@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
title WhisperSRT Setup
pushd "%~dp0"
if errorlevel 1 exit /b 1

call "%~dp0select_python.bat"
if errorlevel 1 goto :install
echo [WhisperSRT] Existing environment is ready. No installation needed.
"%WHISPERSRT_PYTHON%" %WHISPERSRT_PYTHON_ARGS% "%~dp0check_environment.py"
set "WHISPERSRT_EXIT=%errorlevel%"
goto :finish

:install
call "%~dp0select_python.bat" --python-only
if errorlevel 1 goto :no_python
if exist "%~dp0.venv\Scripts\python.exe" goto :venv_ready
echo [WhisperSRT] Creating a local virtual environment...
"%WHISPERSRT_PYTHON%" %WHISPERSRT_PYTHON_ARGS% -m venv "%~dp0.venv"
if errorlevel 1 goto :failed

:venv_ready
set "WHISPERSRT_PYTHON=%~dp0.venv\Scripts\python.exe"
set "WHISPERSRT_PYTHON_ARGS="
"%WHISPERSRT_PYTHON%" -m pip install --upgrade pip
if errorlevel 1 goto :failed

echo [WhisperSRT] Installing CUDA PyTorch. The download is large.
"%WHISPERSRT_PYTHON%" -m pip install torch==2.8.0 torchaudio==2.8.0 torchvision==0.23.0 --index-url https://download.pytorch.org/whl/cu128
if errorlevel 1 goto :failed

echo [WhisperSRT] Installing transcription dependencies...
"%WHISPERSRT_PYTHON%" -m pip install whisperx==3.8.6 "transformers<5" faster-whisper==1.2.1 nvidia-cublas-cu12 nvidia-cudnn-cu12 nvidia-cuda-runtime-cu12
if errorlevel 1 goto :failed
"%WHISPERSRT_PYTHON%" "%~dp0check_environment.py"
if errorlevel 1 goto :failed
echo [WhisperSRT] Setup complete. Run run_whisper_srt.bat.
set "WHISPERSRT_EXIT=0"
goto :finish

:no_python
echo [WhisperSRT] Python 3.10-3.12 is required. Install Python 3.11 and add it to PATH.
set "WHISPERSRT_EXIT=1"
goto :finish

:failed
echo [WhisperSRT] Setup failed. Check the error above and retry.
set "WHISPERSRT_EXIT=1"

:finish
popd
if not defined WHISPERSRT_NO_PAUSE pause
exit /b %WHISPERSRT_EXIT%
