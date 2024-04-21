from random import choice

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

ALL_CELLS = set(
    (x, y)
    for x in range(0, SCREEN_WIDTH, 20)
    for y in range(0, SCREEN_HEIGHT, 20)
)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (255, 255, 255)

SNAKE_COLOR = (0, 255, 0)

APPLE_COLOR = (255, 0, 0)

INEDIBLE_OBJECT_COLOR = (139, 69, 19)

STONE_COLOR = (128, 128, 128)

YELLOW = (255, 255, 102)

SNAKE_START = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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

    def randomize_position(self, snake_positions):
        random_cell = choice(tuple(ALL_CELLS - set(snake_positions)))
        return random_cell


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
        screen.fill(BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Дочерний класс Apple."""

    def __init__(self, position=SNAKE_START):
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position(position)

    def draw(self):
        """Метод draw класса Apple."""
        self.create_cell(self.position, self.body_color, 0)
        self.create_cell(self.position, BORDER_COLOR, 1)


class InedibleObject(GameObject):
    """Дочерний класс Inedibleobject."""

    def __init__(self, postion=SNAKE_START):
        self.body_color = INEDIBLE_OBJECT_COLOR
        self.position = self.randomize_position(postion)

    def draw(self):
        """Метод draw класса InedibleObject."""
        self.create_cell(self.position, self.body_color, 0)
        self.create_cell(self.position, BORDER_COLOR, 1)


class Stone(GameObject):
    """Дочерний класс Stone."""

    def __init__(self, position=SNAKE_START):
        self.body_color = STONE_COLOR
        self.position = self.randomize_position(position)

    def draw(self):
        """Метод draw класса Stone."""
        self.create_cell(self.position, self.body_color, 0)
        self.create_cell(self.position, BORDER_COLOR, 1)


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
    font_score = pygame.font.SysFont('Arial', 25, bold=True)

    snake = Snake()
    apple = Apple()
    inedible = InedibleObject()
    stone = Stone()
    score = 0

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if (snake.positions[0] in snake.positions[2:]
           or snake.positions[0] == stone.position):
            snake.reset()
            score = 0
            apple.position = apple.randomize_position(SNAKE_START)
            stone.position = stone.randomize_position(SNAKE_START)
        if snake.positions[0] == apple.position:
            snake.length += 1
            score += 1
            apple.position = apple.randomize_position(snake.positions)
        elif snake.positions[0] == inedible.position:
            inedible.position = inedible.randomize_position(snake.positions)
            if len(snake.positions) != 1:
                snake.length -= 1
                score -= 1
                snake.create_cell(snake.last, BOARD_BACKGROUND_COLOR, 0)
                snake.last = snake.positions[-1]
                snake.positions.remove(snake.last)
            else:
                snake.reset()
        snake.draw()
        apple.draw()
        inedible.draw()
        stone.draw()

        screen.blit(font_score.render(f'Score: {score}', True, YELLOW),
                    (0, 0))
        pygame.display.update()


if __name__ == '__main__':
    main()
