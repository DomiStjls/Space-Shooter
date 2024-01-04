import os
import random

import pygame

# константы
FPS = 60
# тип врага, картинка врага, картинка пули, время между выстрелами, скорости пуль(по Х и по У), очки за убийство врага
enemies = [
    (0, "enemyr.png", "bulletr.png", 2000, [(0, 1)], 10),
    (1, "enemyg.png", "bulletg.png", 2000, [(0, 1)], 20),
    (2, "enemyb.png", "bulletb.png", 2000, [(0, 1)], 30),
]

# тип игрока, картинка игрока, скорость игрока, картинка пули, время между выстрелами, скорости пуль по осям
players = [
    (0, "playery.png", 5, "bullety.png", 100, [(0, -10)]),
    (1, "playero.png", 5, "bulleto.png", 200, [(0, -10), (1, -10), (-1, -10)]),
    (2, "playerw.png", 5, "bulletw.png", 200, [(0, -5), (0, -10)])
]

presents = [
    (0, "presenty.png", (0, 2)),
    (1, "presento.png", (0, 2)),
    (2, "presentw.png", (0, 2)),
    (3, "presentspeed.png", (0, 2)),
    (4, "presenttime.png", (0, 2)),
    (5, "presentmove.png", (0, 2)),
]
player = None
# глобальные переменные
pygame.init()
# WIDTH, HEIGHT = 600, 400
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
presents_group = pygame.sprite.Group()
score = 0
events = {}
running = False
bul_dur_k = 1


def load_image(name, color_key=-1, width=20, height=20):
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot load image:", name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return pygame.transform.scale(image, (width, height))


class Enemy(pygame.sprite.Sprite):

    def __init__(self, type, pos_x, pos_y):
        super().__init__(enemy_group)
        self.type, image, self.bullet_filename, duration, self.speeds, self.points = enemies[type]
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.rect.x -= self.rect.w // 2
        self.rect.y -= self.rect.h // 2

        EVENT = pygame.USEREVENT + len(events) + 1
        pygame.time.set_timer(EVENT, duration)
        events[EVENT] = self

    def update(self):
        if pygame.sprite.spritecollideany(self, player_bullets):
            enemy_group.remove(self)
            global score
            score += self.points
            for key, value in events.items():
                if value == self:
                    Present(self.rect.x + self.rect.w, self.rect.y + self.rect.h, random.randint(0, 5))
                    del events[key]
                    break

    def shoot(self):
        for x, y in self.speeds:
            Bullet(self.bullet_filename, self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h, x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type=1):
        super().__init__(player_group)
        self.k = 1
        self.EVENT = pygame.USEREVENT + len(events) + 1
        events[self.EVENT] = self
        self.set_type(type)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.rect.x -= self.rect.w // 2
        self.rect.y -= self.rect.h // 2

    def set_type(self, type=0):
        self.type, player_filename, self.speed, self.bullet_filename, self.duration, self.speeds = players[type]
        self.image = load_image(player_filename)
        self.set_duration(self.duration)

    def set_duration(self, dur):
        self.duration = dur
        pygame.time.set_timer(self.EVENT, dur)

    def update(self):
        global running
        if pygame.sprite.spritecollideany(self, enemy_bullets):
            running = False

    def shoot(self):
        for x, y in self.speeds:
            Bullet(self.bullet_filename, self.rect.x + self.rect.w // 2, self.rect.y, x * self.k, self.k * y, 1)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, vx, vy, whose=0):  # whose = 0 - вражеская, 1 - своя
        super().__init__(bullet_group)
        if not whose:
            enemy_bullets.add(self)
        else:
            player_bullets.add(self)
        self.image = load_image(image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.rect.x -= self.rect.w // 2
        self.rect.y -= self.rect.h // 2
        self.vx = vx
        self.vy = vy
        self.whose = whose

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (
                self.rect.x + self.rect.w < 0
                or self.rect.y + self.rect.h < 0
                or self.rect.x > WIDTH
                or self.rect.y > HEIGHT
        ):
            bullet_group.remove(self)


class Present(pygame.sprite.Sprite):
    # types
    """
    types:
    0) меняет тип игрока на 0
    1) меняет тип игрока на 1
    2) меняет тип игрока на 2
    3) увеличивает скорость пуль
    4) уменьшает задержку между пулями
    5) увеличивает скорость игрока
    """

    def __init__(self, x, y, type):
        super().__init__(presents_group)
        self.type, image, self.speed = presents[type]
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(x, y)
        self.rect.x -= self.rect.w // 2
        self.rect.y -= self.rect.h // 2
        self.vx, self.vy = self.speed

    def update(self):
        global player
        self.rect.x += self.vx
        self.rect.y += self.vy
        if pygame.sprite.spritecollideany(self, player_group):
            presents_group.remove(self)
            if self.type == 3:
                player.k *= 2
            elif self.type == 4:
                player.set_duration(int(player.duration * 0.5))
            elif self.type == 5:
                player.speed *= 2
            elif self.type == 0:
                player.set_type(0)
            elif self.type == 1:
                player.set_type(1)
            elif self.type == 2:
                player.set_type(2)
        if (
                self.rect.x + self.rect.w < 0
                or self.rect.y + self.rect.h < 0
                or self.rect.x > WIDTH
                or self.rect.y > HEIGHT
        ):
            presents_group.remove(self)


def start_level(level):
    global events, running, score, player
    score = 0
    events = {}
    with open("data/" + level) as f:
        q = f.readlines()
        x = WIDTH / (len(q[0]) - 1)
        y = HEIGHT / len(q)
        for i, line in enumerate(q):
            for j, char in enumerate(line[:-1]):
                if char == "@":
                    player = Player(x * j + x / 2, y * i + y / 2)
                elif char != ".":
                    Enemy(int(char), x * j + x / 2, y * i + y / 2)

    vx = vy = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT:
                    vx = -player.speed
                if event.key == pygame.K_RIGHT:
                    vx = player.speed
                if event.key == pygame.K_UP:
                    vy = -player.speed
                if event.key == pygame.K_DOWN:
                    vy = player.speed
            elif event.type == pygame.KEYUP:
                # if event.key == pygame.K_LEFT:
                #     vx = player.speed
                # if event.key == pygame.K_RIGHT:
                #     vx = -player.speed
                # if event.key == pygame.K_UP:
                #     vy = player.speed
                # if event.key == pygame.K_DOWN:
                #     vy = -player.speed
                vx = 0
                vy = 0
            elif event.type in events.keys():
                events[event.type].shoot()

        player.rect.x += vx
        player.rect.y += vy
        player.rect.x = max(0, min(WIDTH - player.rect.w, player.rect.x))
        player.rect.y = max(0, min(HEIGHT - player.rect.h, player.rect.y))

        screen.fill(255)
        player_group.update()
        player_group.draw(screen)

        bullet_group.update()
        bullet_group.draw(screen)

        enemy_group.update()
        enemy_group.draw(screen)

        presents_group.update()
        presents_group.draw(screen)

        if len(events) <= 1:
            running = False

        pygame.display.flip()
        clock.tick(FPS)
    return score if len(events) else 0


if __name__ == "__main__":
    print(start_level("q.txt"))
