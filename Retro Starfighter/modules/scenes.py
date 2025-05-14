import random
from itertools import repeat

import glvars
from modules.muda import load_img, Scene, draw_background, shake, image_at, scale_rect, draw_hpbar
from modules.spawner import Spawner
from modules.sprites import Player
from modules.widgets import *


def get_ticks():
    return kataen.import_pygame().time.get_ticks()


class ScoresScene(Scene):
    def __init__(self, p_prefs):
        # Player preferences
        self.P_Prefs = p_prefs

        # Load scores list
        self.scores_list = list()
        # try:
        #     with open(SCORES_FILE, 'rb') as f:
        #         self.scores_list = pickle.load(f)
        # except:
        #     pass

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Scores table
        self.scores_table = ScoresTableWidget(self.scores_list)

        # Control panel
        self.control_widget = ScoresControlWidget()

        # Sounds
        self.sfx_keypress = load_sound("sfx_keypress.wav", SFX_DIR, self.P_Prefs.sfx_vol)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.P_Prefs.key_left:
                    self.sfx_keypress.play()  # Play keypress sound
                    self.control_widget.move_left()
                elif event.key == self.P_Prefs.key_right:
                    self.sfx_keypress.play()  # Play keypress sound
                    self.control_widget.move_right()
                elif event.key == self.P_Prefs.key_up:
                    self.sfx_keypress.play()  # Play keypress sound
                    self.control_widget.move_up()
                elif event.key == self.P_Prefs.key_down:
                    self.sfx_keypress.play()  # Play keypress sound
                    self.control_widget.move_down()

                elif event.key == self.P_Prefs.key_fire or event.key == pygame.K_RETURN:

                    if self.control_widget.get_active_panel() == "DIRECTION":

                        if self.control_widget.get_dp_selected_option() == "PREV":
                            if self.scores_table.cur_tbl > 0:
                                self.sfx_keypress.play()  # Play keypress sound

                            self.scores_table.prev_table()

                        elif self.control_widget.get_dp_selected_option() == "NEXT":
                            if self.scores_table.cur_tbl < len(self.scores_table.scores) - 1:
                                self.sfx_keypress.play()  # Play keypress sound

                            self.scores_table.next_table()

                    elif self.control_widget.get_active_panel() == "BACK":
                        self.sfx_keypress.play()  # Play keypress sound
                        self.manager.go_to(glvars.title_scene)  # TitleScene(self.P_Prefs)

                elif event.key == self.P_Prefs.key_back:
                    self.sfx_keypress.play()  # Play keypress sound
                    self.manager.go_to(glvars.title_scene)  # TitleScene(self.P_Prefs)

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "HALL OF FAME", FONT_SIZE * 2, GAME_FONT, window.get_rect().centerx, 64, "white", "centered")
        self.scores_table.draw(window)
        self.control_widget.draw(window)


class OptionsScene(Scene):
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Menu widget
        self.menu_widget = OptionsSceneMenuWidget(self.P_Prefs.options_scene_selected)

        # Sounds
        self.sfx_keypress = load_sound("sfx_keypress.wav", SFX_DIR, self.P_Prefs.sfx_vol)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:

                # Key press events
                if event.key == self.P_Prefs.key_back:
                    self.sfx_keypress.play()  # Play key press sound
                    self.P_Prefs.options_scene_selected = 0
                    self.manager.go_to(glvars.title_scene)

                elif event.key == self.P_Prefs.key_up:
                    self.sfx_keypress.play()  # Play key press sound
                    self.menu_widget.select_up()

                elif event.key == self.P_Prefs.key_down:
                    self.sfx_keypress.play()  # Play key press sound
                    self.menu_widget.select_down()

                elif event.key == self.P_Prefs.key_fire or event.key == pygame.K_RETURN:
                    self.sfx_keypress.play()  # Play key press sound

                    if self.menu_widget.get_selected_str() == "VIDEO":
                        self.P_Prefs.options_scene_selected = 0
                        self.manager.go_to(VideoOptionsScene(self.P_Prefs))

                    elif self.menu_widget.get_selected_str() == "SOUND":
                        self.P_Prefs.options_scene_selected = 1
                        self.manager.go_to(SoundOptionsScene(self.P_Prefs))

                    elif self.menu_widget.get_selected_str() == "GAME":
                        self.P_Prefs.options_scene_selected = 2
                        self.manager.go_to(GameOptionsScene(self.P_Prefs))

                    elif self.menu_widget.get_selected_str() == "CONTROLS":
                        self.P_Prefs.options_scene_selected = 3
                        self.manager.go_to(ControlsOptionsScene(self.P_Prefs))

                    elif self.menu_widget.get_selected_str() == "BACK":
                        self.P_Prefs.options_scene_selected = 0
                        self.manager.go_to(glvars.title_scene)

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

        self.menu_widget.update()

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "OPTIONS", FONT_SIZE * 2, GAME_FONT, WIN_RES["w"] / 2, 64, "white", "centered")
        self.menu_widget.draw(window)


