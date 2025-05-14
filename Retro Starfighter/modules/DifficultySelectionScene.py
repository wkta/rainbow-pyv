import random
from itertools import repeat

import glvars
from modules.muda import load_img, Scene, draw_background, shake, image_at, scale_rect, draw_hpbar
from modules.spawner import Spawner
from modules.sprites import Player
from modules.widgets import *
from modules.GameScene import GameScene


# DIFFICULTY SELECTION SCENE ================================================================

class DifficultySelectionScene(Scene):
    def __init__(self, P_Prefs):
        self._dur_last_joymove = 0

        # Player preferences
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Difficulty Menu widget
        DEFAULT_SELECTED = 1
        self.w_diffmenu = DifficultyMenuWidget(DEFAULT_SELECTED)
        self.selected_diff = DEFAULT_SELECTED

        # Difficulty icons
        DIFFICULTY_SPRITESHEET = load_img("difficulty_sheet.png", IMG_DIR, SCALE * 2)
        self.DIFFICULTY_ICONS = {
            0: image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE * 2, [0, 0, 16, 16]), True),
            1: image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE * 2, [0, 16, 16, 16]), True),
            2: image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE * 2, [0, 32, 16, 16]), True)
        }

        # Sounds
        self.sfx_keypress = load_sound("sfx_keypress.wav", SFX_DIR, self.P_Prefs.sfx_vol)

    def _selectup(self):
        self.sfx_keypress.play()  # Play sound
        self.w_diffmenu.select_up()
        self.selected_diff = self.w_diffmenu.get_selected()

    def _selectdown(self):
        self.sfx_keypress.play()  # Play sound
        self.w_diffmenu.select_down()
        self.selected_diff = self.w_diffmenu.get_selected()

    def _confirm_choice(self):
        self.sfx_keypress.play()  # Play sound

        if self.w_diffmenu.get_selected_str() != "BACK":
            self.P_Prefs.game_difficulty = self.selected_diff
            self.manager.go_to(GameScene(self.P_Prefs))

        elif self.w_diffmenu.get_selected_str() == "BACK":
            self.manager.go_to(glvars.title_scene)

    def handle_events(self, events):
        for event in events:
            # ------ ajout 18/11 (joystick) ----
            if event.type == pygame.JOYAXISMOTION:
                glvars.jhandler[event.joy].axis[event.axis] = event.value

            elif event.type == pygame.JOYBALLMOTION:
                glvars.jhandler[event.joy].ball[event.ball] = event.rel

            elif event.type == pygame.JOYHATMOTION:
                glvars.jhandler[event.joy].hat[event.hat] = event.value

            elif event.type == pygame.JOYBUTTONUP:
                glvars.jhandler[event.joy].button[event.button] = 0
                print('button<-0 :', event.button)

            elif event.type == pygame.JOYBUTTONDOWN:
                glvars.jhandler[event.joy].button[event.button] = 1
                print('button<-1 :', event.button)
                if event.button == 0:
                    self.sfx_keypress.play()  # Play key press sound
                    self._confirm_choice()
            # --------------- fin joystick

            elif event.type == pygame.KEYDOWN:
                if event.key == self.P_Prefs.key_up:
                    self._selectup()

                elif event.key == self.P_Prefs.key_down:
                    self._selectdown()

                elif event.key == self.P_Prefs.key_fire or event.key == pygame.K_RETURN:
                    self._confirm_choice()

                elif event.key == self.P_Prefs.key_back:
                    self.sfx_keypress.play()  # Play sound
                    pass  # self.manager.go_to(TitleScene(self.P_Prefs))

    def update(self, dt):
        # gestion joystick
        hatval = glvars.jhandler[0].hat[0]
        if hatval == (0, 0):
            self._dur_last_joymove = 0
        else:
            if self._dur_last_joymove >= 0:
                forcedelay = -0.2
                if hatval == (-1, 0):
                    self._selectdown()
                    self._dur_last_joymove = forcedelay
                elif hatval == (1, 0):
                    self._selectup()
                    self._dur_last_joymove = forcedelay
            else:
                self._dur_last_joymove += dt
        # -- fin joystick

        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt
        self.w_diffmenu.update()

    def draw(self, window):
        #draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        #draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)
        window.fill((0,0,0))
        draw_text(window, "SELECT DIFFICULTY", FONT_SIZE * 2, GAME_FONT, WIN_RES["w"] / 2, 64, "white", "centered")

        try:
            window.blit(
                self.DIFFICULTY_ICONS[self.selected_diff],
                (window.get_width() / 2 - self.DIFFICULTY_ICONS[self.selected_diff].get_width() / 2,
                 window.get_height() * 0.30)
            )
        except:
            pass
        # self.w_diffmenu.draw(window)  # bug ici
