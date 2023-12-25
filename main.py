import pygame
import random
from game import start_level

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()


click = pygame.mixer.Sound("data/clav.wav")
clav = pygame.mixer.Sound("data/click.ogg")
music = pygame.mixer.Sound("data/strange_cosmos.ogg")


star_field_slow = []
star_field_medium = []
star_field_fast = []
music.play(-1)
for i in range(60):
    star_loc_x = random.randrange(0, width)
    star_loc_y = random.randrange(0, height)
    star_field_slow.append([star_loc_x, star_loc_y])

for i in range(35):
    star_loc_x = random.randrange(0, width)
    star_loc_y = random.randrange(0, height)
    star_field_medium.append([star_loc_x, star_loc_y])

for i in range(25):
    star_loc_x = random.randrange(0, width)
    star_loc_y = random.randrange(0, height)
    star_field_fast.append([star_loc_x, star_loc_y])


WHITE = (255, 255, 255)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

d = {1: "q.txt", 2: "q.txt", 3: "q.txt"}

font = pygame.font.SysFont("Verdana", 60)
fh = pygame.font.SysFont("Verdana", 100)

head = fh.render("Space Shooter", True, CYAN)
text1 = font.render("Sing  in", True, BLUE)
text2 = font.render("  Play  ", True, BLUE)
text3 = font.render("Settings", True, BLUE)


textRect1 = text1.get_rect()
textRect2 = text2.get_rect()
textRect3 = text3.get_rect()
header = head.get_rect()
x = width // 2
y = height // 4 - text1.get_height() // 2

textRect1.center = (x, y + height // 8)
textRect2.center = (x, y + height // 8 + height // 4 - text1.get_height() // 2)
textRect3.center = (x, y + height // 8 + 2 * height // 4 - text1.get_height() // 2)
header.center = (x, head.get_height() // 2)


def choice(f):
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    pygame.display.set_caption("Space Shooter")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 60)
    enter = font.render("Back", True, WHITE)
    enterR = enter.get_rect()
    enterR.center = (width // 8, height // 8 * 7)
    if f == 1:
        font = pygame.font.SysFont("Verdana", 30)
        user_text = ""

        # pygame.draw.rect(screen, YELLOW, (20, 20, width * 2 // 3, 40), 1)

        input_rect = pygame.Rect(20, 20, width * 2 // 3, 40)

        color_active = pygame.Color("lightskyblue")
        color_passive = pygame.Color("gray15")
        color = color_passive
        text_surface = font.render("write your name", True, 0)
        screen.blit(text_surface, (input_rect.x, input_rect.y))
        active = False
        r = True
        while r:

            for event in pygame.event.get():
                if (
                    event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    r = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click.play()
                    if input_rect.collidepoint(event.pos):
                        active = True

                    if enterR.collidepoint(event.pos):
                        r = False
                        start_window()
                if event.type == pygame.KEYDOWN:
                    clav.play()
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[0:-1]
                    else:
                        user_text += event.unicode

            if active:
                color = color_active
            else:
                color = color_passive

            pygame.draw.rect(screen, color, input_rect)

            pygame.draw.rect(screen, WHITE, enterR, 1)
            screen.blit(enter, enterR)

            text_surface = font.render(user_text, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y))
            input_rect.w = max(width * 2 // 3, text_surface.get_width() + 10)
            pygame.display.flip()
            clock.tick(60)
    elif f == 2:
        lev1 = font.render("Level 1", True, BLUE)
        lev2 = font.render("Level 2", True, BLUE)
        lev3 = font.render("Level 3", True, BLUE)
        Rect1 = lev1.get_rect()
        Rect2 = lev2.get_rect()
        Rect3 = lev3.get_rect()
        x = width // 7 + lev1.get_width() // 2
        y = height // 3 + lev1.get_height() // 2

        Rect1.center = (x, y)
        Rect2.center = (x + width // 7 * 2, y)
        Rect3.center = (x + width // 7 * 4, y)

        r = True
        is_level = True
        while r:
            for event in pygame.event.get():
                if (
                    event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    r = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click.play()
                    if Rect1.collidepoint(event.pos):
                        level_n = 1
                        r = False
                    if Rect2.collidepoint(event.pos):
                        level_n = 2
                        r = False
                    if Rect3.collidepoint(event.pos):
                        level_n = 3
                        r = False
                    if enterR.collidepoint(event.pos):
                        r = False
                        start_window()
                        is_level = False

            screen.blit(lev1, Rect1)
            pygame.draw.rect(screen, BLUE, Rect1, 1)
            screen.blit(lev2, Rect2)
            pygame.draw.rect(screen, BLUE, Rect2, 1)
            screen.blit(lev3, Rect3)
            pygame.draw.rect(screen, BLUE, Rect3, 1)

            pygame.draw.rect(screen, WHITE, enterR, 1)
            screen.blit(enter, enterR)

            pygame.display.flip()
            clock.tick(60)
        if is_level:
            start_level(d[level_n])
    elif f == 3:
        pass

    pygame.quit()


def start_window():
    f = 0
    r = True
    while r:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                r = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click.play()
                if textRect1.collidepoint(event.pos):
                    f = 1
                    r = False
                if textRect2.collidepoint(event.pos):
                    f = 2
                    r = False
                if textRect3.collidepoint(event.pos):
                    f = 3
                    r = False

        screen.fill(BLACK)

        for star in star_field_slow:
            star[1] += 1
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, DARKGREY, star, 3)

        for star in star_field_medium:
            star[1] += 4
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, LIGHTGREY, star, 2)

        for star in star_field_fast:
            star[1] += 8
            if star[1] > height:
                star[0] = random.randrange(0, width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, CYAN, star, 1)
        screen.blit(text1, textRect1)
        pygame.draw.rect(screen, BLUE, textRect1, 1)
        screen.blit(text2, textRect2)
        pygame.draw.rect(screen, BLUE, textRect2, 1)
        screen.blit(text3, textRect3)
        pygame.draw.rect(screen, BLUE, textRect3, 1)
        screen.blit(head, header)
        pygame.display.flip()
        clock.tick(60)

    choice(f)


start_window()
