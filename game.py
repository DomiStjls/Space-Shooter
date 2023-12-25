import os

import pygame

# константы
FPS = 60

SPEED = 10
DURATION = 100
enemies = [
    (0, "enemyr.png", "bullet.png", 1000, [(0, 10)]),
    (1, "enemyg.png", "bullet.png", 750, [(2, 15), (-2, 15)]),
    (2, "enemyb.png", "bullet.png", 1500, [(0, 10), (3, 20), (-3, 20)]),
]
players = [
    (0, "player.png", 10, "bullet.png", 100, [(0, -20)])
]

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

events = {}
running = False


def load_image(name, color_key=-1):
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
    return image


class Enemy(pygame.sprite.Sprite):

    def __init__(self, type, pos_x, pos_y):
        super().__init__(enemy_group)
        self.type, image, self.bullet_filename, duration, self.speeds = enemies[type]
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
            for key, value in events.items():
                if value == self:
                    del events[key]
                    break

    def shoot(self):
        for x, y in self.speeds:
            Bullet(self.bullet_filename, self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h, x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type=0):
        super().__init__(player_group)
        self.type, player_filename, self.speed, self.bullet_filename, duration, self.speeds = players[type]
        self.image = load_image(player_filename)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.rect.x -= self.rect.w // 2
        self.rect.y -= self.rect.h // 2

        EVENT = pygame.USEREVENT + len(events) + 1
        pygame.time.set_timer(EVENT, duration)
        events[EVENT] = self

    def update(self):
        global running
        if pygame.sprite.spritecollideany(self, enemy_bullets):
            running = False

    def shoot(self):
        for x, y in self.speeds:
            Bullet(self.bullet_filename, self.rect.x + self.rect.w // 2, self.rect.y, x, y, 1)


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
    pass


def start_level(level):
    global events, running
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
                if event.key == pygame.K_LEFT:
                    vx -= player.speed
                if event.key == pygame.K_RIGHT:
                    vx += player.speed
                if event.key == pygame.K_UP:
                    vy -= player.speed
                if event.key == pygame.K_DOWN:
                    vy += player.speed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    vx += player.speed
                if event.key == pygame.K_RIGHT:
                    vx -= player.speed
                if event.key == pygame.K_UP:
                    vy += player.speed
                if event.key == pygame.K_DOWN:
                    vy -= player.speed
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

        if not events:
            running = False

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    start_level("q.txt")
