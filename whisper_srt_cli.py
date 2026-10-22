"""Chinese command-line frontend for the reusable WhisperX SRT backend."""

from __future__ import annotations

import argparse
import shlex
from pathlib import Path

from whisper_srt_backend import WhisperSRTProcessor, iter_audio_files, output_path_for


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="灏嗘湰鏈洪煶棰?瑙嗛杞负缇庡紡鑻辫閫愯瘝鏃堕棿鎴?SRT锛屽瓧骞曞啓鍏ユ簮鏂囦欢鍚岀洰褰曘€?
    )
    parser.add_argument("paths", nargs="*", help="鏂囦欢鎴栫洰褰曪紱璺緞鍚┖鏍兼椂璇峰姞寮曞彿")
    parser.add_argument("-r", "--recursive", action="store_true", help="鐩綍妯″紡涓嬮€掑綊鎵弿瀛愮洰褰?)
    parser.add_argument("--overwrite", action="store_true", help="瑕嗙洊宸叉湁鍚屽悕瀛楀箷")
    parser.add_argument("--device", choices=("auto", "cuda", "cpu"), default="auto", help="ASR 璁惧锛岄粯璁よ嚜鍔ㄩ€夋嫨")
    parser.add_argument("--align-device", choices=("auto", "cuda", "cpu"), default="cpu", help="寮哄埗瀵归綈璁惧锛岄粯璁?CPU 浠ヨ妭鐪佹樉瀛?)
    parser.add_argument("--batch-size", type=int, default=4, help="GPU 鎵瑰ぇ灏忥紝鏄惧瓨涓嶈冻鏃惰皟灏?)
    parser.add_argument("--model", default="large-v3", help="Whisper 妯″瀷鍚嶏紝榛樿 large-v3")
    return parser


def interactive_paths() -> list[str]:
    print("璇疯緭鍏ヨ杞崲鐨勬枃浠舵垨鐩綍銆傚彲浠ヨ緭鍏ュ涓矾寰勶紝鐢ㄥ垎鍙峰垎闅旓紱鐩存帴鍥炶溅閫€鍑恒€?)
    raw = input("璺緞锛?).strip()
    if not raw:
        return []
    if ";" in raw:
        return [part.strip().strip('"') for part in raw.split(";") if part.strip()]
    try:
        return shlex.split(raw, posix=False)
    except ValueError:
        return [raw.strip('"')]


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    raw_paths = args.paths or interactive_paths()
    if not raw_paths:
        print("鏈寚瀹氳矾寰勶紝绋嬪簭缁撴潫銆?)
        return 0

    files: list[Path] = []
    for raw in raw_paths:
        try:
            files.extend(iter_audio_files(Path(raw.strip('"')), recursive=args.recursive))
        except (FileNotFoundError, ValueError) as exc:
            print(f"璺宠繃锛歿exc}")
    files = list(dict.fromkeys(files))
    if not files:
        print("娌℃湁鎵惧埌鍙鐞嗙殑闊抽/瑙嗛鏂囦欢銆?)
        return 1

    if not args.overwrite:
        existing = [p for p in files if output_path_for(p).exists()]
        if existing:
            answer = input(f"鍙戠幇 {len(existing)} 涓凡鏈夊瓧骞曪紝鏄惁瑕嗙洊锛?y/N)锛?).strip().lower()
            if answer in {"y", "yes"}:
                args.overwrite = True

    print(f"灏嗗鐞?{len(files)} 涓枃浠讹紱璇█鍥哄畾涓虹編寮忚嫳璇紙en锛夈€?)
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
                print(f"澶辫触锛歿source}\n鍘熷洜锛歿exc}")
        print(f"\n澶勭悊缁撴潫锛氭垚鍔?{len(files) - failed} 涓紝澶辫触 {failed} 涓€?)
        return 1 if failed else 0
    except KeyboardInterrupt:
        print("\n鐢ㄦ埛涓柇銆?)
        return 130
    finally:
        if processor is not None:
            processor.close()


if __name__ == "__main__":
    raise SystemExit(main())

