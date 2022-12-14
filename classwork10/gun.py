import math
from random import choice, randint

import pygame


FPS = 30

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 300

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= 5
        self.x += self.vx
        self.y -= self.vy
        if self.x + self.r >= 780:
            self.x = 780 - self.r
            self.vx = -self.vx

        if self.y + self.r >= 580:
            self.y = 580 - self.r
            self.vy = -self.vy

        if self.x - self.r <= 10:
            self.x = 10 + self.r
            self.vx = -self.vx

        if self.y - self.r <= 20:
            self.y = 20 + self.r
            self.vy = -self.vy

        self.live -= 1


    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x - obj.x)**2 + (self.y - obj.y)**2)**0.5 <= obj.r:
            return True
        else:
            return False

    def deleted(self):
        del self


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = BLACK

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] == 20:
                self.an = -10000000000000000
            else:
                self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = YELLOW
        else:
            self.color = BLACK

    def draw(self):
        pygame.draw.line(self.screen, self.color, (20, 450),
                         (20 + (10 + self.f2_power//1.5) * math.cos(self.an),
                         450 + (10 + self.f2_power//1.5) * math.sin(self.an)),
                         7 + self.f2_power//30)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = YELLOW
        else:
            self.color = BLACK


class Target():
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(20, 100)
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)
        self.color = RED
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points
        del self

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r >= 780:
            self.x = 780 - self.r
            self.vx = -self.vx

        if self.y + self.r >= 580:
            self.y = 580 - self.r
            self.vy = -self.vy

        if self.x - self.r <= 10:
            self.x = 10 + self.r
            self.vx = -self.vx

        if self.y - self.r <= 20:
            self.y = 20 + self.r
            self.vy = -self.vy


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    target.move()
    text_surface = my_font.render(f'{target.points}', False, (0, 0, 0))
    screen.blit(text_surface, (10, 5))
    for b in balls:
        b.draw()

    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    i = 0
    while i < len(balls):
        balls[i].move()
        if balls[i].hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
        if balls[i].live == 0:
            del balls[i]
        i += 1
    gun.power_up()
pygame.quit()
