import pygame
import random


pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()


star_field_slow = []
star_field_medium = []
star_field_fast = []

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


pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
if f == 1:
    font = pygame.font.SysFont("Verdana", 30)
    user_text = ""

    # pygame.draw.rect(screen, YELLOW, (20, 20, width * 2 // 3, 40), 1)

    input_rect = pygame.Rect(20, 20, width * 2 // 3, 40)

    color_active = pygame.Color("lightskyblue")
    color_passive = pygame.Color("gray15")
    color = color_passive
    text_surface = font.render("write your name", True, (255, 255, 255))
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
                if input_rect.collidepoint(event.pos):
                    active = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[0:-1]
                else:
                    user_text += event.unicode

        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(screen, color, input_rect)

        text_surface = font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y))
        input_rect.w = max(width * 2 // 3, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)
elif f == 2:
    import game


pygame.quit()
