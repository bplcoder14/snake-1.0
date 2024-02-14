import pygame
from pygame.locals import *
import random
import sys

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 213, 0)


def create_unit_surface(color):
    surface = pygame.Surface((38, 38))
    surface.fill(color)
    return surface.convert_alpha()


class Text:

    def __init__(self, text, font_name, font_size, text_color, bg_color, x, y):
        self.text = text
        self.font = pygame.font.Font(font_name, font_size)
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.text_width, self.text_height = self.font.size(self.text)
        self.center = (self.text_width // 2, self.text_height // 2)
        self.x = x
        self.y = y

    def draw(self, surface, width=0, height=0):
        text = self.font.render(self.text, True, self.text_color, self.bg_color)
        surface.blit(text, (self.x - self.center[0] + width, self.y - self.center[1] + height))

    def change_text(self, text):
        self.text = text


class Text_Box:

    def __init__(self, x, y, width, height, text, font_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center = [self.x - (self.width // 2), self.y - (self.height // 2)]
        self.text_pos = self.center
        self.text = text
        self.font_size = font_size
        self.text_obj = Text(self.text, "freesansbold.ttf", self.font_size, WHITE, BLACK, self.center[0],
                             self.center[1])

    def draw(self, surface, text=None):
        if text is not None:
            self.text_obj.change_text(text)
        pygame.draw.rect(surface, WHITE, (self.center, (self.width, self.height)), 5)
        self.text_obj.draw(surface, (self.width // 2), (self.height // 2))


class Text_Button:

    def __init__(self, x, y, width, height, text, font_size, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center = [self.x - (self.width // 2), self.y - (self.height // 2)]
        self.text_pos = self.center
        self.text = text
        self.font_size = font_size
        self.text_obj = Text(self.text, "freesansbold.ttf", self.font_size, WHITE, BLACK, self.center[0],
                             self.center[1])
        self.action = action
        self.hover = False
        self.clicks = 0
        self.mouse_x = pygame.mouse.get_pos()[0]
        self.mouse_y = pygame.mouse.get_pos()[1]
        self.mouse_down = False
        self.hold = True

    def draw(self, surface, mouse_down, text=None):
        self.mouse_down = mouse_down
        self.mouse_x = pygame.mouse.get_pos()[0]
        self.mouse_y = pygame.mouse.get_pos()[1]
        if self.center[0] <= self.mouse_x <= self.center[0] + self.width and self.center[1] <= self.mouse_y <= \
                self.center[1] + self.height:
            self.hover = True
        else:
            self.hover = False
        if text is not None:
            self.text_obj.change_text(text)
        if self.hover:
            pygame.draw.rect(surface, YELLOW, (self.center, (self.width, self.height)), 5)
        else:
            pygame.draw.rect(surface, WHITE, (self.center, (self.width, self.height)), 5)
        self.text_obj.draw(surface, (self.width // 2), (self.height // 2))
        if self.mouse_down and self.hover:
            if not self.hold:
                self.hold = True
                return self.action
            else:
                return
        if not (self.mouse_down and self.hover):
            self.hold = False
            return


class SnakeGame:
    FPS = 30

    def __init__(self):
        self.win = pygame.display.set_mode((798, 798))
        pygame.display.set_caption('SNAKE by bplcoder14')
        self.clock = pygame.time.Clock()
        self.scene = self.Scenes.PLAY
        self.started = False
        self.score = 0
        self.highscore = 0
        self.snake = self.Snake(10, 10, GREEN)
        self.grid = self.Grid(WHITE)
        self.action = None
        self.mouse_down = False
        self.score_text = Text("SCORE: 0", "freesansbold.ttf", 20, WHITE, BLACK, 399, 300)
        self.high_score_text = Text("HIGHSCORE: 0", "freesansbold.ttf", 20, WHITE, BLACK, 399, 200)
        self.play_again_button = Text_Button(399, 400, 200, 100, "PLAY AGAIN", 10, self.Actions.PLAY_AGAIN)
        self.apple = self.Apple()

    class Scenes:
        PLAY = 1
        RESULT = 2

    class Actions:
        PLAY_GAME = 0
        PLAY_AGAIN = 3

    class Grid:

        def __init__(self, color):
            self.size = 21
            self.unit_size = 38
            self.color = color

        def draw(self, surface):
            for row in range(self.size):
                for unit in range(self.size):
                    pygame.draw.rect(surface, self.color,
                                     ((unit * self.unit_size, row * self.unit_size), (self.unit_size, self.unit_size)),
                                     1)

    class Apple:

        def __init__(self):
            self.x = random.randint(0, 20)*38
            self.y = random.randint(0, 20)*38
            self.color = YELLOW

        def check_eaten(self, snake):
            if self.x == snake.body[0].x and self.y == snake.body[0].y:
                snake.grow()
                self.x = random.randint(0, 20) * 38
                self.y = random.randint(0, 20) * 38
                for snake_body_part in snake.body:
                    if self.x == snake_body_part.x and self.y == snake_body_part.y:
                        self.x = random.randint(0, 20) * 38
                        self.y = random.randint(0, 20) * 38
                    else:
                        break

        def draw(self, surface):
            pygame.draw.rect(surface, self.color, ((self.x, self.y), (38, 38)))

    class Snake:

        def __init__(self, x, y, color):
            self.color = color
            self.body = [self.BodyPart(x * 38, y * 38, True), self.BodyPart(x * 38 + 38, y * 38)]
            self.length = 0
            self.move_delay = 0
            self.dead = False

        class BodyPart:

            def __init__(self, x, y, is_head=False):
                self.x = x
                self.y = y
                self.facing = self.Directions.LEFT
                self.body_part = create_unit_surface(GREEN)
                self.is_head = is_head

            class Directions:
                LEFT = 0
                RIGHT = 1
                UP = 2
                DOWN = 3

            def move(self, body_part=None):
                if self.is_head:
                    if self.facing == self.Directions.LEFT:
                        self.x -= 38
                    elif self.facing == self.Directions.RIGHT:
                        self.x += 38
                    elif self.facing == self.Directions.UP:
                        self.y -= 38
                    elif self.facing == self.Directions.DOWN:
                        self.y += 38
                else:
                    self.facing = body_part.facing
                    self.x = body_part.x
                    self.y = body_part.y

            def draw(self, surface):
                surface.blit(self.body_part, (self.x, self.y))

        def grow(self):
            if self.length == 0:
                if self.body[0].facing == self.BodyPart.Directions.LEFT:
                    self.body.append(self.BodyPart(self.body[0].x + 38, self.body[0].y))
                elif self.body[0].facing == self.BodyPart.Directions.RIGHT:
                    self.body.append(self.BodyPart(self.body[0].x - 38, self.body[0].y))
                elif self.body[0].facing == self.BodyPart.Directions.UP:
                    self.body.append(self.BodyPart(self.body[0].x, self.body[0].y + 38))
                elif self.body[0].facing == self.BodyPart.Directions.DOWN:
                    self.body.append(self.BodyPart(self.body[0].x, self.body[0].y - 38))
            else:
                if self.body[len(self.body)-1].facing == self.BodyPart.Directions.LEFT:
                    self.body.append(self.BodyPart(self.body[len(self.body)-1].x + 38, self.body[len(self.body)-1].y))
                elif self.body[len(self.body)-1].facing == self.BodyPart.Directions.RIGHT:
                    self.body.append(self.BodyPart(self.body[len(self.body)-1].x - 38, self.body[len(self.body)-1].y))
                elif self.body[len(self.body)-1].facing == self.BodyPart.Directions.UP:
                    self.body.append(self.BodyPart(self.body[len(self.body)-1].x, self.body[len(self.body)-1].y + 38))
                elif self.body[len(self.body)-1].facing == self.BodyPart.Directions.DOWN:
                    self.body.append(self.BodyPart(self.body[len(self.body)-1].x, self.body[len(self.body)-1].y - 38))
            self.length += 1

        def move(self):
            if self.body[0].x / 38 == 21:
                self.body[0].x = 0
            elif self.body[0].x == -38:
                self.body[0].x = 20 * 38
            elif self.body[0].y / 38 == 21:
                self.body[0].y = 0
            elif self.body[0].y == -38:
                self.body[0].y = 20 * 38
            if self.move_delay == 3:
                self.move_delay = 0
                for body_part in self.body:
                    if self.body[0] != body_part:
                        if (self.body[0].x, self.body[0].y) == (body_part.x, body_part.y):
                            self.dead = True
                for body_part in reversed(self.body):
                    if self.body.index(body_part) > 0:
                        body_part.move(self.body[self.body.index(body_part)-1])
                    else:
                        body_part.move()
            else:
                self.move_delay += 1

        def draw(self, surface):
            if not self.dead:
                self.body[0].draw(surface)
                for body_part in self.body:
                    body_part.draw(surface)

    def play_scene(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_a] and self.snake.body[0].facing != self.snake.BodyPart.Directions.RIGHT:
            self.snake.body[0].facing = self.snake.body[0].Directions.LEFT
        elif key_pressed[K_d] and self.snake.body[0].facing != self.snake.BodyPart.Directions.LEFT:
            self.snake.body[0].facing = self.snake.body[0].Directions.RIGHT
        elif key_pressed[K_w] and self.snake.body[0].facing != self.snake.BodyPart.Directions.DOWN:
            self.snake.body[0].facing = self.snake.body[0].Directions.UP
        elif key_pressed[K_s] and self.snake.body[0].facing != self.snake.BodyPart.Directions.UP:
            self.snake.body[0].facing = self.snake.body[0].Directions.DOWN
        if key_pressed[K_SPACE]:
            self.started = True
        if self.started:
            self.snake.move()
            self.apple.check_eaten(self.snake)
            self.apple.draw(self.win)
        self.snake.draw(self.win)
        self.grid.draw(self.win)

    def result_scene(self):
        buttons = [self.play_again_button]
        texts = [self.score_text, self.high_score_text]
        for text in texts:
            text.draw(self.win)
        for button in buttons:
            self.action = button.draw(self.win, self.mouse_down)
            if self.action is not None:
                break

    def update_scores(self):
        self.score = self.snake.length
        highscore_file = open("highscore.txt", "r")
        self.highscore = int(highscore_file.readline())
        highscore_file.close()
        if self.score > self.highscore:
            self.highscore = self.score
            highscore_file = open("highscore.txt", "w")
            highscore_file.write(str(self.score))
            highscore_file.close()
        self.score_text.change_text(f"SCORE: {self.score}")
        self.high_score_text.change_text(f"HIGHSCORE: {self.highscore}")

    def run(self):
        while True:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        print(self.snake.length)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down = True
                else:
                    self.mouse_down = False
            self.win.fill(BLACK)
            if self.scene == self.Scenes.PLAY:
                self.play_scene()
            elif self.scene == self.Scenes.RESULT:
                self.result_scene()
            if self.action == self.Actions.PLAY_AGAIN:
                self.scene = self.Scenes.PLAY
            if self.snake.dead:
                self.update_scores()
                self.snake = self.Snake(10, 10, GREEN)
                self.apple = self.Apple()
                self.scene = self.Scenes.RESULT
            self.action = None
            pygame.display.flip()


game = SnakeGame()
game.run()
