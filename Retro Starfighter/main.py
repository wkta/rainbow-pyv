# Open source game
# GPL-3.0
# MOD: star-fighter-k

# +YoItsRion

# First author: zyenap
# collaboration with Kata.Games
# News(twitter): @zyenapz, @CreatePlayEarn


import katagames_sdk.engine as kataen


kataen.init(kataen.HD_MODE)

import time
import katagames_sdk.capsule.engine_ground.conf_eng as cgmconf

# import hack
pygame = kataen.import_pygame()
render_target = None
manager = None

# import pygame, os, random, math, time, pickle
# from pygame.locals import *
# from pygame._sdl2.video import Window
# import glvars

from modules.scenes import *
from modules.defines import WIN_RES, TITLE
from modules.muda import (
    load_img,
    load_sound,
    # read_savedata,
    # write_savedata,
    SceneManager,
)

from modules.TitleScene import TitleScene


class PlayerPrefs:
    def __init__(self):
        self.is_fullscreen = False
        self.is_frameless = False
        self.music_vol = 0.40
        self.sfx_vol = 0.30
        self.game_difficulty = 0
        self.hp_pref = 0
        self.can_pause = False

        # Controls
        self.key_up = pygame.K_RIGHT  # pygame.K_UP
        self.key_down = pygame.K_LEFT  # pygame.K_DOWN
        self.key_left = pygame.K_UP  # pygame.K_LEFT
        self.key_right = pygame.K_DOWN  # pygame.K_RIGHT
        self.key_fire = pygame.K_SPACE  # pygame.K_z
        self.key_back = pygame.K_x

        self.score = 0
        self.title_selected = 0
        self.options_scene_selected = 0


class ScreenUpdater(kataen.EventReceiver):

    def proc_event(self, ev, source):
        if ev.type == kataen.EngineEvTypes.PAINT:
            global render_target
            render_target.fill("black")
            manager.scene.draw(render_target)
            # substantifique moelle du HACK
            ev.screen.blit(
                pygame.transform.scale(
                    pygame.transform.rotate(
                        render_target
                        , -90),
                    (ev.screen.get_width(), ev.screen.get_height())), (0, 0)
            )
            # ev.screen.blit(render_target, (0,0))


class GameLogicUpdater(kataen.EventReceiver):
    def __init__(self):
        super().__init__()
        self.prev_time = time.time()
        self._e_queue = list()

    def proc_event(self, ev, source):

        if ev.type == kataen.EngineEvTypes.LOGICUPDATE:
            now = time.time()
            xdt = now - self.prev_time
            self.prev_time = now

            # Check for QUIT event
            # if pygame.event.get(pygame.QUIT) or \
            # This is a dumb hack but it will work for now.
            #    (type(manager.scene) == TitleScene and manager.scene.exit):
            #     # Save player preferences
            #     try:
            #         with open(USERDAT_FILE, 'wb') as f:
            #             pickle.dump(P_Prefs, f)
            #     except:
            #         print("ERROR: Failed to save.")
            #
            #     # Exit loop and function
            #     running = False
            #     return

            # Call scene methods
            manager.scene.handle_events(self._e_queue)
            self._e_queue.clear()

            manager.scene.update(xdt)
        elif ev.type == kataen.EngineEvTypes.PAINT:
            pass
        else:
            self._e_queue.append(ev)


def run_game():
    global render_target, manager
    # os.environ["SDL_VIDEO_CENTERED"] = "1"
    # hack.init_t = time.time()
    # pygame.init()
    # pygame.mixer.init()

    # Load / create PlayerPrefs object
    P_Prefs = None

    # try:
    #     with open(USERDAT_FILE, 'rb') as f:
    #         cont = f.read()
    #         tmptxt = str(binascii.hexlify(cont))
    #         fff = open('bidule.txt', 'w')
    #         fff.write(tmptxt)
    #         fff.close()
    #
    #         P_Prefs = pickle.loads(f.read())
    #
    #         # Reset these variables
    #         P_Prefs.title_selected = 0
    #         P_Prefs.options_scene_selected = 0
    # except:

    P_Prefs = PlayerPrefs()

    # Play music
    music = load_sound('ost_fighter.ogg', 'data/sfx/', P_Prefs.music_vol)
    # sm = pygame.mixer.Sound("data/sfx/ost_fighter.ogg")  # load("data/sfx/ost_fighter.ogg")
    # sm.set_volume(P_Prefs.music_vol)
    music.play(-1)
    print('sm.play called')

    # Set window flags
    # window_flags = HWACCEL | DOUBLEBUF
    # if P_Prefs.is_fullscreen:
    #     window_flags = window_flags | FULLSCREEN
    # if P_Prefs.is_frameless:
    #     window_flags = window_flags | NOFRAME

    # Initialize the window

    # if P_Prefs.is_fullscreen:
    # window = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), window_flags)
    # else:

    if True:
        w = int(WIN_RES["w"]) * SCALE
        h = int(WIN_RES["h"]) * SCALE
        w, h = cgmconf.CONST_SCR_SIZE
        window = pygame.display.set_mode((w, h))  # , window_flags)

    pygame.display.set_caption(TITLE)
    # pygame.display.set_icon(load_img("icon.png", IMG_DIR, 1))
    pygame.mouse.set_visible(False)

    # Create a scene manager
    glvars.title_scene = TitleScene(P_Prefs)

    manager = SceneManager(glvars.title_scene)

    # Create Render target
    # render_target = pygame.Surface((WIN_RES["w"], WIN_RES["h"]))
    render_target = pygame.Surface((320, 480))

    # Loop variables
    # clock = pygame.time.Clock()
    # running = True
    # prev_time = time.time()
    # dt = 0

    li_receivers = [
        ScreenUpdater(),
        GameLogicUpdater(),
        kataen.get_game_ctrl()
    ]
    for e in li_receivers:
        e.turn_on()
    li_receivers[-1].loop()


if __name__ == "__main__":
    run_game()
    kataen.cleanup()
