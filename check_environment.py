"""Lightweight dependency check used by the Windows launcher and installer."""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import shutil
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--require-cuda", action="store_true")
    parser.add_argument("--python-only", action="store_true", help="Only check the Python version for venv creation")
    args = parser.parse_args()
    if args.python_only:
        return 0 if (3, 10) <= sys.version_info[:2] <= (3, 12) else 1

    modules = {
        "whisperx": importlib.util.find_spec("whisperx") is not None,
        "faster_whisper": importlib.util.find_spec("faster_whisper") is not None,
        "torch": importlib.util.find_spec("torch") is not None,
        "ctranslate2": importlib.util.find_spec("ctranslate2") is not None,
    }
    import_errors = {}
    for name, found in modules.items():
        if not found:
            continue
        try:
            importlib.import_module(name)
        except Exception as exc:
            modules[name] = False
            import_errors[name] = str(exc)
    ffmpeg = shutil.which("ffmpeg")
    cuda = False
    cuda_name = ""
    torch_version = ""
    cuda_backend = False
    if modules["torch"]:
        try:
            import torch

            cuda = bool(torch.cuda.is_available())
            torch_version = torch.__version__
            if cuda:
                cuda_name = torch.cuda.get_device_name(0)
        except Exception:
            cuda = False
    if modules["ctranslate2"] and cuda:
        try:
            import ctranslate2
            cuda_backend = ctranslate2.get_cuda_device_count() > 0
        except Exception:
            cuda_backend = False

    result = {
        "python": sys.executable,
        "python_version": sys.version.split()[0],
        "modules": modules,
        "import_errors": import_errors,
        "ffmpeg": ffmpeg,
        "all_required_modules": all(modules.values()),
        "cuda_available": cuda,
        "cuda_device": cuda_name,
        "ctranslate2_cuda_backend": cuda_backend,
        "torch_version": torch_version,
    }
    if not args.quiet:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["all_required_modules"]:
        return 1
    if args.require_cuda and not (cuda and cuda_backend):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
