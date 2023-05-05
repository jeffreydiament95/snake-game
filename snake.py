import pygame
import sys
import random
from pygame.locals import *

pygame.init()

# Define game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 10

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)

    def move(self):
        head_x, head_y = self.positions[0]
        new_x, new_y = self.direction
        new_head = (head_x + new_x, head_y + new_y)

        self.positions.insert(0, new_head)
        self.positions.pop()

    def grow(self):
        tail_x, tail_y = self.positions[-1]
        new_tail = (tail_x - self.direction[0], tail_y - self.direction[1])
        self.positions.append(new_tail)

    def change_direction(self, new_direction):
        if not (new_direction[0] * -1, new_direction[1] * -1) == self.direction:
            self.direction = new_direction


class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def respawn(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

class Button:
    def __init__(self, text, x, y, width, height, color, font_size=36):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.font_size = font_size

    def draw(self, surface):
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width // 2, self.y + self.height // 2)
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 2)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height


def draw_grid():
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(window, WHITE, rect, 1)


def draw_snake(snake):
    for position in snake.positions:
        rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(window, GREEN, rect)


def draw_food(food):
    rect = pygame.Rect(food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(window, RED, rect)


def check_collision(snake, food):
    if snake.positions[0] == food.position:
        snake.grow()
        food.respawn()
        return True
    return False


def check_game_over(snake):
    head = snake.positions[0]
    if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
        return True
    if head in snake.positions[1:]:
        return True
    return False

def show_game_over_screen():
    font = pygame.font.Font(None, 36)
    text_surface = font.render("GAME OVER, LOSER", True, RED)
    text_rect = text_surface.get_rect()
    text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100)

    replay_button = Button("Replay", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, 200, 50, WHITE)
    quit_button = Button("Quit", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50, 200, 50, WHITE)

    while True:
        window.fill((0, 0, 0))
        window.blit(text_surface, text_rect)
        replay_button.draw(window)
        quit_button.draw(window)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if replay_button.is_clicked(mouse_x, mouse_y):
                    return True
                elif quit_button.is_clicked(mouse_x, mouse_y):
                    return False

def main():
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.locals.KEYDOWN:
                if event.key == K_UP:
                    snake.change_direction((0, -1))
                elif event.key == K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == K_RIGHT:
                    snake.change_direction((1, 0))

        snake.move()
        if check_collision(snake, food):
            continue

        if check_game_over(snake):
            if show_game_over_screen():
                snake = Snake()
                food = Food()
            else:
                pygame.quit()
                sys.exit()

        window.fill((0, 0, 0))
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
