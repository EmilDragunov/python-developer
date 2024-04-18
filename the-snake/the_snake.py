from random import choice, randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SNAKE_START = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

SPEED = 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Родительский класс GameObject."""

    def __init__(self, position=SNAKE_START, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод draw класса GameObject."""

    def create_cell(self, position, color, width):
        """Метод create_cell класса GameObject"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect, width)


class Apple(GameObject):
    """Дочерний класс Apple."""

    def __init__(self, body_color=APPLE_COLOR):
        self.body_color = body_color
        self.position = ((randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                         (randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
        self.randomize_position()

    def randomize_position(self):
        """Метод randomize_position класса Apple."""
        self.position = ((randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                         (randint(0, GRID_HEIGHT - 1) * GRID_SIZE))

    def draw(self):
        """Метод draw класса Apple."""
        self.create_cell(self.position, self.body_color, 0)
        self.create_cell(self.position, BORDER_COLOR, 1)


class Snake(GameObject):
    """Дочерний класс Snake."""

    def __init__(self, positions=[SNAKE_START]):
        self.positions = positions
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.position = self.positions[0]
        self.last = None
        self.reset()

    def update_direction(self, course):
        """Метод update_direction класса Snake."""
        self.direction = course

    def move(self):
        """Метод move класса Snake."""
        head_x, head_y = self.get_head_position()
        x = (head_x + (self.direction[0] * GRID_SIZE)) % SCREEN_WIDTH
        y = (head_y + (self.direction[1] * GRID_SIZE)) % SCREEN_HEIGHT
        new_pos = (x, y)
        self.positions.insert(0, new_pos)
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.remove(self.last)
        if self.positions[0] in self.positions[2:]:
            self.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Метод draw класса Snake."""
        self.create_cell(self.positions[0], self.body_color, 0)
        self.create_cell(self.positions[0], BORDER_COLOR, 1)
        if self.last:
            self.create_cell(self.last, BOARD_BACKGROUND_COLOR, 0)

    def get_head_position(self):
        """Метод get_head_position класса Snake."""
        return self.positions[0]

    def reset(self):
        """Метод reset класса Snake."""
        self.length = 1
        self.positions = [SNAKE_START]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Функция обрабатывает нажатие клавиш"""
    for event in pygame.event.get():
        control = {(LEFT, pygame.K_UP): UP,
                   (RIGHT, pygame.K_UP): UP,
                   (LEFT, pygame.K_DOWN): DOWN,
                   (RIGHT, pygame.K_DOWN): DOWN,
                   (UP, pygame.K_LEFT): LEFT,
                   (DOWN, pygame.K_LEFT): LEFT,
                   (UP, pygame.K_RIGHT): RIGHT,
                   (DOWN, pygame.K_RIGHT): RIGHT}
        if event.type == pygame.KEYDOWN:
            course = control.get((game_object.direction, event.key),
                                 game_object.direction)
            game_object.update_direction(course)
        elif event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit


def main():
    """Основной игровой цикл"""
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position()
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
