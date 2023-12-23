import os
import pygame

# глобальные переменные
pygame.init()
WIDTH, HEIGHT = 600, 400
# WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# константы
FPS = 60
SPEED = 10  # px/frame speed of player

player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

BULLETEVENT = pygame.USEREVENT + 1


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
    types = [
        (load_image("enemyr.png"), 1),
        (load_image("enemyb.png"), 2),
        (load_image("enemyg.png"), 3),
    ]

    def __init__(self, type, pos_x, pos_y):
        super().__init__(enemy_group)
        self.image, self.bul_speed = Enemy.types[type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.rect.x -= self.rect.w // 2
        self.rect.y -= self.rect.h // 2

    def update(self):
        global running
        if pygame.sprite.spritecollideany(self, player_bullets):
            enemy_group.remove(self)
        Bullet("bullet.png", self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h, 0, self.bul_speed)


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(player_group)
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.rect.x -= self.rect.w // 2
        self.rect.y -= self.rect.h // 2

    def update(self):
        global running
        if pygame.sprite.spritecollideany(self, enemy_bullets):
            running = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, vx, vy, whose=0):  # whose = 0 - вражеская 1 - своя
        super().__init__(bullet_group)
        if whose == 0:
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
        global running
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


level = "q.txt"
with open("data/" + level) as f:
    q = f.readlines()
    x = WIDTH / (len(q[0]) - 1)
    y = HEIGHT / len(q)
    for i, line in enumerate(q):
        for j, char in enumerate(line[:-1]):
            if char == "@":
                player = Player("player.png", x * j + x / 2, y * i + y / 2)
            elif char != ".":
                Enemy(int(char), x * j + x / 2, y * i + y / 2)

pygame.time.set_timer(BULLETEVENT, 500)
vx = vy = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                vx -= SPEED
            if event.key == pygame.K_RIGHT:
                vx += SPEED
            if event.key == pygame.K_UP:
                vy -= SPEED
            if event.key == pygame.K_DOWN:
                vy += SPEED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                vx += SPEED
            if event.key == pygame.K_RIGHT:
                vx -= SPEED
            if event.key == pygame.K_UP:
                vy += SPEED
            if event.key == pygame.K_DOWN:
                vy -= SPEED
        if event.type == BULLETEVENT:
            bullet = Bullet(
                "bullet.png", player.rect.x + player.rect.w // 2, player.rect.y, 0, -20, 1
            )
            enemy_group.update()

    # движение игрока
    player.rect.x += vx
    player.rect.y += vy
    player.rect.x = max(0, min(WIDTH - player.rect.w, player.rect.x))
    player.rect.y = max(0, min(HEIGHT - player.rect.h, player.rect.y))

    screen.fill(255)
    player_group.update()
    player_group.draw(screen)

    bullet_group.update()
    bullet_group.draw(screen)

    enemy_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
