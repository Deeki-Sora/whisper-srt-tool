"""Chinese command-line frontend for the reusable WhisperX SRT backend."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from whisper_srt_backend import WhisperSRTProcessor, iter_audio_files, output_path_for


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="将本机音频/视频转为美式英语逐词时间戳 SRT，字幕写入源文件同目录。"
    )
    parser.add_argument("paths", nargs="*", help="文件或目录；路径含空格时请加引号")
    parser.add_argument("-r", "--recursive", action="store_true", help="目录模式下递归扫描子目录")
    parser.add_argument("--overwrite", action="store_true", help="覆盖已有同名字幕")
    parser.add_argument("--device", choices=("auto", "cuda", "cpu"), default="auto", help="ASR 设备，默认自动选择")
    parser.add_argument("--align-device", choices=("auto", "cuda", "cpu"), default="cpu", help="强制对齐设备，默认 CPU 以节省显存")
    parser.add_argument("--batch-size", type=int, default=4, help="GPU 批大小，显存不足时调小")
    parser.add_argument("--model", default="large-v3", help="Whisper 模型名，默认 large-v3")
    return parser


def interactive_paths() -> list[str]:
    print("请输入要转换的文件或目录。可以输入多个路径，用分号分隔；直接回车退出。")
    raw = input("路径：").strip()
    if not raw:
        return []
    if ";" in raw:
        return [part.strip().strip('"') for part in raw.split(";") if part.strip()]
    # Pasted Windows paths can contain spaces without being quoted.
    return [raw.strip('"')]


def main() -> int:
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args()
    raw_paths = args.paths or interactive_paths()
    if not raw_paths:
        print("未指定路径，程序结束。")
        return 0

    files: list[Path] = []
    for raw in raw_paths:
        try:
            files.extend(iter_audio_files(Path(raw.strip('"')), recursive=args.recursive))
        except (FileNotFoundError, ValueError) as exc:
            print(f"跳过：{exc}")
    files = list(dict.fromkeys(files))
    if not files:
        print("没有找到可处理的音频/视频文件。")
        return 1

    if not args.overwrite:
        existing = [p for p in files if output_path_for(p).exists()]
        if existing:
            answer = input(f"发现 {len(existing)} 个已有字幕，是否覆盖？(y/N)：").strip().lower()
            if answer in {"y", "yes"}:
                args.overwrite = True

    print(f"将处理 {len(files)} 个文件；语言固定为美式英语（en）。")
    processor = None
    try:
        processor = WhisperSRTProcessor(
            model_name=args.model,
            device=args.device,
            align_device=args.align_device,
            batch_size=max(1, args.batch_size),
        )
        failed = 0
        for source in files:
            try:
                processor.convert(source, overwrite=args.overwrite)
            except Exception as exc:
                failed += 1
                print(f"失败：{source}\n原因：{exc}")
        print(f"\n处理结束：成功 {len(files) - failed} 个，失败 {failed} 个。")
        return 1 if failed else 0
    except KeyboardInterrupt:
        print("\n用户中断。")
        return 130
    except Exception as exc:
        print(f"\n启动失败：{exc}")
        return 1
    finally:
        if processor is not None:
            processor.close()


if __name__ == "__main__":
    raise SystemExit(main())
