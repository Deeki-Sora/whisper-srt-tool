@echo off
setlocal EnableExtensions
cd /d "%~dp0"
chcp 65001 >nul
title WhisperX SRT 瀹夎绋嬪簭

where py >nul 2>nul
if errorlevel 1 (
    echo 鏈壘鍒?Python銆傝瀹夎 Python 3.10 鎴?3.11锛屽苟鍕鹃€?Add Python to PATH銆?    pause
    exit /b 1
)

python check_environment.py --quiet >nul 2>&1
if not errorlevel 1 (
    echo 宸叉娴嬪埌鏈満 Python 鐜鍏峰 WhisperSRT 鎵€闇€渚濊禆锛岃烦杩囪櫄鎷熺幆澧冨畨瑁呫€?    python check_environment.py
    echo.
    echo 鍙互鐩存帴杩愯 run_whisper_srt.bat銆?    pause
    exit /b 0
)

if not exist ".venv\Scripts\python.exe" (
    echo 姝ｅ湪鍒涘缓鏈湴铏氭嫙鐜...
    py -3.11 -m venv .venv
    if errorlevel 1 py -m venv .venv
)
set "PYTHON_EXE=.venv\Scripts\python.exe"
%PYTHON_EXE% -m pip install --upgrade pip

echo 姝ｅ湪瀹夎 WhisperX銆乫aster-whisper 鍜?CUDA 杩愯搴?..
%PYTHON_EXE% -m pip install whisperx faster-whisper nvidia-cublas-cu12 nvidia-cudnn-cu12 nvidia-cuda-runtime-cu12
if errorlevel 1 goto :failed

echo 姝ｅ湪瀹夎 CUDA 鐗?PyTorch锛堢害 3.5 GB锛岃鑰愬績绛夊緟锛?..
%PYTHON_EXE% -m pip install --upgrade --force-reinstall torch==2.8.0 torchaudio==2.8.0 torchvision==0.23.0 --index-url https://download.pytorch.org/whl/cu128
if errorlevel 1 goto :failed

%PYTHON_EXE% check_environment.py
if errorlevel 1 goto :failed
echo.
echo 瀹夎瀹屾垚銆傚弻鍑?run_whisper_srt.bat锛屾垨灏嗘枃浠?鐩綍鎷栧埌璇?bat 涓婅繍琛屻€?pause
exit /b 0

:failed
echo.
echo 瀹夎澶辫触銆傝妫€鏌ョ綉缁滃悗閲嶆柊杩愯鏈剼鏈€?pause
exit /b 1

