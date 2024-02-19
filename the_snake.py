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

initial_position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Тут опишите все классы игры.

"""Родительский класс."""
class GameObject:

    """Родительский конструктор передающий центральную точку и
    дефолтный цвет объектов.
    """
    def __init__(self, position=initial_position, body_color=(0, 0, 0)):
        self.body_color = body_color
        self.position = position
    """Абстрактный родительский метод прорисовки объектов."""
    def draw(self, surface):
        pass


"""Дочерний класс описывающий игровое яблоко."""
class Apple(GameObject):

    """Дочерний конструктор принимающий в себя атрибуты цвета
    и позиции объекта.
    """
    def __init__(self, position=initial_position, body_color=APPLE_COLOR) -> None:
        super().__init__(position, body_color)
        self.position = self.randomize_position()

    """Метод устанавливающий яблоко в случайном порядке."""
    def randomize_position(self):
        return (randint(0, 31) * GRID_SIZE, randint(0, 23) * GRID_SIZE)

    """Метод отрисовывающий яблоко на игрвоом поле."""
    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


"""Дочерний класс определяющий объект: Змейка."""
class Snake(GameObject):

    """Дочерний конструктор  класса Змейка с набором атрибутов
    характеризующих змейку, таких как стартовая позиция, длинна,
    цвет тела, направление движения."""
    def __init__(self, body_color=SNAKE_COLOR, position=initial_position) -> None:
        super().__init__(position, body_color)
        self.positions = [self.position]
        self.body_color = body_color
        self.length = 1
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.position = initial_position

    """Метод определяющий позицию головы змейки."""
    def get_head_position(self):
        return self.positions

    """Метод отрисовывающий змейку на игровом поле."""
    def draw(self, surface):
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

    """Метод сбрасывающий змейку в начальное состояние."""
    def reset(self):
        self.length = 1
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.positions = [initial_position]
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)

    """Метод обновляющий направление движения змейки."""
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    """Метод обновляющий положение змейки, а так же
    добавляющий новую голову или удаляющий последний сегмент."""
    def move(self):
        head = self.get_head_position()

        directions = {
            RIGHT: (head[0][0] + GRID_SIZE, head[0][1]),
            LEFT: (head[0][0] - GRID_SIZE, head[0][1]),
            UP: (head[0][0], head[0][1] - GRID_SIZE),
            DOWN: (head[0][0], head[0][1] + GRID_SIZE)
        }
        self.head = directions[self.direction]
        x, y = self.head
        """Проверка на столкновение с самой собой."""
        if self.head in self.positions:
            self.reset()
        """Определение границ игрового поля с возможностью
        прохождения 'сквозь стены'."""
        if x < 0:
            x = SCREEN_WIDTH - GRID_SIZE
        elif x >= SCREEN_WIDTH:
            x = 0
        if y < 0:
            y = SCREEN_HEIGHT - GRID_SIZE
        elif y >= SCREEN_HEIGHT:
            y = 0
        if len(self.positions) > self.length:
            self.positions.pop(-1)
        self.last = self.positions[-1]
        self.positions.insert(0, (x, y))


"""Функция принимающая управление змейкой и
поддерживающее открытым игровой экран."""
def handle_keys(game_object):
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


"""Функция определяющая и описывающая логику игры."""
def main():
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


'''Условный оператор запускающий код напрямую.'''
if __name__ == '__main__':
    main()
