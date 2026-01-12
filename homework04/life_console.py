"""Консольный интерфейс для игры 'Жизнь'"""

import curses
from life import GameOfLife
from ui import UI


class Console(UI):
    """Консольный интерфейс для игры 'Жизнь'"""

    def __init__(self, game_life: GameOfLife) -> None:
        super().__init__(game_life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку"""
        screen.border(0)

    def draw_grid(self, screen, height: int, width: int) -> None:
        """Отобразить состояние клеток"""
        for i in range(min(height - 2, self.life.rows)):
            for j in range(min(width - 2, self.life.cols)):
                if self.life.curr_generation[i][j] == 1:
                    try:
                        screen.addch(i + 1, j + 1, "█")
                    except curses.error:
                        pass

    def run(self) -> None:
        """Запуск консольного интерфейса"""
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        curses.curs_set(0)

        try:
            height, width = screen.getmaxyx()

            while self.life.is_changing and not self.life.is_max_generations_exceeded:
                screen.clear()
                self.draw_borders(screen)

                # Отображение информации
                info = f"Поколение: {self.life.generations}"
                if self.life.max_generations != float("inf"):
                    info += f" / {self.life.max_generations}"
                screen.addstr(0, 2, info[: width - 4])
                screen.addstr(height - 1, 2, "Q: выход, N: следующий шаг"[: width - 4])

                # Отображение сетки
                self.draw_grid(screen, height, width)

                screen.refresh()

                # Ожидание ввода
                screen.timeout(500)  # 500 мс
                key = screen.getch()

                if key in (ord("q"), ord("Q")):
                    break
                if key in (ord("n"), ord("N")):
                    self.life.step()
                elif key == curses.KEY_RESIZE:
                    height, width = screen.getmaxyx()
                else:
                    self.life.step()

        finally:
            curses.nocbreak()
            screen.keypad(False)
            curses.echo()
            curses.endwin()


if __name__ == "__main__":
    # Пример запуска
    life = GameOfLife((24, 80), max_generations=100)
    ui = Console(life)
    ui.run()
