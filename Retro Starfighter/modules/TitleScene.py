import glvars
from modules.defines import IMG_DIR, SCALE, SFX_DIR, BG_SPD, PAR_SPD, WIN_RES, VERSION, FONT_SIZE
from modules.muda import Scene
from modules.muda import load_img, draw_background, load_sound, draw_text
from modules.DifficultySelectionScene import DifficultySelectionScene
from modules.widgets import TitleMenuWidget


GAME_FONT = None


import katagames_sdk as katasdk

kengi = katasdk.engine
pygame = kengi.import_pygame()


class TitleScene(Scene):
    def __init__(self, P_Prefs):
        super().__init__()
        # Player preferences
        self.P_Prefs = P_Prefs

        # Background
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # Images
        self.logo_img = load_img("logo_notilt.png", IMG_DIR, 4, convert_alpha=False)
        self.logo_rect = self.logo_img.get_rect()
        self.logo_hw = self.logo_rect.width / 2

        # Menu object
        self.title_menu = TitleMenuWidget(0)  # self.P_Prefs.title_selected)

        # Logo bob
        self.bob_timer = katasdk.engine.import_pygame().time.get_ticks()
        self.bob_m = 0

        self.exit = False  # Dumb hack to set running = False on the main loop

        # Sounds
        self.sfx_keypress = load_sound("sfx_keypress.wav", SFX_DIR, self.P_Prefs.sfx_vol)

        self._pygame = kengi.import_pygame()
        self._dur_last_joymove = 0

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

            elif event.type == self._pygame.KEYDOWN:

                if event.key == self.P_Prefs.key_up:
                    self.title_menu.select_up()
                    self.sfx_keypress.play()  # Play key press sound

                elif event.key == self.P_Prefs.key_down:
                    self.title_menu.select_down()
                    self.sfx_keypress.play()  # Play key press sound

                elif event.key == self.P_Prefs.key_fire or event.key == self._pygame.K_RETURN:
                    self.sfx_keypress.play()  # Play key press sound

                    self._confirm_choice()

    def _confirm_choice(self):
        if self.title_menu.get_selected() == 0:
            self.P_Prefs.title_selected = 0
            self.manager.go_to(DifficultySelectionScene(self.P_Prefs))

        elif self.title_menu.get_selected() == 1:
            self.P_Prefs.title_selected = 1
            # self.manager.go_to(ScoresScene(self.P_Prefs))

        elif self.title_menu.get_selected() == 2:
            self.P_Prefs.title_selected = 2
            # self.manager.go_to(OptionsScene(self.P_Prefs))

        elif self.title_menu.get_selected() == 3:
            self.P_Prefs.title_selected = 3
            # self.manager.go_to(CreditsScene(self.P_Prefs))

        elif self.title_menu.get_selected() == 4:
            self.exit = True

    def update(self, dt):
        # gestion joystick
        hatval = glvars.jhandler[0].hat[0]
        if hatval == (0, 0):
            self._dur_last_joymove = 0
        else:
            if self._dur_last_joymove >= 0:
                forcedelay = -0.2
                if hatval == (-1, 0):
                    self.title_menu.select_down()
                    self._dur_last_joymove = forcedelay
                elif hatval == (1, 0):
                    self.title_menu.select_up()
                    self._dur_last_joymove = forcedelay
            else:
                self._dur_last_joymove += dt

        # le reste du logic update
        self.bg_y += BG_SPD * dt
        self.par_y += PAR_SPD * dt
        self.title_menu.update()

    def draw(self, window):
        now = kengi.import_pygame().time \
            .get_ticks()
        if now - self.bob_timer > 500:
            self.bob_timer = now
            self.bob_m = 1 - self.bob_m

        draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
        draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

        window.blit(self.logo_img, (WIN_RES["w"] / 2 - self.logo_hw, -64 + (2 * self.bob_m)))

        # Draw menu
        self._draw_menu(window)

    def _draw_menu(self, window):
        self.title_menu.draw(window)  # TitleMenuWidget

        # draw_text(window, "(Test Build v.Whatever)", int(FONT_SIZE/2), GAME_FONT, window.get_rect().centerx, 30, "white", "centered")
        tty = 480
        cx = 160
        draw_text(window, f"Game v{VERSION}", int(FONT_SIZE * 0.7), GAME_FONT, cx,
                  tty - 50, "white", "centered")
        draw_text(window, "Pygame v2.0.1", int(FONT_SIZE * 0.7), GAME_FONT, cx,
                  tty - 40, "white", "centered")
        draw_text(window, "(c) 2020 zyenapz", int(FONT_SIZE * 0.7), GAME_FONT, cx,
                  tty - 30, "white", "centered")
        draw_text(window, "Code licensed under GPL-3.0", int(FONT_SIZE * 0.7), GAME_FONT, cx,
                  tty - 20, "white", "centered")
        draw_text(window, "Art licensed under CC BY-NC 4.0", int(FONT_SIZE * 0.7), GAME_FONT, cx,
                  tty - 10, "white", "centered")
