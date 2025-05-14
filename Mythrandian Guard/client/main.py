""""
** Mythrandian Guard **
a game of Heroes and Lackeys
un jeu de Héros et de Laquais

project started by: wkta-tom (contact@kata.games )
+ authored by various users see the CONTRIBUTORS file
started in Dec. 2021

important notice:
All project files (source-code) that ARE NOT part of katagames_sdk
are licensed under the:
MIT License
"""

# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi
kengi.bootstrap_e()

import game_defs
import glvars

from app.battle_state import BattleState
from app.magery_state import MageryState
from app.main_screen_state import MainScreenState
from app.shopping_state import ShoppingState
from game_defs import GameStates

print('Mythrandian Guard demo: /!\\ Current kengi version is: ', kengi.ver)

CgmEvent = kengi.event.CgmEvent
StackBasedGameCtrl = kengi.event.StackBasedGameCtrl
# CgmEvent.inject_custom_names(MyEvTypes)

# - main program
kengi.init()
WIN_CAPTION = 'Mythrandian Guard'
kengi.pygame.display.set_caption(WIN_CAPTION)
# bios_like_st = KataFrameState(-1, 'bios-like', game_defs)

kengi.declare_states(
    game_defs.GameStates,
    {
        GameStates.MainScreen: MainScreenState,
        GameStates.Battle: BattleState,
        GameStates.Shopping: ShoppingState,
        GameStates.Magery: MageryState
    },    glvars,
)
ctrl = kengi.get_game_ctrl()

ctrl.turn_on()
ctrl.loop()
kengi.quit()
print('clean exit OK')
