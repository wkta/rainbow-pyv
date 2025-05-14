"""
----------------------------
 mConquest: the game
----------------------------

inspired by the "Dice WARS" browser-game

inspired by a software using pygame & written
 in 2006-03-06 by DR0ID (see http://mypage.bluewin.ch/DR0ID)
"""


import pygame
import coremon_main.conf_eng as cgmconf

if not cgmconf.runs_in_web():
    import sys
    sys.path.append('../../scripts/Lib/site-packages')

# import coremon_main.engine as coremon


from coremon_main.httpserver import HttpServer
from coremon_netw.AsyncMessagingCtrl import AsyncMessagingCtrl


from gamecrm.defs_mco.gamestates import GameStates


# sans proxied Http
# from cgm_engine.networking.EnvoiAsynchrone2 import EnvoiAsynchrone2
import gamecrm.defs_mco.glvars as glvars


# ------------------------------------------------
#  programme principal
# ------------------------------------------------
def run():
    if cgmconf.runs_in_web():
        glvars.server_port = 80
        glvars.server_host = 'sc.gaudia-tech.com'
    else:
        # lecture depuis ../server.cfg & enregistrement dans glvars
        # le format du fichier .cfg étant tout simple:
        # host\n
        # port\n
        glvars.load_server_config()

    serv = HttpServer.instance()
    serv.proxied_get('http://{}:{}/tom/resetgame.php'.format(glvars.server_host, glvars.server_port), {})
    serv.set_debug_info(True)  # glvars.server_debug)

    etq = 'M-Conquest: a multiplayer game like no other'  # RQ: devrait-on importer ca des var globales?

    # TEMP desactivé
    if not cgmconf.runs_in_web():
        import os
        pygame.display.set_caption(etq)
        inweb = False
        if not inweb:
            logo = pygame.image.load(os.path.join('data', 'images', 'globe.png'))
            pygame.display.set_icon(logo)

    glvars.init_fonts_n_colors()

    # TEMP desactivé
    #if not cgmconf.runs_in_web():
    async_ctrl = AsyncMessagingCtrl()
    async_ctrl.turn_on()

    # using a stack based runner
    from coremon_main.engine import StackBasedGameCtrl

    game_ctrl = StackBasedGameCtrl(GameStates, GameStates.Login)

    game_ctrl.turn_on()
    game_ctrl.loop()


if __name__ == '__main__':
    run()
