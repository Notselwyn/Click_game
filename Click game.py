""""Written by NotSelwyn (https://github.com/NotSelwyn)"""


def main():
    import sys
    import subprocess
    import random
    import time
    import os

    try:
        import pygame
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "pip", "install", "pygame"])
        import pygame
    try:
        import datetime
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "pip", "install", "datetime"])
        import datetime

    pygame.init()
    clock = pygame.time.Clock()
    size = [512, 612]
    bg = pygame.image.load(os.path.join("img", "background.png"))
    bg_fade = pygame.image.load(os.path.join("img", "background_fade.png"))
    play = pygame.image.load(os.path.join("img", "play.png"))
    highscore_rect = pygame.image.load(os.path.join("img", "highscore.png"))
    settings = pygame.image.load(os.path.join("img", "settings.png"))
    settingsbg = pygame.image.load(os.path.join("img", "settingsbg.png"))
    settingsbg = pygame.transform.scale(settingsbg, [350, 612])
    X = size[0]
    Y = size[1]

    screen = pygame.display.set_mode(size)

    font = pygame.font.Font('freesansbold.ttf', 30)

    pygame.display.set_caption('Click thing')

    def font_func(*num):
        return pygame.font.Font('freesansbold.ttf', num[0])

    def write_score():
        with open("scores.txt", "a") as f:
            f.write(f"{score}\n")

    def top_scores():
        with open("scores.txt", "r") as f:
            scores = f.readlines()
        for a, b in enumerate(scores):
            scores[a].replace(r"\n", "")
            scores[a] = int(scores[a])
        scores = sorted(scores)
        scores.reverse()
        return scores

    def count_down():
        x = 0
        start_time_ = datetime.datetime.now()
        count_font = pygame.font.Font('freesansbold.ttf', 120)
        time_text = font_func(20).render(f'TIME', True, [0, 0, 0])
        timeRect = time_text.get_rect()
        timeRect.center = (512 - 64, 30)
        time_count_text = font_func(50).render(f'30', True, [255, 0, 0])
        time_countRect = time_count_text.get_rect()
        time_countRect.center = (512 - 64, 70)

        score_text = font_func(20).render(f'SCORE', True, [0, 0, 0], [255, 255, 255])
        scoreRect = score_text.get_rect()
        scoreRect.center = (256, 30)
        score_count_text = font_func(50).render(f'{score}', True, [0, 255, 0], [255, 255, 255])
        score_countRect = score_count_text.get_rect()
        score_countRect.center = (256, 70)

        high_score_text = font_func(20).render(f'HIGHSCORE', True, [0, 0, 0], [255, 255, 255])
        high_scoreRect = high_score_text.get_rect()
        high_scoreRect.center = (64, 30)
        high_score_count_text = font_func(50).render(f'{max(top_scores()[0], score)}', True, [0, 0, 0], [255, 255, 255])
        high_score_countRect = high_score_count_text.get_rect()
        high_score_countRect.center = (64, 70)

        while 3 - x > 0:

            count_ = count_font.render(f'{3 - x}', True, [255, 255, 255])
            count_rect = count_.get_rect()
            count_rect.center = (X // 2, Y // 2 + 50)

            screen.blit(bg, [0, 0])

            screen.blit(time_text, timeRect)
            screen.blit(time_count_text, time_countRect)
            screen.blit(score_text, scoreRect)
            screen.blit(score_count_text, score_countRect)
            screen.blit(high_score_text, high_scoreRect)
            screen.blit(high_score_count_text, high_score_countRect)

            screen.blit(bg_fade, [0, 0])
            screen.blit(count_, count_rect)

            x = int((datetime.datetime.now() - start_time_).total_seconds())
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.K_SPACE:
                    x = 5
                    print(x)
        pygame.event.clear()

    start_time = datetime.datetime.now()
    time_text = font.render(f'time: {datetime.datetime.now() - start_time}', True, [0, 0, 0], [255, 255, 255])
    timeRect = time_text.get_rect()
    timeRect.topleft = (512 - 200, 10)

    squares = []
    thanos_snap2 = []
    score = 0
    on_square = False
    settings_bool = False
    settings_opening = True
    settings_done = True
    z = 0
    score_count = 50
    score_done = True

    # SKIP PLAYING BUTTON!!!!!!!!!!!!!! IMPORTANT FOR NEAT!!!!!!!!!!!
    playing = False

    while True:
        while playing is False:
            screen.fill([255, 255, 255])

            start_text = font.render(f'START', True, [0, 0, 0], [255, 255, 255])
            startRect = start_text.get_rect()
            startRect.center = (size[0] // 2, size[1] // 2 - 100)

            play = pygame.transform.scale(play, (128, 128))
            playRect = play.get_rect()
            playRect.center = (size[0] // 2, size[1] // 2)

            # settings = pygame.transform.scale(settings, (64, 64))
            # settingsRect = settings.get_rect()
            # settingsRect.center = (42, 42)

            screen.blit(play, playRect)
            screen.blit(start_text, startRect)
            # screen.blit(settings, settingsRect)

            screen.blit(font_func(20).render(f'HIGHSCORES', True, [0, 0, 0], [255, 255, 255]),
                        [size[0] - highscore_rect.get_width() + 10, (size[1] - highscore_rect.get_height()) // 2 - 20])
            screen.blit(highscore_rect, [size[0] - highscore_rect.get_width(), (size[1] - highscore_rect.get_height()) // 2])

            for i, j in enumerate(top_scores()):
                screen.blit(font_func(30).render(str(j), True, [0, 0, 0]), [512 - 100, i * 42 + 207])
                if i == 4:
                    break

            # if settings_bool:
            #    if settings_opening is True and settings_done is False:
            #        limit = 10
            #        z += 1
            #        if z == limit:
            #            settings_opening = False
            #            settings_done = True
            #    if settings_opening is False and settings_done is False:
            #        z -= 1
            #        if z == 0:
            #            settings_opening = True
            #            settings_done = True
            #            settings_bool = False
            #
            #    screen.blit(pygame.transform.scale(settingsbg, [int((350 / limit) * z), int((612 / limit) * z)]), [(X - settingsbg.get_width()) // 2, 0])
            #    screen.blit(font_func(50).render(f'WIP', True, [255, 255, 255], [0, 0, 0]),
            #                [x//2-25 for x in size])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if playRect.collidepoint(mouse_pos[0], mouse_pos[1]) and settings_bool is False:
                        time.sleep(0.1)

                        score = 0
                        count_down()

                        start_time = datetime.datetime.now()
                        time_text = font.render(f'time: 30', True, [0, 0, 0], [255, 255, 255])
                        timeRect = time_text.get_rect()
                        timeRect.topleft = (512 - 200, 10)

                        squares = []
                        on_square = False
                        playing = True

                        for i in range(3):
                            random.randint(0, 15)
                            square = pygame.Rect(random.randint(0, 3) * 128, random.randint(0, 3) * 128 + 100, 128, 128)
                            if str(square) not in squares:
                                squares.append(square)

                    # elif settingsRect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    #    settings_bool = True
                    #    settings_done = False

            pygame.display.flip()
            clock.tick(60)

        settings_bool = False
        settings_done = False
        settings_opening = True
        z = 0

        while playing:
            time_text = font_func(20).render(f'TIME', True, [0, 0, 0])
            timeRect = time_text.get_rect()
            timeRect.center = (512 - 64, 30)
            time_count_text = font_func(50).render(f'{int(31 - (datetime.datetime.now() - start_time).total_seconds())}', True, [255, 0, 0])
            time_countRect = time_count_text.get_rect()
            time_countRect.center = (512 - 64, 70)

            score_text = font_func(20).render(f'SCORE', True, [0, 0, 0])
            scoreRect = score_text.get_rect()
            scoreRect.center = (256, 30)

            if not score_done:
                if score_count >= 60:
                    print((datetime.datetime.now() - score_time_start).total_seconds())
                    if (datetime.datetime.now() - score_time_start).total_seconds() < 0.3:
                        print("a")
                        if score_count >= 70:
                            print("b")
                            score_count = 70
                    else:
                        sum_ = -4

                elif score_count <= 50:
                    sum_ = 4
                    score_done = True

                print(score_count)
                score_count += sum_

            score_count_text = font_func(score_count).render(f'{score}', True, [0, 255, 0])
            score_countRect = score_count_text.get_rect()
            score_countRect.center = (256, 70)

            high_score_text = font_func(20).render(f'HIGHSCORE', True, [0, 0, 0], [255, 255, 255])
            high_scoreRect = high_score_text.get_rect()
            high_scoreRect.center = (64, 30)

            if max(top_scores()[0], score) == score:
                high_score_count_text = font_func(score_count).render(f'{score}', True, [0, 0, 0])
            if max(top_scores()[0], score) == top_scores()[0]:
                high_score_count_text = font_func(50).render(f'{top_scores()[0]}', True, [0, 0, 0])

            high_score_countRect = high_score_count_text.get_rect()
            high_score_countRect.center = (64, 70)

            screen.blit(bg, [0, 0])

            for k in range(len(thanos_snap2)):
                screen.blit(pygame.transform.scale(pygame.image.load(os.path.join("img", "tile.png")),
                                                   (int((128 / 20) * (20 - thanos_snap2[k - 1]["stage"])), int((128 / 20) * (20 - thanos_snap2[k - 1]["stage"])))), (
                                thanos_snap2[k - 1]["pos"][0] + int((64 / 20) * thanos_snap2[k - 1]["stage"]),
                                thanos_snap2[k - 1]["pos"][1] + int((64 / 20) * thanos_snap2[k - 1]["stage"])))
                thanos_snap2[k - 1]["stage"] += 1
                if thanos_snap2[k - 1]["stage"] == 20:
                    thanos_snap2.pop(k - 1)

            screen.blit(score_text, scoreRect)
            screen.blit(score_count_text, score_countRect)

            screen.blit(time_text, timeRect)
            screen.blit(time_count_text, time_countRect)

            screen.blit(high_score_text, high_scoreRect)
            screen.blit(high_score_count_text, high_score_countRect)

            for i in squares:
                pygame.draw.rect(screen, [0, 0, 0], i)

            c_c = pygame.image.load(os.path.join("img", "cursor.png")).get_rect()
            c_c.center = pygame.mouse.get_pos()
            screen.blit(pygame.image.load(os.path.join("img", "cursor.png")), c_c)

            if int(29 - (datetime.datetime.now() - start_time).total_seconds()) < 0:
                time_text = font_func(60).render(f'Timer ran out.', True, [255, 255, 255])
                timeRect = time_text.get_rect()
                timeRect.center = (X // 2, Y // 2 + 50)

                screen.blit(bg_fade, [0, 0])
                screen.blit(time_text, timeRect)

                write_score()

                pygame.display.flip()
                time.sleep(3)

                playing = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i in squares:
                        if i.collidepoint(mouse_pos[0], mouse_pos[1]):
                            squares.remove(i)
                            thanos_snap2.append({"pos": [(mouse_pos[0] // 128) * 128, ((mouse_pos[1] - 100) // 128) * 128 - 28 + 128], "stage": 0})
                            while len(squares) < 3:
                                random.randint(0, 15)
                                square = pygame.Rect(random.randint(0, 3) * 128, random.randint(0, 3) * 128 + 100, 128, 128)
                                if square not in squares:
                                    squares.append(square)
                            score += 1
                            on_square = True
                            score_done = False
                            score_time_start = datetime.datetime.now()
                            sum_ = 2
                            # playsound(os.path.join("snd", "hit.wav"))

                    else:
                        if not on_square and mouse_pos[1] > 100:
                            time_text = font_func(100).render(f"Missed", True, [255, 255, 255])
                            timeRect = time_text.get_rect()
                            timeRect.center = (X // 2, Y // 2 + 50)
                            screen.blit(bg_fade, [0, 0])
                            screen.blit(time_text, timeRect)
                            write_score()
                            pygame.display.flip()
                            time.sleep(3)
                            playing = False

                        elif on_square:
                            on_square = False

            pygame.display.flip()
            clock.tick(60)


if __name__ == '__main__':
    main()