class VideoOptionsScene(Scene):
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Menu widget
        self.menu_widget = VideoOptionsSceneMenuWidget(self.P_Prefs)

        # Sounds
        self.sfx_keypress = load_sound("sfx_keypress.wav", SFX_DIR, self.P_Prefs.sfx_vol)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:

                # Key press events
                if event.key == self.P_Prefs.key_fire or event.key == pygame.K_RETURN:
                    self.sfx_keypress.play()  # Play key press sound

                    if self.menu_widget.get_selected() == self.menu_widget.get_max_index():
                        self.manager.go_to(OptionsScene(self.P_Prefs))

                elif event.key == self.P_Prefs.key_back:
                    self.sfx_keypress.play()  # Play key press sound
                    self.manager.go_to(OptionsScene(self.P_Prefs))

                elif event.key == self.P_Prefs.key_up:
                    self.sfx_keypress.play()  # Play key press sound
                    self.menu_widget.select_up()

                elif event.key == self.P_Prefs.key_down:
                    self.sfx_keypress.play()  # Play key press sound
                    self.menu_widget.select_down()

                elif event.key == self.P_Prefs.key_left:
                    self.sfx_keypress.play()  # Play key press sound
                    self.menu_widget.select_left()

                elif event.key == self.P_Prefs.key_right:
                    self.sfx_keypress.play()  # Play key press sound
                    self.menu_widget.select_right()

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

        self.menu_widget.update()

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "VIDEO OPTIONS", FONT_SIZE * 2, GAME_FONT, WIN_RES["w"] / 2, 64, "white", "centered")
        self.menu_widget.draw(window)


class SoundOptionsScene(Scene):
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Menu widget
        self.menu_widget = SoundOptionsSceneMenuWidget(self.P_Prefs)

        # Key press delay
        self.press_timer = get_ticks()
        self.press_delay = 75

        # Sounds
        self.sfx_keypress = load_sound("sfx_keypress.wav", SFX_DIR, self.P_Prefs.sfx_vol)

    def handle_events(self, events):
        # KEYDOWN EVENTS
        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == self.P_Prefs.key_fire or event.key == pygame.K_RETURN:
                    self.sfx_keypress.play()  # Play key press sound

                    if self.menu_widget.get_selected() == self.menu_widget.get_max_index():
                        self.manager.go_to(OptionsScene(self.P_Prefs))

                elif event.key == self.P_Prefs.key_back:
                    self.sfx_keypress.play()  # Play key press sound
                    self.manager.go_to(OptionsScene(self.P_Prefs))

                elif event.key == self.P_Prefs.key_up:
                    self.sfx_keypress.play()  # Play key press sound
                    self.menu_widget.select_up()

                elif event.key == self.P_Prefs.key_down:
                    self.sfx_keypress.play()  # Play key press sound
                    self.menu_widget.select_down()

        # Volume knob key presses
        now = get_ticks()
        if now - self.press_timer > self.press_delay:
            self.press_timer = now

            pressed = pygame.key.get_pressed()
            if pressed[self.P_Prefs.key_left]:
                self.menu_widget.select_left()

            elif pressed[self.P_Prefs.key_right]:
                self.menu_widget.select_right()

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

        # Update preferences
        self.P_Prefs.sfx_vol = self.menu_widget.rs_sfx.get_value() / 100
        self.P_Prefs.music_vol = self.menu_widget.rs_ost.get_value() / 100

        # Update sound volumes
        self.sfx_keypress.set_volume(self.P_Prefs.sfx_vol)

        self.menu_widget.update()

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "SOUND OPTIONS", FONT_SIZE * 2, GAME_FONT, WIN_RES["w"] / 2, 64, "white", "centered")
        self.menu_widget.draw(window)


