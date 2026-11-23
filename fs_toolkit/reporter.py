"""
Модуль форматування та консольного виведення результатів аудиту файлової системи.
Освітній компонент: Програмування на Python.
"""

from typing import List, Dict


def print_audit_report(file_records: List[Dict], hours: int, search_root: str) -> None:
    """
    Генерує вирівняний інженерний табличний звіт про результати аудиту
    файлів із підрахунком сумарного обсягу пам'яті.
    """
    header_sep = "=" * 92
    row_sep = "-" * 92

    print("\n" + header_sep)
    print(f"{'ЗВІТ СИСТЕМНОГО АУДИТУ ДИСКОВОГО ПРОСТОРУ ТА ФАЙЛІВ':^92}")
    print(header_sep)
    print(f"Базова директорія пошуку: {search_root}")
    print(f"Період пошуку: останні {hours} годин")
    print(row_sep)
    print(
        f"| {'№':^4} | {'Відносний шлях файлу':<36} | "
        f"{'Розмір (КБ)':^12} | {'Дата модифікації':^19} | {'Права':^7} |"
    )
    print(row_sep)

    total_bytes = 0

    for idx, rec in enumerate(file_records, start=1):
        total_bytes += rec["size_bytes"]
        rel_path_str = str(rec["relative_path"])
        # Обрізання занадто довгих шляхів для збереження геометрії таблиці
        if len(rel_path_str) > 36:
            rel_path_str = f"...{rel_path_str[-33:]}"

        print(
            f"| {idx:^4d} | {rel_path_str:<36} | "
            f"{rec['size_kb']:>10.2f} КБ | {rec['modified_at']:^19} | {rec['permissions']:^7} |"
        )

    print(header_sep)
    total_kb = total_bytes / 1024.0
    total_mb = total_kb / 1024.0
    print(f"{'ПІДСУМКОВА ДИСКОВА СТАТИСТИКА':^92}")
    print(row_sep)
    print(f"  Всього знайдено відповідних файлів: {len(file_records):>6d}")
    print(f"  Сумарний фізичний обсяг вибірки:    {total_kb:>10.2f} КБ ({total_mb:.4f} МБ)")
    print(header_sep + "\n")