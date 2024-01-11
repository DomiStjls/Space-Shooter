import pygame
import random
import sqlite3
from game import start_level

# создание базы данных игроков
connection = sqlite3.connect("data/shooter_bd.db")
cursor = connection.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Players (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    score INTEGER
    );
    """
)
connection.commit()

# начало игры, задание нужных параметров
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
clock = pygame.time.Clock()

# музыка + цвета
click = pygame.mixer.Sound("data/clav.wav")
clav = pygame.mixer.Sound("data/click.ogg")
music = pygame.mixer.Sound("data/strange_cosmos.ogg")
win_mu = pygame.mixer.Sound("data/win.ogg")
lose = pygame.mixer.Sound("data/lose.ogg")
WHITE = (255, 255, 255)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
BLACK = (0, 0, 0)
LIGHTBL = "lightskyblue"
GRAY = "gray15"
BLUE = (0, 0, 255)
GREEN = (100, 255, 10)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
# уровни + шрифты
d = {1: "q.txt", 2: "q.txt", 3: "q.txt"}

font = pygame.font.SysFont("Verdana", 60)
fh = pygame.font.SysFont("Verdana", 100)

# поиск игрока с именем n
def findpers(n):
    query = """
        SELECT name, score
        FROM Players
        WHERE name LIKE ?
    """
    res = cursor.execute(query, [n]).fetchall()
    connection.commit()
    if res == []:
        return [("Записи не найдено.", "")]
    return res


# создание игрока с именем n
def makepers(n):
    query = """
    INSERT INTO Players VALUES(?, ?, ?);
    """
    res = cursor.execute(query, [int(100000 * random.random()), n, 0]).fetchall()
    connection.commit()
    return findpers(n)


def update(n, s):
    query = """
    UPDATE Players
    SET score = score + ?
    WHERE name = ?;
    """
    res = cursor.execute(query, [s, n]).fetchall()
    connection.commit()


def blit_text(screen, text, pos, font, color=pygame.Color(WHITE)):
    words = [word.split(" ") for word in text.splitlines()]
    max_width, max_height = screen.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            screen.blit(word_surface, (x, y))
            x += word_width + font.size(" ")[0]
        x = pos[0]
        y += word_height


# стартавая функция
def start_window():
    click_music = True
    back_music = True
    music_play = True
    end_game = False
    font = pygame.font.SysFont("Verdana", 60)
    fh = pygame.font.SysFont("Verdana", 100)

    # подготовка нужных для разных экранов частей визуала(стоит доработать)
    head = fh.render("Space Shooter", True, CYAN)
    text1 = font.render("Sing  in", True, BLUE)
    text2 = font.render("  Play  ", True, BLUE)
    text3 = font.render("Settings", True, BLUE)

    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect3 = text3.get_rect()
    header = head.get_rect()
    x = width // 2
    y = height // 4

    textRect1.center = (x, y)
    textRect2.center = (x, y * 2)
    textRect3.center = (x, y * 3)
    header.center = (x, head.get_height() // 2)

    enter = font.render("Back", True, WHITE)
    enterR = enter.get_rect()
    enterR.center = (width // 8, height // 8 * 7)
    font = pygame.font.SysFont("Verdana", 60)

    text_box = ""
    user_text = ""
    active = False

    pygame.display.set_caption("Space Shooter")
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
    if back_music:
        music.play(-1)
    # объявление открытого экрана + начальные данные
    is_main_window = True
    is_data_window = False
    is_levels_window = False
    is_settings_window = False
    win = False
    f = 0  # выбранное окно
    r = True  # ход цикла
    name = "Unknown"
    # основной цикл
    while r:

        if is_main_window:
            # главный экран
            end_game = False  # для досрочного выхода из игры без финального экрана
            for event in pygame.event.get():
                if (
                    event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    r = False
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if click_music:
                        click.play()
                    if textRect1.collidepoint(event.pos) and f == 0:
                        f = 1
                        is_main_window = False
                        is_data_window = True
                    if textRect2.collidepoint(event.pos) and f == 0:
                        f = 2
                        is_main_window = False
                        is_levels_window = True

                    if textRect3.collidepoint(event.pos) and f == 0:
                        f = 3
                        is_main_window = False
                        is_settings_window = True

            screen.fill(BLACK)
            # фон
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
            # отрисовка
            screen.blit(text1, textRect1)
            pygame.draw.rect(screen, BLUE, textRect1, 1)
            screen.blit(text2, textRect2)
            pygame.draw.rect(screen, BLUE, textRect2, 1)
            screen.blit(text3, textRect3)
            pygame.draw.rect(screen, BLUE, textRect3, 1)
            screen.blit(head, header)

            pygame.display.flip()
            clock.tick(60)
        if is_data_window:
            # окно входа
            if win:
                win = False
                res = findpers(user_text)
                name = text_box = res[0][0]
                score = res[0][1]
                y_score = font.render(f"Your Score: {str(score)}", True, WHITE)
                y_scoreR = y_score.get_rect()
                y_scoreR.center = (
                    width // 4 + width // 3,
                    height // 4 + 2 * y_score.get_height(),
                )
            font = pygame.font.SysFont("Verdana", 30)
            f = 0
            screen.fill(BLACK)
            find = font.render("Sing in", True, WHITE)
            findR = find.get_rect()
            findR.center = (width // 8, height // 8)

            make = font.render("Make new account", True, WHITE)
            makeR = make.get_rect()
            makeR.center = (width // 4 * 3, height // 8)

            ramka = pygame.Rect(
                width // 3,
                height // 8 + find.get_height(),
                width * 1 // 2,
                height // 8 * 6,
            )
            input_rect = pygame.Rect(20, 20, width * 2 // 3, 40)

            color_active = pygame.Color(LIGHTBL)
            color_passive = pygame.Color(GRAY)
            color = color_passive

            for event in pygame.event.get():
                if (
                    event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    r = False
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if click_music:
                        click.play()
                    if input_rect.collidepoint(event.pos):
                        active = True

                    if enterR.collidepoint(event.pos):
                        is_data_window = False
                        is_main_window = True
                    if findR.collidepoint(event.pos):
                        res = findpers(user_text)
                        name = text_box = res[0][0]
                        score = res[0][1]
                        y_score = font.render(f"Your Score: {str(score)}", True, WHITE)
                        y_scoreR = y_score.get_rect()
                        y_scoreR.center = (
                            width // 4 + width // 3,
                            height // 4 + 2 * find.get_height(),
                        )
                    if makeR.collidepoint(event.pos):
                        res = makepers(user_text)
                        name = text_box = res[0][0]
                        score = res[0][1]
                        y_score = font.render(f"Your Score: {str(score)}", True, WHITE)
                        y_scoreR = y_score.get_rect()
                        y_scoreR.center = (
                            width // 4 + width // 3,
                            height // 4 + 2 * find.get_height(),
                        )
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
            # отрисовка
            pygame.draw.rect(screen, color, input_rect)
            pygame.draw.rect(screen, GRAY, ramka, border_radius=15)

            pygame.draw.rect(screen, WHITE, enterR, 1)
            screen.blit(enter, enterR)
            pygame.draw.rect(screen, WHITE, findR, 1)
            screen.blit(find, findR)
            pygame.draw.rect(screen, WHITE, makeR, 1)
            screen.blit(make, makeR)
            # заполнение полей с изменяемыми данными
            if name != "Unknown" and name != "Записи не найдено.":
                screen.blit(y_score, y_scoreR)

            text_surface = font.render(user_text, True, WHITE)
            text_rect = font.render(text_box, True, WHITE)
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y))
            text_rectR = text_rect.get_rect()
            text_rectR.center = (
                width // 3 + width // 4,
                height // 8 + 2 * find.get_height(),
            )
            screen.blit(text_rect, text_rectR)
            # нужно для поля с именем
            input_rect.w = max(width * 2 // 3, text_surface.get_width() + 10)
            pygame.display.flip()
            clock.tick(60)
        if is_levels_window:
            # окно с уровнями
            font = pygame.font.SysFont("Verdana", 60)
            f = 0
            screen.fill(BLACK)
            level_n = None
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

            is_level = False  # флаг выбран ли уровень
            for event in pygame.event.get():
                if (
                    event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    r = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if click_music:
                        click.play()
                    if Rect1.collidepoint(event.pos):
                        level_n = 1
                        is_level = True
                        # r = False
                    if Rect2.collidepoint(event.pos):
                        level_n = 2
                        is_level = True
                        # r = False
                    if Rect3.collidepoint(event.pos):
                        level_n = 3
                        is_level = True
                        # r = False
                    if enterR.collidepoint(event.pos):
                        is_main_window = True
                        is_levels_window = False
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
                end_game = True  # флаг того, как закончилась игра
                # выходом или заходом в уровень
                music_play = (
                    True  # флаг того, чтоможно снова играть музыку победы/проигрыша
                )
                is_levels_window = False
                # r = False
                score = start_level(d[level_n])
                update(name, score)
                win = score > 0  # победил человек или нет
        if is_settings_window:
            # окно с настройками
            f = 0
            screen.fill(BLACK)
            ramka_set = pygame.Rect(
                0,
                0,
                width * 1 // 2,
                height,
            )
            query = """
            SELECT * FROM Players ORDER BY score
            """
            connection.commit()
            font = pygame.font.SysFont("Verdana", 30)
            fonth = pygame.font.SysFont("Verdana", 60)
            res = [
                f"{i + 1}. {el[1]}-{el[2]}"
                for i, el in enumerate(
                    sorted(cursor.execute(query).fetchall()[:4], key=lambda el: -el[2])
                )
            ]
            if len(res) < 3:
                res.append("")
                res.append("")
                res.append("")
            top1 = font.render(res[0], True, WHITE)
            top1R = top1.get_rect()
            top2 = font.render(res[1], True, WHITE)
            top2R = top2.get_rect()
            top3 = font.render(res[2], True, WHITE)
            top3R = top3.get_rect()
            headt = fonth.render("Top of players", True, WHITE)
            headtR = headt.get_rect()

            music1 = font.render("On/Off background music", True, WHITE)
            music2 = font.render("On/Off click music", True, WHITE)

            music1R = music1.get_rect()
            music2R = music2.get_rect()
            music1R.center = (width * 3 // 4, height // 3)
            music2R.center = (width * 3 // 4, height // 3 * 2)

            top1R.center = (width * 1 // 4, height // 8 * 3)
            top2R.center = (width * 1 // 4, height // 8 * 4)
            top3R.center = (width * 1 // 4, height // 8 * 5)
            headtR.center = (width * 1 // 4, height // 8)
            for event in pygame.event.get():
                if (
                    event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    r = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if click_music:
                        click.play()

                    if enterR.collidepoint(event.pos):
                        is_settings_window = False
                        is_main_window = True
                    if music1R.collidepoint(event.pos):
                        back_music = False if back_music else True
                        if back_music:
                            music.play(-1)
                        else:
                            music.stop()
                    if music2R.collidepoint(event.pos):
                        click_music = False if click_music else True
            pygame.draw.rect(screen, GRAY, ramka_set)
            pygame.draw.rect(screen, WHITE, enterR, 1)
            screen.blit(enter, enterR)
            screen.blit(top1, top1R)
            screen.blit(top2, top2R)
            screen.blit(top3, top3R)
            screen.blit(headt, headtR)
            screen.blit(music2, music2R)
            pygame.draw.rect(screen, WHITE, music2R, 1)
            screen.blit(music1, music1R)
            pygame.draw.rect(screen, WHITE, music1R, 1)

            pygame.display.flip()
            clock.tick(60)
        if end_game:
            # конечное окно для победы/поражения
            font = pygame.font.SysFont("Verdana", 50)
            new_ramka = pygame.Rect(
                width // 4,
                height // 4,
                width // 2,
                height // 2,
            )
            # подведение итогов по уровню
            y_name = font.render(name, True, WHITE)
            y_nameR = y_name.get_rect()
            y_nameR.center = (width // 2, height // 4 + height // 8)
            y_score = font.render(f"{str(score)} - Score", True, WHITE)
            y_scoreR = y_score.get_rect()
            y_scoreR.center = (width // 2, height // 4 + height // 8 * 3)

            if win:
                if music_play:
                    win_mu.play(0)
                    music_play = False
                winner = "Mission Accomplished"
            else:
                if music_play:
                    lose.play(0)
                    music_play = False
                winner = "Mission Failed"
            winner_text = font.render(winner, True, GREEN if win else RED)
            winner_textR = winner_text.get_rect()
            winner_textR.center = (width // 2, height // 4 + height // 8 * 2)
            f = 0
            screen.fill(BLACK)
            for event in pygame.event.get():
                if (
                    event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    r = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click.play()

                    if enterR.collidepoint(event.pos):
                        is_levels_window = False
                        end_game = False
                        is_main_window = True
            pygame.draw.rect(screen, GRAY, new_ramka, border_radius=15)
            pygame.draw.rect(screen, WHITE, enterR, 1)
            screen.blit(enter, enterR)
            screen.blit(y_score, y_scoreR)
            screen.blit(winner_text, winner_textR)
            screen.blit(y_name, y_nameR)

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()


start_window()
