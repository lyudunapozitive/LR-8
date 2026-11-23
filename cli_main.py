
"""
Головна точка входу консольної утиліти сканування модифікованих файлів.
Здійснює розбір параметрів командного рядка sys.argv та диспетчеризацію завдань.
Освітній компонент: Програмування на Python.
Варіант 20.
"""

import sys
import time
from pathlib import Path

# Імпорт публічного інтерфейсу з власного пакета fs_toolkit
from fs_toolkit import scan_directory_tree, print_audit_report


def print_usage_help() -> None:
    """Виводить інструкцію з використання утиліти командного рядка."""
    usage_text = """
ВИКОРИСТАННЯ:
    python cli_main.py --path <каталог> [--hours <24>]

ПАРАМЕТРИ:
    --path       : (Обов'язковий) Абсолютний або відносний шлях до цільового каталогу.
    --hours      : (Опціональний) Період пошуку файлів у годинах (за замовчуванням: 24).
    --help, -h   : Виведення цієї інформаційної довідки.

ПРИКЛАДИ:
    python cli_main.py --path ./test_sandbox --hours 24
    python cli_main.py --path ./test_sandbox
"""
    print(usage_text)


def parse_cli_arguments(args_list: list[str]) -> dict:
    """
    Здійснює ручний розбір списку аргументів командного рядка sys.argv.
    Повертає словник виділених параметрів конфігурації.
    """
    config = {
        "path": None,
        "hours": 24,
    }

    if "--help" in args_list or "-h" in args_list or len(args_list) <= 1:
        print_usage_help()
        sys.exit(0)

    i = 1
    while i < len(args_list):
        arg = args_list[i]

        if arg == "--path":
            if i + 1 < len(args_list):
                config["path"] = Path(args_list[i + 1]).resolve()
                i += 2
            else:
                print("Помилка синтаксису: Після прапорця '--path' необхідно вказати шлях до каталогу.")
                sys.exit(1)

        elif arg == "--hours":
            if i + 1 < len(args_list):
                try:
                    config["hours"] = int(args_list[i + 1])
                    i += 2
                except ValueError:
                    print("Помилка значення: Параметр '--hours' повинен бути цілим числом.")
                    sys.exit(1)
            else:
                print("Помилка синтаксису: Після '--hours' необхідно вказати кількість годин.")
                sys.exit(1)

        else:
            print(f"Помилка: Невідомий параметр командного рядка '{arg}'.")
            print_usage_help()
            sys.exit(1)

    if config["path"] is None:
        print("Помилка: Обов'язковий параметр '--path' не вказано.")
        print_usage_help()
        sys.exit(1)

    if config["hours"] <= 0:
        print("Помилка: Кількість годин повинна бути додатною.")
        sys.exit(1)

    return config


def main() -> None:
    """Головна функція диспетчеризації CLI-утиліти."""
    # 1. Розбір вхідних параметрів командного рядка
    cli_config = parse_cli_arguments(sys.argv)

    target_directory = cli_config["path"]
    hours = cli_config["hours"]

    t_start = time.perf_counter()

    # 2. Виконання сканування файлової системи за допомогою пакета
    try:
        results = scan_directory_tree(
            base_path=target_directory,
            hours=hours,
        )
    except ValueError as val_err:
        print(f"Помилка аргументів: {val_err}")
        sys.exit(2)
    except Exception as general_err:
        print(f"Критичний збій виконання аудиту: {general_err}")
        sys.exit(3)

    # 3. Формування та друк звіту
    print_audit_report(results, hours, str(target_directory))

    t_elapsed = time.perf_counter() - t_start
    print(f"Операція сканування успішно завершена за {t_elapsed * 1000:.3f} мс.")
    sys.exit(0)


if __name__ == "__main__":
    main()
