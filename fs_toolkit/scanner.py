"""
Модуль сканування файлової системи та аналізу метаданих файлів.
Освітній компонент: Програмування на Python.
"""

import os
import time
from pathlib import Path



def scan_directory_tree(base_path: Path, hours: int = 24) -> list[dict]:
    """
    Виконує рекурсивне сканування базової директорії, знаходить файли,
    змінені за останні N годин.
    Повертає список словників зі структурованими метаданими.
    """
    if not base_path.exists() or not base_path.is_dir():
        raise ValueError(f"Шлях '{base_path}' не існує або не є директорією.")

    if hours <= 0:
        raise ValueError("Кількість годин повинна бути додатною.")

    matched_files = []
    current_time = time.time()

    # Рекурсивний обхід усіх вузлів файлової системи
    for item in base_path.rglob("*"):
        if item.is_file():
            try:
                stat_res = item.stat()
                file_size = stat_res.st_size

                # Перевірка часу останньої модифікації
                time_difference = current_time - stat_res.st_mtime

                if 0 <= time_difference <= hours * 3600:
                    octal_permissions = oct(stat_res.st_mode & 0o777)
                    modification_time = time.strftime(
                        "%Y-%m-%d %H:%M:%S",
                        time.localtime(stat_res.st_mtime)
                    )

                    file_record = {
                        "path": item,
                        "relative_path": item.relative_to(base_path),
                        "size_bytes": file_size,
                        "size_kb": file_size / 1024.0,
                        "modified_at": modification_time,
                        "permissions": octal_permissions,
                    }
                    matched_files.append(file_record)

            except (PermissionError, OSError) as err:
                print(f"Попередження системи: Немає доступу до файлу '{item}': {err}")
                continue

    return matched_files
