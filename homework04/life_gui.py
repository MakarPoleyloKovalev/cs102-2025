"""Графический интерфейс для игры 'Жизнь'"""

import pygame
from life import GameOfLife
from ui import UI


class GUI(UI):
    """Графический интерфейс для игры 'Жизнь'"""

    def __init__(self, game_life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(game_life)
        self.cell_size = cell_size
        self.speed = speed
        self.paused = True  # По умолчанию на паузе, чтобы можно было рисовать
        self.drawing = False

        # Вычисляем размер окна
        self.width = game_life.cols * cell_size
        self.height = game_life.rows * cell_size

        # Инициализация pygame
        pygame.init()  # pylint: disable=no-member
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life - Графическая версия")

        # Шрифт для текста
        self.font = pygame.font.SysFont(None, 24)

    def draw_lines(self) -> None:
        """Рисование сетки"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """Отрисовка клеток"""
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                color = pygame.Color("green") if self.life.curr_generation[row][col] == 1 else pygame.Color("white")
                rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)
                # Рисуем тонкую границу для лучшей видимости
                pygame.draw.rect(self.screen, pygame.Color("gray"), rect, 1)

    def handle_click(self, pos: tuple) -> None:
        """Обработка клика мыши"""
        if not self.paused:
            return

        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size

        if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
            # Инвертируем состояние клетки
            self.life.curr_generation[row][col] = 1 - self.life.curr_generation[row][col]

    def draw_info(self) -> None:
        """Отображение информации на экране"""
        # Поколение
        gen_text = f"Поколение: {self.life.generations}"
        if self.life.max_generations != float("inf"):
            gen_text += f" / {self.life.max_generations}"
        gen_surface = self.font.render(gen_text, True, pygame.Color("black"))
        self.screen.blit(gen_surface, (10, 10))

        # Статус паузы
        status = "ПАУЗА (можно рисовать)" if self.paused else "ВОСПРОИЗВЕДЕНИЕ"
        status_surface = self.font.render(status, True, pygame.Color("red"))
        self.screen.blit(status_surface, (10, 40))

        # Подсказки
        hints = [
            "ПРОБЕЛ: пауза/продолжить",
            "R: случайная генерация",
            "C: очистить поле",
            "ESC: выход",
            "ЛКМ: рисовать (в паузе)",
            "S: шаг вперед (в паузе)",
        ]
        for i, hint in enumerate(hints):
            hint_surface = self.font.render(hint, True, pygame.Color("darkgray"))
            self.screen.blit(hint_surface, (10, self.height - 30 * (len(hints) - i)))

    def run(self) -> None:
        """Запуск игрового цикла"""
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pylint: disable=no-member
                    running = False
                elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                    if event.key == pygame.K_SPACE:  # pylint: disable=no-member
                        self.paused = not self.paused
                    elif event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
                        running = False
                    elif event.key == pygame.K_r:  # pylint: disable=no-member
                        # Случайная генерация
                        self.life = GameOfLife((self.life.rows, self.life.cols), randomize=True)
                    elif event.key == pygame.K_c:  # pylint: disable=no-member
                        # Очистка поля
                        self.life = GameOfLife((self.life.rows, self.life.cols), randomize=False)
                    elif event.key == pygame.K_s and self.paused:  # pylint: disable=no-member
                        # Шаг вперед в режиме паузы
                        self.life.step()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
                    if self.paused and event.button == 1:  # Левая кнопка мыши
                        self.drawing = True
                        self.handle_click(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:  # pylint: disable=no-member
                    if event.button == 1:
                        self.drawing = False
                elif event.type == pygame.MOUSEMOTION:  # pylint: disable=no-member
                    if self.drawing and self.paused:
                        self.handle_click(event.pos)

            # Очищаем экран
            self.screen.fill(pygame.Color("white"))

            # Обновляем поколение, если игра не на паузе
            if not self.paused and self.life.is_changing and not self.life.is_max_generations_exceeded:
                self.life.step()

            # Рисуем сетку и клетки
            self.draw_grid()
            self.draw_lines()
            self.draw_info()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()  # pylint: disable=no-member


if __name__ == "__main__":
    # Пример запуска
    game = GameOfLife((48, 64), randomize=True, max_generations=1000)
    ui = GUI(game, cell_size=15, speed=10)
    ui.run()
