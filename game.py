import os
import random

import pygame

# тип врага, картинка врага, картинка пули, папка с анимацией, время между выстрелами, скорости пуль(по Х и по У), очки за убийство врага
enemies = [
    (0, "enemy1.png", "bullet.png", "animation1", 1500, [(0, 5)], 10),
    (1, "enemy2.png", "bullet.png", "animation1", 2500, [(0, 20)], 20),
    (2, "enemy3.png", "bullet.png", "animation1", 3500, [(1, 6), (-1, 6), (0, 7)], 30),
]

# тип игрока, картинка игрока, картинка пули, время между выстрелами, скорости пуль по осям
players = [
    (0, "playerr.png", "bulletr.png", 100, [(0, -10)]),
    (1, "playerg.png", "bulletg.png", 500, [(0, -10), (1, -10), (-1, -10)]),
    (2, "playerb.png", "bulletb.png", 1000, [(0, -5), (1, -5), (2, -5), (-1, -5), (-2, -5)])
]

# тип подарка, изображение подарка, скорость
presents = [
    (0, "presentr.png", (0, 2)),
    (1, "presentg.png", (0, 2)),
    (2, "presentb.png", (0, 2)),
    (3, "presentspeed.png", (0, 2)),
    (4, "presenttime.png", (0, 2)),
]

pygame.init()
# разрешение экрана
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
# WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

player = None
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
presents_group = pygame.sprite.Group()
animation_group = pygame.sprite.Group()
score = 0
events = {}
running = False


def load_image(name, color_key=-1, width=50, height=50):
    # функция, которая загружает изображение из файла name и масштабирует его до width и height

    # открытие
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot load image:", name)
        raise SystemExit(message)

    # удаление заднего фона, если нужно
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    # масштабирование
    return pygame.transform.scale(image, (width, height))


