"""Импорт модулей из библиотеки."""
from random import choice, randint


import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Центральная точка экрана:
initial_position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс."""

    def __init__(self, position=initial_position, body_color=(0, 0, 0)):
        """Родительский конструктор принимающий атрибуты позиции и цвета."""
        self.body_color = body_color
        self.position = position

    def draw(self, surface):
        """Абстрактный метод, реализуется в дочерних классах."""
        pass


class Apple(GameObject):
    """Дочерний класс описывающий игровое яблоко."""

    def __init__(self, position=initial_position, body_color=APPLE_COLOR):
        """Дочерний конструктор принимающий атрибуты позиции и цвета."""
        super().__init__(position, body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод устанавливающий яблоко в случайном порядке."""
        return (randint(0, 31) * GRID_SIZE, randint(0, 23) * GRID_SIZE)

    def draw(self, surface):
        """Метод отрисовывающий яблоко на игровом поле."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс определяющий объект: Змейка."""

    def __init__(self, body_color=SNAKE_COLOR, position=initial_position):
        """Дочерний конструктор с атрибутами длинны, цвета, позиции, направления."""
        super().__init__(position, body_color)
        self.positions = [self.position]
        self.body_color = body_color
        self.length = 1
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.position = initial_position

    def get_head_position(self):
        """Метод определяющий позицию головы змейки."""
        return self.positions

    def draw(self, surface):
        """Метод отрисовывающий змейку на игровом поле."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Метод сбрасывающий змейку в начальное состояние."""
        self.length = 1
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.positions = [initial_position]
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)

    def update_direction(self):
        """Метод обновляющий направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обновляющий положение змейки."""
        head = self.get_head_position()
        directions = {
            RIGHT: (head[0][0] + GRID_SIZE, head[0][1]),
            LEFT: (head[0][0] - GRID_SIZE, head[0][1]),
            UP: (head[0][0], head[0][1] - GRID_SIZE),
            DOWN: (head[0][0], head[0][1] + GRID_SIZE)
        }
        self.head = directions[self.direction]
        x, y = self.head
        if self.head in self.positions:
            self.reset()
        """Проверка на столкновение с самой собой."""
        if x < 0:
            x = SCREEN_WIDTH - GRID_SIZE
        elif x >= SCREEN_WIDTH:
            x = 0
        if y < 0:
            y = SCREEN_HEIGHT - GRID_SIZE
        elif y >= SCREEN_HEIGHT:
            y = 0
        """Определение границ игрового поля с возможностью
        прохождения 'сквозь стены'."""
        if len(self.positions) > self.length:
            self.positions.pop(-1)
        self.last = self.positions[-1]
        self.positions.insert(0, (x, y))


def handle_keys(game_object):
    """Функция принимающая управление змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция определяющая и описывающая логику игры."""
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    # Тут опишите основную логику игры.
    while True:
        clock.tick(SPEED)
        apple.draw(screen)
        snake.draw(screen)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        pygame.display.update()
        """Удлиннение змейки."""
        if snake.head == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        """Сброс змейки."""
        if snake.head in snake.positions[-1]:
            snake.reset()


if __name__ == '__main__':
    main()
"""Условный оператор запускающий код напрямую."""
