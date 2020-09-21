import pygame


# COLORS TO BE USED IN GAME

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
OLIVE = (128, 128, 0)
PINK = (255, 20, 147)
# GAME AREA

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
PLAY_AREA_X = 500
PLAY_AREA_Y = 700
POS_AREA_X = [(SCREEN_WIDTH - PLAY_AREA_X) / 2, (SCREEN_WIDTH - PLAY_AREA_X) / 2 + PLAY_AREA_X]
POS_AREA_Y = [(SCREEN_HEIGHT - PLAY_AREA_Y) / 2, (SCREEN_HEIGHT - PLAY_AREA_Y) / 2 + PLAY_AREA_Y]
# PADDLE PROPERTIES

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_COLOR = GREEN
PADDLE_Y_POS = 700
# BALL PROPERTIES

BALL_COLOR = WHITE
BALL_RADIUS = 7
BALL_LATERAL_SPEED = 5
BALL_HORIZONTAL_SPEED = 3
# TARGET PROPERTIES

TARGET_COLOR = [RED, GREEN, BLUE, YELLOW, ORANGE, PINK, OLIVE]
TARGET_HEIGHT = 15
TARGET_AMOUNT = 8
TARGET_Y_START_POS = 75
GAP_SIZE = 13
TARGET_WIDTH = 480 / TARGET_AMOUNT - GAP_SIZE / 2

FPS = 120


class Game:
    def __init__(self):
        self.screen_height = SCREEN_HEIGHT
        self.screen_width = SCREEN_WIDTH

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def have_we_won(self, target):
        sum = 0
        win = len(TARGET_COLOR) * TARGET_AMOUNT * - 50
        for i in range(len(target)):
            for j in target[i]:
                sum += j.y
        if sum == win:
            return True
        else:
            return False

    def have_we_lost(self, ball):
        if ball.y >= POS_AREA_Y[1] - 10:
            return True
        else:
            return False

    def create_targets(self):
        target_list = []
        for j, eni in enumerate(TARGET_COLOR):
            new_list = []
            for i in range(TARGET_AMOUNT):
                color = TARGET_COLOR[j]
                x = POS_AREA_X[0] + 10 + (TARGET_WIDTH + GAP_SIZE / 2) * i
                y = POS_AREA_Y[0] + 50 + (TARGET_HEIGHT + GAP_SIZE / 2) * j
                width = TARGET_WIDTH
                height = TARGET_HEIGHT
                target = Targets(int(y), color, int(x), int(width), height, self.screen)
                new_list.append(target)
            target_list.append(new_list)
        return target_list

    def run(self):
        pygame.init()
        target_list = self.create_targets()
        master_paddle = Paddle(500, 700, self.screen)
        master_ball = Ball(500, 400, self.screen)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
            clock = pygame.time.Clock()

            self.draw_screen(master_paddle, master_ball, target_list)
            self.paddle_hit(master_paddle, master_ball)
            for i in range(len(target_list)):
                for targets in target_list[i]:
                    self.target_hit(targets, master_ball)
            if self.have_we_won(target_list):
                break
            if self.have_we_lost(master_ball):
                break
            clock.tick(FPS)

    def draw_screen(self, paddle, ball, target):
        self.screen.fill(BLACK)
        #DRAW GAME AREA
        pygame.draw.rect(self.screen, WHITE, (int((SCREEN_WIDTH - PLAY_AREA_X) / 2), int((SCREEN_HEIGHT - PLAY_AREA_Y) / 2),
                                         PLAY_AREA_X, PLAY_AREA_Y), 5)
        #DRAW PADDLE

        paddle.move_paddle()
        paddle.draw_paddle()

        #DRAW BALL
        ball.move()
        ball.draw_ball()

        #DRAW TARGET
        for i in range(len(target)):
            for targets in target[i]:
                targets.draw_target()
        pygame.display.update()

    def paddle_hit(self, paddle, ball):
        if not ball.x + ball.radius <= paddle.x - (PADDLE_WIDTH / 2) and not ball.x - ball.radius >= paddle.x + \
                                                                             (PADDLE_WIDTH / 2):
            if not ball.y + ball.radius <= PADDLE_Y_POS:
                ball.y_step *= -1

    def target_hit(self, target, ball):
        if not ball.x + ball.radius <= target.x and not ball.x - ball.radius >= target.x + target.width:
            if ball.y - ball.radius <= target.y + target.height:
                ball.y_step *= -1
                target.y = -50


class Ball:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.x_step = BALL_HORIZONTAL_SPEED
        self.y_step = BALL_LATERAL_SPEED
        self.color = BALL_COLOR
        self.radius = BALL_RADIUS
        self.screen = screen

    def move(self):
        self.x += self.x_step
        self.y += self.y_step

        if not POS_AREA_X[0] + self.radius <= self.x <= POS_AREA_X[1] - self.radius:
            self.x_step *= -1
        if not POS_AREA_Y[0] + self.radius <= self.y <= POS_AREA_Y[1] - self.radius:
            self.y_step *= -1

    def draw_ball(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)


class Paddle:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.paddle_width = PADDLE_WIDTH
        self.paddle_color = PADDLE_COLOR
        self.paddle_height = PADDLE_HEIGHT
        self.screen = screen

    def move_paddle(self):
        self.x, self.y = pygame.mouse.get_pos()

    def draw_paddle(self):
        if self.x >= POS_AREA_X[1] - PADDLE_WIDTH / 2:
            pygame.draw.rect(self.screen, PADDLE_COLOR, (int(POS_AREA_X[1] - PADDLE_WIDTH), PADDLE_Y_POS, PADDLE_WIDTH, PADDLE_HEIGHT))
        elif self.x <= POS_AREA_X[0] + PADDLE_WIDTH / 2:
            pygame.draw.rect(self.screen, PADDLE_COLOR, (int(POS_AREA_X[0]), PADDLE_Y_POS, PADDLE_WIDTH, PADDLE_HEIGHT))
        else:
            pygame.draw.rect(self.screen, PADDLE_COLOR, (int(self.x - PADDLE_WIDTH / 2), PADDLE_Y_POS, PADDLE_WIDTH, PADDLE_HEIGHT))


class Targets:
    def __init__(self, y, color, x, width, height, screen):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.screen = screen

    def draw_target(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 4)


def main():
    breakout = Game()
    breakout.run()


if __name__ == "__main__":
    main()