class GameOptionsScene(Scene):
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Menu widget
        self.menu_widget = GameOptionsSceneMenuWidget(self.P_Prefs)

        # Sounds
        self.sfx_keypress = load_sound("sfx_keypress.wav", SFX_DIR, self.P_Prefs.sfx_vol)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == self.P_Prefs.key_fire or event.key == pygame.K_RETURN:
                    self.sfx_keypress.play()  # Play sound
                    if self.menu_widget.get_selected() == self.menu_widget.get_max_index():
                        self.manager.go_to(OptionsScene(self.P_Prefs))

                elif event.key == self.P_Prefs.key_back:
                    self.sfx_keypress.play()  # Play sound
                    self.manager.go_to(OptionsScene(self.P_Prefs))

                elif event.key == self.P_Prefs.key_up:
                    self.sfx_keypress.play()  # Play sound
                    self.menu_widget.select_up()

                elif event.key == self.P_Prefs.key_down:
                    self.sfx_keypress.play()  # Play sound
                    self.menu_widget.select_down()

                elif event.key == self.P_Prefs.key_left:
                    self.sfx_keypress.play()  # Play sound
                    self.menu_widget.select_left()

                elif event.key == self.P_Prefs.key_right:
                    self.sfx_keypress.play()  # Play sound
                    self.menu_widget.select_right()

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

        self.menu_widget.update()

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "GAME OPTIONS", FONT_SIZE * 2, GAME_FONT, WIN_RES["w"] / 2, 64, "white", "centered")
        self.menu_widget.draw(window)


class ControlsOptionsScene(Scene):
    def __init__(self, P_Prefs):
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Menu widget
        self.menu_widget = ControlsOptionsSceneMenuWidget(self.P_Prefs)

        # Sounds
        self.sfx_keypress = load_sound("sfx_keypress.wav", SFX_DIR, self.P_Prefs.sfx_vol)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if not self.menu_widget.is_changingkey:
                    if event.key == self.P_Prefs.key_up:
                        self.sfx_keypress.play()  # Play sound
                        self.menu_widget.select_up()

                    elif event.key == self.P_Prefs.key_down:
                        self.sfx_keypress.play()  # Play sound
                        self.menu_widget.select_down()

                    elif event.key == self.P_Prefs.key_left:
                        self.sfx_keypress.play()  # Play sound
                        self.menu_widget.select_left()

                    elif event.key == self.P_Prefs.key_right:
                        self.sfx_keypress.play()  # Play sound
                        self.menu_widget.select_right()

                    elif event.key == pygame.K_RETURN and self.menu_widget.get_selected() != self.menu_widget.get_max_index():
                        self.sfx_keypress.play()  # Play sound
                        self.menu_widget.highlight()

                    elif event.key == self.P_Prefs.key_back:
                        self.sfx_keypress.play()  # Play sound
                        self.manager.go_to(OptionsScene(self.P_Prefs))
                        self.menu_widget.save_prefs()

                    elif event.key == self.P_Prefs.key_fire or event.key == pygame.K_RETURN:
                        if self.menu_widget.get_selected() == self.menu_widget.get_max_index():
                            self.sfx_keypress.play()  # Play sound
                            self.manager.go_to(OptionsScene(self.P_Prefs))
                            self.menu_widget.save_prefs()
                else:
                    if event.key == pygame.K_RETURN:
                        self.sfx_keypress.play()  # Play sound
                        self.menu_widget.unhighlight()
                    else:
                        self.sfx_keypress.play()  # Play sound
                        self.menu_widget.change_key(event.key)

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

        self.menu_widget.update()

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "CONTROLS", FONT_SIZE * 2, GAME_FONT, WIN_RES["w"] / 2, 64, "white", "centered")
        self.menu_widget.draw(window)


# CREDITS SCENE ================================================================

