"""Главный модуль для запуска игры 'Жизнь' в разных режимах"""

import pathlib
import time
from life import GameOfLife
from life_console import Console
from life_gui import GUI
from life_proto import GameOfLife as GameOfLifeProto


def main() -> None:
    """Основная функция запуска"""
    print("Игра 'Жизнь' - Конвей")
    print("=" * 40)
    print("Выберите режим:")
    print("1 - Прототип (быстрая версия с pygame)")
    print("2 - Консольная версия (curses)")
    print("3 - Графическая версия (GUI)")
    print("4 - Загрузить из файла и запустить в GUI")

    choice = input("Введите номер (1-4): ").strip()

    if choice == "1":
        # Запуск прототипа
        print("Запуск прототипа...")
        game = GameOfLifeProto(640, 480, 20, 10)
        game.run()

    elif choice == "2":
        # Запуск консольной версии
        print("Запуск консольной версии...")
        print("Размеры: 24 строки, 80 столбцов")
        print("Максимальное количество поколений: 100")
        print("Нажмите Q для выхода, N для следующего шага")
        print("(закроется через 3 секунды...)")

        time.sleep(3)

        # Создаем игровое поле
        life = GameOfLife((24, 80), max_generations=100)

        # Запускаем консольный интерфейс
        ui = Console(life)  # type: ignore
        ui.run()

    elif choice == "3":
        # Запуск графической версии
        print("Запуск графической версии...")

        # Создаем игровое поле
        life = GameOfLife((48, 64), randomize=True, max_generations=1000)

        # Запускаем графический интерфейс
        ui = GUI(life, cell_size=15, speed=10)  # type: ignore
        ui.run()

    elif choice == "4":
        # Загрузка из файла
        filename = input("Введите имя файла (например, glider.txt): ").strip()
        try:
            life = GameOfLife.from_file(pathlib.Path(filename))
            print(f"Загружено поле {life.rows}x{life.cols}")

            # Запускаем графический интерфейс
            ui = GUI(life, cell_size=20, speed=5)  # type: ignore
            ui.run()
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
        except ValueError as e:
            print(f"Ошибка в формате файла: {e}")

    else:
        print("Неверный выбор")


if __name__ == "__main__":
    main()
