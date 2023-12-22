import os

import pygame

# константы
WIDTH = 600
HEIGHT = 400
FPS = 60
SPEED = 10  # px/frame speed of player

# глобальные переменные
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

BULLETEVENT = pygame.USEREVENT + 1


def load_image(name, color_key=-1):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Enemy(pygame.sprite.Sprite):
    pass


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(player_group)
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, vx, vy):
        super().__init__(bullet_group)
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.vx = vx
        self.vy = vy

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.x + self.rect.w < 0 or self.rect.y + self.rect.h < 0 or self.rect.x > WIDTH or self.rect.y > HEIGHT:
            bullet_group.remove(self)


class Present(pygame.sprite.Sprite):
    pass


player = Player("player.png", 200, 200)
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
            bullet = Bullet("bullet.png", player.rect.x, player.rect.y, 0, -10)

    # движение игрока
    player.rect.x += vx
    player.rect.y += vy
    player.rect.x = max(0, min(WIDTH - player.rect.w, player.rect.x))
    player.rect.y = max(0, min(HEIGHT - player.rect.h, player.rect.y))

    screen.fill(255)
    player_group.draw(screen)

    bullet_group.update()
    bullet_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