class CreditsScene(Scene):
    def __init__(self, P_Prefs):
        # Player preferences
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Button
        self.back_button = pygame.Surface((128, 32))
        self.back_button.fill("white")

        # Devs' pictures
        DEVS_SHEET = load_img("devs_sheet.png", IMG_DIR, SCALE)
        self.zye_icon = image_at(DEVS_SHEET, scale_rect(SCALE, [0, 0, 16, 16]), True)
        self.rio_icon = image_at(DEVS_SHEET, scale_rect(SCALE, [16, 0, 16, 16]), True)

        # Sounds
        self.sfx_keypress = load_sound("sfx_keypress.wav", SFX_DIR, self.P_Prefs.sfx_vol)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.sfx_keypress.play()
                if event.key == self.P_Prefs.key_back or event.key == self.P_Prefs.key_fire or event.key == pygame.K_RETURN:
                    self.manager.go_to(glvars.title_scene)

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        draw_text(window, "CREDITS", FONT_SIZE * 2, GAME_FONT, WIN_RES["w"] / 2, 64, "white", "centered")
        window.blit(self.zye_icon, (WIN_RES["w"] / 2 - self.zye_icon.get_width() / 2, WIN_RES["h"] * 0.20))
        draw_text2(window, "zyenapz", GAME_FONT, FONT_SIZE, (WIN_RES["w"] / 2, WIN_RES["h"] * 0.270), "YELLOW",
                   align="center")
        draw_text2(window, "code,art,sfx", GAME_FONT, FONT_SIZE, (WIN_RES["w"] / 2, WIN_RES["h"] * 0.300), "white",
                   align="center")

        window.blit(self.rio_icon, (WIN_RES["w"] / 2 - self.rio_icon.get_width() / 2, WIN_RES["h"] * 0.350))
        draw_text2(window, "YoItsRion", GAME_FONT, FONT_SIZE, (WIN_RES["w"] / 2, WIN_RES["h"] * 0.430), "YELLOW",
                   align="center")
        draw_text2(window, "music", GAME_FONT, FONT_SIZE, (WIN_RES["w"] / 2, WIN_RES["h"] * 0.460), "white",
                   align="center")

        draw_text2(window, "Special thanks", GAME_FONT, FONT_SIZE, (WIN_RES["w"] / 2, WIN_RES["h"] * 0.560), "white",
                   align="center")
        draw_text2(window, "@ooshkei,", GAME_FONT, FONT_SIZE, (WIN_RES["w"] / 2, WIN_RES["h"] * 0.600), "white",
                   align="center")
        draw_text2(window, "my friends,", GAME_FONT, FONT_SIZE, (WIN_RES["w"] / 2, WIN_RES["h"] * 0.640), "white",
                   align="center")
        draw_text2(window, "the pygame community,", GAME_FONT, FONT_SIZE, (WIN_RES["w"] / 2, WIN_RES["h"] * 0.680),
                   "white", align="center")
        draw_text2(window, "and you!", GAME_FONT, FONT_SIZE, (WIN_RES["w"] / 2, WIN_RES["h"] * 0.720), "white",
                   align="center")

        draw_text2(
            self.back_button,
            "BACK",
            GAME_FONT,
            FONT_SIZE,
            (self.back_button.get_width() / 2 - FONT_SIZE, self.back_button.get_height() / 2 - FONT_SIZE / 2),
            "black",
            align="center"
        )
        window.blit(self.back_button,
                    (window.get_width() / 2 - self.back_button.get_width() / 2, window.get_rect().height * 0.8))


# GAME OVER SCENE ================================================================

