#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ANKA2 - Batch GR2 to glTF Converter
================================================================================
Tüm .gr2 dosyalarını paralel olarak glTF formatına dönüştürür.

Kullanım:
    python batch_convert.py --input ./models --output ./output
    python batch_convert.py --input ./models --output ./output --workers 8
    python batch_convert.py --input ./models --output ./output --format glb
================================================================================
"""

import os
import sys
import argparse
import subprocess
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Optional
import json

# ============================================================================
# Ayarlar
# ============================================================================
DEFAULT_WORKERS = 4
DEFAULT_FORMAT = "gltf"
CONVERTER_NAME = "gr2togltf.exe"

# ============================================================================
# Veri Yapıları
# ============================================================================
@dataclass
class ConvertResult:
    input_path: str
    output_path: str
    success: bool
    error_message: str = ""
    duration: float = 0.0

@dataclass
class BatchStats:
    total: int = 0
    success: int = 0
    failed: int = 0
    skipped: int = 0
    total_duration: float = 0.0

# ============================================================================
# Yardımcı Fonksiyonlar
# ============================================================================
def find_converter() -> Optional[str]:
    """gr2togltf.exe'yi bul"""
    # Mevcut dizinde
    if os.path.exists(CONVERTER_NAME):
        return os.path.abspath(CONVERTER_NAME)
    
    # Script dizininde
    script_dir = os.path.dirname(os.path.abspath(__file__))
    converter_path = os.path.join(script_dir, CONVERTER_NAME)
    if os.path.exists(converter_path):
        return converter_path
    
    # tools/gr2togltf/build/Release dizininde
    build_path = os.path.join(script_dir, "gr2togltf", "build", "Release", CONVERTER_NAME)
    if os.path.exists(build_path):
        return build_path
    
    # PATH'te
    import shutil
    return shutil.which(CONVERTER_NAME)

def find_gr2_files(input_dir: str) -> List[str]:
    """Dizindeki tüm .gr2 dosyalarını bul"""
    gr2_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.gr2'):
                gr2_files.append(os.path.join(root, file))
    return gr2_files

def get_output_path(input_path: str, input_dir: str, output_dir: str, format: str) -> str:
    """Çıktı dosya yolunu hesapla"""
    # Göreceli yolu koru
    rel_path = os.path.relpath(input_path, input_dir)
    output_path = os.path.join(output_dir, rel_path)
    
    # Uzantıyı değiştir
    base, _ = os.path.splitext(output_path)
    return f"{base}.{format}"

# ============================================================================
# Dönüştürme
# ============================================================================
def convert_single(
    converter_path: str,
    input_path: str,
    output_path: str,
    format: str,
    extra_args: List[str] = None
) -> ConvertResult:
    """Tek bir dosyayı dönüştür"""
    start_time = time.time()
    
    # Çıktı dizinini oluştur
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Komut oluştur
    cmd = [
        converter_path,
        "--input", input_path,
        "--output", output_path,
        "--format", format
    ]
    
    if extra_args:
        cmd.extend(extra_args)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60  # 60 saniye timeout
        )
        
        duration = time.time() - start_time
        
        if result.returncode == 0:
            return ConvertResult(
                input_path=input_path,
                output_path=output_path,
                success=True,
                duration=duration
            )
        else:
            return ConvertResult(
                input_path=input_path,
                output_path=output_path,
                success=False,
                error_message=result.stderr or result.stdout,
                duration=duration
            )
            
    except subprocess.TimeoutExpired:
        return ConvertResult(
            input_path=input_path,
            output_path=output_path,
            success=False,
            error_message="Timeout (60s)",
            duration=60.0
        )
    except Exception as e:
        return ConvertResult(
            input_path=input_path,
            output_path=output_path,
            success=False,
            error_message=str(e),
            duration=time.time() - start_time
        )

