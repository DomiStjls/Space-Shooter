import pygame

pygame.init()

WIDTH = 500
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()
fon = pygame.transform.scale(
    pygame.image.load("data\base3.png").convert_alpha(), (WIDTH, HEIGHT)
)
bd = pygame.transform.scale(
    pygame.image.load("data\bd.png").convert_alpha(), (WIDTH, HEIGHT)
)
lev = pygame.transform.scale(
    pygame.image.load("data\levels.png").convert_alpha(), (WIDTH, HEIGHT)
)
sett = pygame.transform.scale(
    pygame.image.load("data\set.png").convert_alpha(), (WIDTH, HEIGHT)
)
screen.blit(fon, (0, 0))
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos[0], event.pos[1], event.pos)
            if (
                150 < event.pos[0]
                and event.pos[0] < 330
                and 130 < event.pos[1]
                and event.pos[1] < 190
            ):
                print(1)
                screen.blit(bd, (0, 0))
            if (
                150 < event.pos[0]
                and event.pos[0] < 330
                and 210 < event.pos[1]
                and event.pos[1] < 270
            ):
                print(2)
                screen.blit(lev, (0, 0))
            if (
                150 < event.pos[0]
                and event.pos[0] < 330
                and 290 < event.pos[1]
                and event.pos[1] < 350
            ):
                print(3)
                screen.blit(sett, (0, 0))

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
