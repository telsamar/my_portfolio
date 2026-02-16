#!/usr/bin/env python3
import json
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, 'input')
CONFIG_PATH = os.path.join(SCRIPT_DIR, 'input', 'forecast_config.json')
MAIN_SCRIPT = os.path.join(SCRIPT_DIR, 'main.py')

DEFAULT_CONFIG = {"exclusions": [], "coefficients": []}


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()


def save_config(data):
    os.makedirs(INPUT_DIR, exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def show_config():
    try:
        data = load_config()
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Ошибка: {e}")


def edit_config_editor():
    os.makedirs(INPUT_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
    path = os.path.abspath(CONFIG_PATH)
    if sys.platform == 'darwin':
        subprocess.run(['open', path])
    elif sys.platform == 'win32':
        os.startfile(path)
    else:
        editor = os.environ.get('EDITOR', 'xdg-open')
        subprocess.run([editor, path])


def run_forecast():
    print("\nЗапуск расчёта...\n")
    try:
        code = subprocess.run(
            [sys.executable, MAIN_SCRIPT],
            cwd=SCRIPT_DIR,
        ).returncode
        print(f"\nЗавершено с кодом {code}" if code != 0 else "\nГотово.")
    except Exception as e:
        print(f"Ошибка запуска: {e}")
        sys.exit(1)


def main():
    print("=" * 50)
    print("  Прогноз заявок — настройка и запуск")
    print("=" * 50)

    while True:
        print("  1 — Показать текущий конфиг")
        print("  2 — Открыть конфиг в редакторе (отредактируйте и сохраните файл)")
        print("  3 — Запустить расчёт (с текущим конфигом)")
        print("  0 — Выход")
        try:
            choice = input("\nВыбор: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            break

        if choice == '0':
            print("Выход.")
            break
        elif choice == '1':
            show_config()
        elif choice == '2':
            edit_config_editor()
            print("Сохраните файл в редакторе и закройте его.")
        elif choice == '3':
            run_forecast()
        else:
            print("Введите 0, 1, 2 или 3.")


if __name__ == "__main__":
    main()