def batch_convert(
    input_dir: str,
    output_dir: str,
    format: str = DEFAULT_FORMAT,
    workers: int = DEFAULT_WORKERS,
    extra_args: List[str] = None,
    skip_existing: bool = False
) -> BatchStats:
    """Toplu dönüştürme"""
    
    # Converter'ı bul
    converter = find_converter()
    if not converter:
        print(f"HATA: {CONVERTER_NAME} bulunamadı!")
        print("Önce gr2togltf tool'unu derleyin:")
        print("  cd tools/gr2togltf")
        print("  mkdir build && cd build")
        print("  cmake .. -G \"Visual Studio 17 2022\" -A Win32")
        print("  cmake --build . --config Release")
        sys.exit(1)
    
    print(f"Converter: {converter}")
    
    # GR2 dosyalarını bul
    gr2_files = find_gr2_files(input_dir)
    
    if not gr2_files:
        print(f"UYARI: {input_dir} dizininde .gr2 dosyası bulunamadı")
        return BatchStats()
    
    print(f"Bulunan .gr2 dosyası: {len(gr2_files)}")
    
    # İstatistikler
    stats = BatchStats(total=len(gr2_files))
    results: List[ConvertResult] = []
    
    # Dönüştürme görevleri
    tasks = []
    for gr2_path in gr2_files:
        output_path = get_output_path(gr2_path, input_dir, output_dir, format)
        
        # Mevcut dosyayı atla
        if skip_existing and os.path.exists(output_path):
            stats.skipped += 1
            continue
        
        tasks.append((gr2_path, output_path))
    
    if not tasks:
        print("Dönüştürülecek dosya yok (tümü mevcut)")
        return stats
    
    print(f"Dönüştürülecek: {len(tasks)}")
    print(f"Worker sayısı: {workers}")
    print()
    
    # Paralel dönüştürme
    start_time = time.time()
    completed = 0
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                convert_single, converter, inp, out, format, extra_args
            ): (inp, out)
            for inp, out in tasks
        }
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            completed += 1
            
            if result.success:
                stats.success += 1
                status = "✓"
            else:
                stats.failed += 1
                status = "✗"
            
            # İlerleme
            progress = (completed / len(tasks)) * 100
            filename = os.path.basename(result.input_path)
            print(f"[{progress:5.1f}%] {status} {filename} ({result.duration:.2f}s)")
            
            if not result.success and result.error_message:
                print(f"         Hata: {result.error_message[:100]}")
    
    stats.total_duration = time.time() - start_time
    
    # Özet
    print()
    print("=" * 60)
    print("SONUÇ")
    print("=" * 60)
    print(f"Toplam     : {stats.total}")
    print(f"Başarılı   : {stats.success}")
    print(f"Başarısız  : {stats.failed}")
    print(f"Atlanan    : {stats.skipped}")
    print(f"Süre       : {stats.total_duration:.2f}s")
    print(f"Ortalama   : {stats.total_duration/max(1, completed):.2f}s/dosya")
    print("=" * 60)
    
    # Başarısız dosyaları kaydet
    if stats.failed > 0:
        failed_log = os.path.join(output_dir, "failed_conversions.txt")
        with open(failed_log, 'w', encoding='utf-8') as f:
            for r in results:
                if not r.success:
                    f.write(f"{r.input_path}\n")
                    f.write(f"  Hata: {r.error_message}\n\n")
        print(f"\nBaşarısız dosyalar: {failed_log}")
    
    return stats

# ============================================================================
# Ana Program
# ============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="ANKA2 - Batch GR2 to glTF Converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python batch_convert.py -i ./models -o ./output
  python batch_convert.py -i ./models -o ./output -w 8
  python batch_convert.py -i ./models -o ./output -f glb
  python batch_convert.py -i ./models -o ./output --skip-existing
        """
    )
    
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Girdi dizini (.gr2 dosyalarını içeren)"
    )
    
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Çıktı dizini"
    )
    
    parser.add_argument(
        "-f", "--format",
        default=DEFAULT_FORMAT,
        choices=["gltf", "glb"],
        help=f"Çıktı formatı (varsayılan: {DEFAULT_FORMAT})"
    )
    
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"Paralel worker sayısı (varsayılan: {DEFAULT_WORKERS})"
    )
    
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Mevcut çıktı dosyalarını atla"
    )
    
    parser.add_argument(
        "--flip-uv",
        action="store_true",
        help="UV koordinatlarını çevir"
    )
    
    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Ölçek faktörü (varsayılan: 1.0)"
    )
    
    args = parser.parse_args()
    
    # Ekstra argümanlar
    extra_args = []
    if args.flip_uv:
        extra_args.append("--flip-uv")
    if args.scale != 1.0:
        extra_args.extend(["--scale", str(args.scale)])
    
    # Dönüştür
    stats = batch_convert(
        input_dir=args.input,
        output_dir=args.output,
        format=args.format,
        workers=args.workers,
        extra_args=extra_args if extra_args else None,
        skip_existing=args.skip_existing
    )
    
    # Exit code
    sys.exit(0 if stats.failed == 0 else 1)

if __name__ == "__main__":
    main()
