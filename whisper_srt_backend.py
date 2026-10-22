"""Reusable WhisperX backend for word-level English SRT generation."""

from __future__ import annotations

import gc
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

AUDIO_EXTENSIONS = {
    ".aac", ".aiff", ".alac", ".flac", ".m4a", ".m4v", ".mka", ".mkv",
    ".mov", ".mp3", ".mp4", ".ogg", ".opus", ".wav", ".webm", ".wma",
}


def configure_cuda_dlls() -> None:
    """Expose pip-installed NVIDIA DLL directories on Windows."""
    site_packages = Path(sys.prefix) / "Lib" / "site-packages"
    nvidia_root = site_packages / "nvidia"
    if not nvidia_root.is_dir():
        return
    for dll_dir in nvidia_root.glob("*/bin"):
        if dll_dir.is_dir():
            if hasattr(os, "add_dll_directory"):
                os.add_dll_directory(str(dll_dir))
            os.environ["PATH"] = str(dll_dir) + os.pathsep + os.environ.get("PATH", "")


configure_cuda_dlls()

import torch  # noqa: E402
import whisperx  # noqa: E402


@dataclass
class ConversionResult:
    source: Path
    output: Path
    words: int
    language: str
    first_time: float | None
    last_time: float | None


def choose_device(requested: str) -> str:
    cuda_backend = False
    if torch.cuda.is_available():
        try:
            import ctranslate2
            cuda_backend = ctranslate2.get_cuda_device_count() > 0
        except Exception:
            cuda_backend = False
    if requested == "auto":
        if torch.cuda.is_available() and cuda_backend:
            return "cuda"
        print("鏈娴嬪埌鍙敤鐨?ctranslate2 CUDA 鍚庣锛屽皢浣跨敤 CPU銆?, flush=True)
        return "cpu"
    if requested == "cuda" and (not torch.cuda.is_available() or not cuda_backend):
        raise RuntimeError("宸叉寚瀹?CUDA锛屼絾褰撳墠 Python 鐜妫€娴嬩笉鍒板彲鐢?CUDA/ctranslate2 鍚庣銆傝鍏堣繍琛?install_whisper_srt.bat銆?)
    return requested


def output_path_for(source: Path) -> Path:
    return source.with_name(f"{source.stem}.word_whisperx.srt")


def iter_audio_files(path: Path, recursive: bool = False) -> list[Path]:
    if path.is_file():
        if path.suffix.lower() not in AUDIO_EXTENSIONS:
            raise ValueError(f"涓嶆敮鎸佺殑闊抽/瑙嗛鏍煎紡锛歿path.suffix}")
        return [path]
    if not path.is_dir():
        raise FileNotFoundError(f"鎵句笉鍒拌矾寰勶細{path}")
    iterator: Iterable[Path] = path.rglob("*") if recursive else path.iterdir()
    return sorted(p for p in iterator if p.is_file() and p.suffix.lower() in AUDIO_EXTENSIONS)


def _srt_time(seconds: float) -> str:
    total_ms = max(0, round(seconds * 1000))
    hours, rem = divmod(total_ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, millis = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


class WhisperSRTProcessor:
    """Load ASR once and process any number of local files."""

    def __init__(
        self,
        model_name: str = "large-v3",
        device: str = "auto",
        align_device: str = "cpu",
        batch_size: int = 4,
    ) -> None:
        self.device = choose_device(device)
        self.align_device = choose_device(align_device) if align_device != "auto" else (
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.batch_size = batch_size
        compute_type = "float16" if self.device == "cuda" else "int8"
        print(f"鍔犺浇 ASR 妯″瀷 {model_name}锛堣澶囷細{self.device}锛岃绠楃被鍨嬶細{compute_type}锛?..", flush=True)
        self.asr_model = whisperx.load_model(
            model_name,
            device=self.device,
            # WhisperX ships this VAD checkpoint locally; it avoids a separate
            # torch.hub download each time the reusable tool is started.
            vad_method="pyannote",
            compute_type=compute_type,
            language="en",
            asr_options={
                "initial_prompt": "Transcribe in American English using American spelling and punctuation.",
            },
        )
        self._align_model = None
        self._align_metadata = None

    def _load_alignment_model(self) -> None:
        if self._align_model is None:
            print(f"鍔犺浇鑻辫寮哄埗瀵归綈妯″瀷锛堣澶囷細{self.align_device}锛?..", flush=True)
            self._align_model, self._align_metadata = whisperx.load_align_model(
                language_code="en", device=self.align_device
            )

    def convert(self, source: Path, output: Path | None = None, overwrite: bool = False) -> ConversionResult:
        source = source.resolve()
        output = (output or output_path_for(source)).resolve()
        if output.exists() and not overwrite:
            raise FileExistsError(f"杈撳嚭鏂囦欢宸插瓨鍦細{output}")

        print(f"\n杞綍锛歿source.name}", flush=True)
        audio = whisperx.load_audio(str(source))
        result = self.asr_model.transcribe(audio, batch_size=self.batch_size, language="en")
        self._load_alignment_model()
        aligned = whisperx.align(
            result["segments"], self._align_model, self._align_metadata, audio,
            self.align_device, return_char_alignments=False,
        )

        index = 1
        first_time = None
        last_time = None
        with output.open("w", encoding="utf-8-sig", newline="\n") as handle:
            for segment in aligned["segments"]:
                for word in segment.get("words", []):
                    text = str(word.get("word", "")).strip()
                    start, end = word.get("start"), word.get("end")
                    if not text or start is None or end is None:
                        continue
                    start, end = float(start), float(end)
                    if first_time is None:
                        first_time = start
                    last_time = end
                    handle.write(f"{index}\n{_srt_time(start)} --> {_srt_time(end)}\n{text}\n\n")
                    index += 1

        words = index - 1
        print(f"瀹屾垚锛歿output.name}锛坽words} 涓崟璇嶏級", flush=True)
        return ConversionResult(source, output, words, result.get("language", "en"), first_time, last_time)

    def close(self) -> None:
        self.asr_model = None
        self._align_model = None
        self._align_metadata = None
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