class Enemy(pygame.sprite.Sprite):
    # класс врагов
    def __init__(self, type, pos_x, pos_y):
        super().__init__(enemy_group)
        self.type, image, self.bullet_filename, self.folder, duration, self.speeds, self.points = enemies[type]
        self.image = load_image(image, -1, 50, 50)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.rect.x -= self.rect.w // 2
        self.rect.y -= self.rect.h // 2

        # событие, чтобы персонаж стрелял
        EVENT = pygame.USEREVENT + len(events) + 1
        pygame.time.set_timer(EVENT, duration)
        events[EVENT] = self

    def update(self):
        global score
        if pygame.sprite.spritecollide(self, player_bullets, False, pygame.sprite.collide_mask):
            # при столкновении с пулями игрока, враг удаляется и запускается анимация
            enemy_group.remove(self)
            Animation(self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h, self.folder)
            # начисление очков за убитого врага
            score += self.points
            # выпадает подарок с определенной вероятностью
            Present(self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h // 2, random.randint(0, 10))
            # удаляется событие для стрельбы
            for key, value in events.items():
                if value == self:
                    del events[key]
                    break

    def shoot(self):
        # создаются пули с заданными скоростями
        for x, y in self.speeds:
            Bullet(self.bullet_filename, self.rect.x + self.rect.w // 2, self.rect.y + self.rect.h, x, y)


class Player(pygame.sprite.Sprite):
    # класс игрока
    def __init__(self, pos_x, pos_y, type=0):
        super().__init__(player_group)
        self.k = 1
        self.EVENT = pygame.USEREVENT + len(events) + 1
        events[self.EVENT] = self
        self.set_type(type)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.rect.x -= self.rect.w // 2
        self.rect.y -= self.rect.h // 2

    def set_type(self, type=0):
        # метод меняет(задает) тип игрока
        self.type, player_filename, self.bullet_filename, self.duration, self.speeds = players[type]
        self.image = load_image(player_filename, -1, 70, 70)
        self.mask = pygame.mask.from_surface(self.image)
        self.set_duration(self.duration)

    def set_duration(self, dur):
        # метод меняет задержку между пулями
        self.duration = dur
        pygame.time.set_timer(self.EVENT, dur)

    def update(self):
        global running
        if pygame.sprite.spritecollide(self, enemy_bullets, False, pygame.sprite.collide_mask):
            # при столкновении остановить игру
            running = False

    def shoot(self):
        # создаются пули с заданными скоростями, умноженными на коэффициент, который меняется при получении подарка
        for x, y in self.speeds:
            Bullet(self.bullet_filename, self.rect.x + self.rect.w // 2, self.rect.y, x * self.k, self.k * y, 1)


class Bullet(pygame.sprite.Sprite):
    # класс пуль
    def __init__(self, image, pos_x, pos_y, vx, vy, whose=0):  # whose = 0 - вражеская, 1 - своя
        super().__init__(bullet_group)
        if not whose:
            enemy_bullets.add(self)
        else:
            player_bullets.add(self)
        self.image = load_image(image, -1, 30, 30)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.rect.x -= self.rect.w // 2
        self.rect.y -= self.rect.h // 2
        self.vx = vx
        self.vy = vy
        self.whose = whose

    def update(self):
        # изменение координат пули
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (
                self.rect.x + self.rect.w < 0
                or self.rect.y + self.rect.h < 0
                or self.rect.x > WIDTH
                or self.rect.y > HEIGHT
        ):
            # если пуля вышла за границы экрана, то она исчезает
            bullet_group.remove(self)


class Present(pygame.sprite.Sprite):
    # класс подарков
    """
    types:
    0) меняет тип игрока на 0
    1) меняет тип игрока на 1
    2) меняет тип игрока на 2
    3) увеличивает скорость пуль
    4) уменьшает задержку между пулями
    """

    def __init__(self, x, y, type):
        if not (0 <= type < len(presents)):
            return
        super().__init__(presents_group)
        self.type, image, self.speed = presents[type]
        self.image = load_image(image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(x, y)
        self.rect.x -= self.rect.w // 2
        self.rect.y -= self.rect.h // 2
        self.vx, self.vy = self.speed

    def update(self):
        global player
        # изменение координат
        self.rect.x += self.vx
        self.rect.y += self.vy
        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            # если столкнулся с игроком, то у игрока меняются свойства
            presents_group.remove(self)
            if self.type == 3:
                player.k *= 1.5
            elif self.type == 4:
                player.set_duration(int(player.duration * 0.7))
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
            # если подарок вышел за границы экрана, он исчезает
            presents_group.remove(self)


class Animation(pygame.sprite.Sprite):
    # класс анимаций
    # в папке должны быть файлы 1.png, 2.png, 3.png, ...
    def __init__(self, x, y, folder,
                 n=8):
        super().__init__(animation_group)
        self.images = [load_image(f"{folder}\{i}.png", -1, 100, 100) for i in range(1, n + 1)]
        self.index = -1
        self.x = x
        self.y = y

    def update(self):
        # следущая картинка
        self.index += 1
        if self.index >= len(self.images):
            # если картинки кончились, то анимация заканчивается
            animation_group.remove(self)
            return
        self.image = self.images[self.index]
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.rect.x -= self.rect.w // 2
        self.rect.y -= self.rect.h // 2


def start_level(level):
    global events, running, score, player, player_group, enemy_group, bullet_group, player_bullets, enemy_bullets, presents_group, animation_group

    # обнуление переменных
    score = 0
    events = {}
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    presents_group = pygame.sprite.Group()
    animation_group = pygame.sprite.Group()

    # загрузка уровня
    with open("data/" + level) as f:
        q = f.readlines()
        x = WIDTH / (len(q[0]) - 1)
        y = HEIGHT / len(q)
        for i, line in enumerate(q):
            for j, char in enumerate(line[:-1]):
                if char != ".":
                    Enemy(int(char), x * j + x / 2, y * i + y / 2)
    player = Player(0, 0)
    background = load_image("background.jpg", None, WIDTH, HEIGHT)

    # игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEMOTION:
                # перемещение игрока
                player.rect.x = event.pos[0] - player.rect.w // 2
                player.rect.y = event.pos[1] - player.rect.h // 2
            elif event.type in events.keys():
                # если сработал один из таймеров, то соответсвующий объект стреляет
                events[event.type].shoot()

        # игрок не выходит за границы
        player.rect.x = max(0, min(WIDTH - player.rect.w, player.rect.x))
        player.rect.y = max(0, min(HEIGHT - player.rect.h, player.rect.y))

        # обновление и рисование спрайтов
        screen.blit(background, (0, 0))

        player_group.update()
        player_group.draw(screen)

        bullet_group.update()
        bullet_group.draw(screen)

        enemy_group.update()
        enemy_group.draw(screen)

        presents_group.update()
        presents_group.draw(screen)

        animation_group.update()
        animation_group.draw(screen)

        if not enemy_group.sprites() and not animation_group.sprites():
            # если все враги убиты и все анимации закончились, то игра завершается
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    # если все враги убиты(в списке событий только одно событие), то начисляются заработанные очки, иначе начисляется ноль
    return score if len(events) == 1 else 0


if __name__ == "__main__":
    print(start_level("q.txt"))