class GameOverScene(Scene):
    def __init__(self, P_Prefs):
        # Player preferences 
        self.P_Prefs = P_Prefs

        # Scene variables
        self.score = self.P_Prefs.score
        self.name = str()
        self.bckspace_timer = get_ticks()
        self.bckspace_delay = 200
        self.MIN_CHAR = 2
        self.MAX_CHAR = 5
        self.score_comment = self._get_comment(self.score)
        self.difficulty = self.P_Prefs.game_difficulty

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Enter button
        self.enter_button = pygame.Surface((128, 32))
        self.enter_button.fill("white")

        # Ranks
        RANKS_SHEET = load_img("ranks_sheet.png", IMG_DIR, SCALE * 2)
        self.RANKS_IMGS = {
            "RECRUIT": image_at(RANKS_SHEET, scale_rect(SCALE * 2, [0, 0, 16, 16]), True),
            "ENSIGN": image_at(RANKS_SHEET, scale_rect(SCALE * 2, [16, 0, 16, 16]), True),
            "LIEUTENANT": image_at(RANKS_SHEET, scale_rect(SCALE * 2, [32, 0, 16, 16]), True),
            "COMMANDER": image_at(RANKS_SHEET, scale_rect(SCALE * 2, [48, 0, 16, 16]), True),
            "CAPTAIN": image_at(RANKS_SHEET, scale_rect(SCALE * 2, [64, 0, 16, 16]), True),
            "ADMIRAL": image_at(RANKS_SHEET, scale_rect(SCALE * 2, [80, 0, 16, 16]), True)
        }
        self.rank = self.score_comment.upper()

        # Sounds
        self.sfx_keypress = load_sound("sfx_keypress.wav", SFX_DIR, self.P_Prefs.sfx_vol)

    def handle_events(self, events):
        # Keydown events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if str(event.unicode).isalpha() and len(self.name) < self.MAX_CHAR:
                    self.sfx_keypress.play()
                    self.name += event.unicode
                elif event.key == pygame.K_RETURN and len(self.name) >= self.MIN_CHAR:
                    self.sfx_keypress.play()
                    self._exit_scene()

        # Key presses event
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_BACKSPACE]:

            now = get_ticks()
            if now - self.bckspace_timer > self.bckspace_delay:
                if len(self.name) != 0:
                    self.sfx_keypress.play()

                self.bckspace_timer = now
                self.name = self.name[:-1]

    def update(self, dt):
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt

    def draw(self, window):
        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        # Draw game over and score
        draw_text(window, "GAME OVER!", FONT_SIZE * 2, GAME_FONT, WIN_RES["w"] / 2, 64, "white", "centered")
        draw_text(window, f"{int(self.score)}", FONT_SIZE * 4, GAME_FONT, WIN_RES["w"] / 2, 104, HP_RED1, "centered")
        draw_text(window, f"{int(self.score)}", FONT_SIZE * 4, GAME_FONT, WIN_RES["w"] / 2, 100, "white", "centered")

        # Draw rank and image
        # draw_text2(window, "Your Rank", GAME_FONT, int(FONT_SIZE*2), (WIN_RES["w"]/2, WIN_RES["h"]*0.35), "white", align="center")
        try:
            window.blit(
                self.RANKS_IMGS[self.rank],
                (window.get_width() / 2 - self.RANKS_IMGS[self.rank].get_width() / 2, window.get_height() * 0.35)
            )
        except:
            pass
        draw_text2(window, f"Rank: {self.score_comment.capitalize()}", GAME_FONT, int(FONT_SIZE),
                   (WIN_RES["w"] / 2, WIN_RES["h"] * 0.5), "white", align="center")

        # if self.score_comment.upper() == "RECRUIT":
        #     draw_text2(window, f"You don't deserve symmetry", GAME_FONT, int(FONT_SIZE), (WIN_RES["w"]/2, WIN_RES["h"]*0.), "white", align="center")

        # Draw  textbox
        if len(self.name) == 0:
            draw_text2(window, "ENTER NAME", GAME_FONT, int(FONT_SIZE * 2), (WIN_RES["w"] / 2, WIN_RES["h"] * 0.645),
                       "GRAY", align="center")
        else:
            draw_text2(window, f"> {self.name.upper()} <", GAME_FONT, int(FONT_SIZE * 2),
                       (WIN_RES["w"] / 2, WIN_RES["h"] * 0.645), "white", align="center")

        # Draw enter button
        if len(self.name) >= self.MIN_CHAR:
            draw_text2(
                self.enter_button,
                "ENTER",
                GAME_FONT,
                FONT_SIZE,
                (self.enter_button.get_width() / 2, (self.enter_button.get_height() / 2) - FONT_SIZE / 2),
                "black",
                align="center"
            )
            self.enter_button.set_colorkey("black")
            window.blit(
                self.enter_button,
                (
                    window.get_width() / 2 - self.enter_button.get_width() / 2,
                    WIN_RES["h"] * 0.75
                )
            )

    def _exit_scene(self):
        # Load scores list
        scores_list = list()

        # try:
        #     with open(SCORES_FILE, 'rb') as f:
        #         scores_list = pickle.load(f)
        # except:
        #     pass

        # Save score data to file
        # score_dat = (self.name, int(self.score), self.difficulty)
        # scores_list.append(score_dat)
        # with open(SCORES_FILE, 'wb') as f:
        #     pickle.dump(scores_list, f)

        # Go to title scene
        self.manager.go_to(glvars.title_scene)

    def _get_comment(self, score):
        if score == 0:
            return "recruit"
        elif score < 1000:
            return "ensign"
        elif 1000 <= score < 3000:
            return "lieutenant"
        elif 3000 <= score < 6000:
            return "commander"
        elif 6000 <= score < 9000:
            return "captain"
        elif score >= 9000:
            return "admiral"
        else:
            return "bugged"
