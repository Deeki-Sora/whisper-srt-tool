# WhisperX 逐词字幕工具

这套脚本把本机音频或视频转换为美式英语逐词时间戳 SRT。字幕输出在源文件同目录，命名为：

    原文件名.word_whisperx.srt

## 首次安装

双击 install_whisper_srt.bat。脚本会先检查当前系统的 Python 环境：

1. 如果系统 Python 已安装 WhisperX、faster-whisper、PyTorch 和 ctranslate2，则直接使用系统环境，不创建虚拟环境，也不会重复安装。
2. 如果系统环境缺少依赖，脚本才会在本目录创建 .venv，并把依赖安装到该虚拟环境。

安装脚本会先检测 PATH 中的 python，其次检测 py -3.11、py -3，最后检测工具自己的 .venv；本机环境已可用时会直接跳过安装，也不要求额外安装 py 启动器。创建新环境建议使用 Python 3.11。首次转录可能需要下载 Whisper 及英语对齐模型。

音频解码需要 ffmpeg.exe 在 PATH 中可用；环境报告会显示检测到的 FFmpeg 路径。CUDA PyTorch 安装包较大，请预留足够的安装与模型缓存空间。

## 使用方式

双击 run_whisper_srt.bat 后按中文提示输入文件或目录；也可以把一个或多个文件/目录拖到 bat 文件上。启动脚本同样会优先选择已具备依赖的系统 Python，只有系统环境不可用时才选择 .venv。

命令行示例：

    run_whisper_srt.bat "E:\Games\lol_guide\讲解.mp4"
    run_whisper_srt.bat "E:\Games\lol_guide\录音目录" --recursive
    run_whisper_srt.bat "E:\Games\lol_guide\录音.flac" --overwrite

支持常见的 wav、flac、mp3、m4a、mp4、mkv、mov、webm、ogg、opus 等格式。默认使用 RTX GPU 做 Whisper 转录，使用 CPU 做强制对齐以降低显存峰值；如果显存充足，可以增加 --align-device cuda。显存不足时将 --batch-size 2 或 --batch-size 1。

程序固定使用 en 识别，并在提示词中要求 American English spelling。逐词时间戳来自 WhisperX 的 forced alignment，时间边界是模型估计值，不能保证每个单词都毫秒级准确。

## BAT 启动故障修复

如果窗口提示 errorlevel、python.exe 的部分字符“不是内部或外部命令”，或者中文乱码，请用本版文件完整替换旧工具：

- 所有 BAT 使用纯 ASCII、无 BOM 和 Windows CRLF 换行，避免 CMD 拆分命令；中文提示由 UTF-8 Python 界面显示。
- .gitattributes 固定 BAT 的 CRLF 换行。使用编辑器修改 BAT 后请保持 CRLF，不要另存为 UTF-16。
- 请同时保留 select_python.bat 和 check_environment.py，它们与两个入口 BAT 放在同一目录。
- 本机已装好依赖时直接双击 run_whisper_srt.bat，无需重新安装或删除原字幕。

在命令行验证启动（不会加载转录模型）：

    run_whisper_srt.bat --help

自动化调用时可先设置 WHISPERSRT_NO_PAUSE=1 以跳过结束时的按键暂停。BAT 的安装状态信息使用英文；实际交互界面及参数说明使用中文。
