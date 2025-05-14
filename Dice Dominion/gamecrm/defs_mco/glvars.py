
multiplayer_mode = None  # sera déterminé en fct de s'il y a des joueurs "remote"

server_host = None  # recevra un str
server_port = None  # recevra un int
server_debug = None

# --- constantes permettant ajuster affichage...
# grid_myst_parameter = (31, 27)
grid_myst_parameter = (31, 27)
gr_size = (30, 27)
gr_offset = (60, 70)

# graphics
screen_width = 800
screen_height = 600
flags = None  # not used at the moment, or better each option seperate?
frames_per_sec = 30

# needed by gamelogic in Multigame and Singlegame
single_player = True
# TODO: these two must be set in Multivote or in Singleoptions

local_pid = 0  # par défaut cest 0 ET le netw_spinner est set à ZÉRO

gl_conquest_mod = None

players = []  # [player]

world = None

player_infos = []  # - nouveauté !

# un code repr. le type d'adversaire

colors = dict()
fonts = dict()


def load_server_config():
    global server_host, server_port, server_debug

    import os
    f = open(os.path.join('server.cfg'))
    config_externe = f.readlines()

    k = int(config_externe[0])
    server_debug = False if (k == 0) else True
    server_host = config_externe[1].strip("\n")
    server_port = int(config_externe[2])


def init_fonts_n_colors():
    global colors, fonts
    import pygame
    import os
    from gamecrm.defs_mco.fonts_n_colors import my_fonts, my_colors

    pygame.font.init()

    for name, v in my_colors.items():
        colors[name] = pygame.Color(v)

    ressource_loc_li = ['.']
    for name, t in my_fonts.items():
        if t[0] is not None:
            tmp = list(ressource_loc_li)
            tmp.append(t[0])
            source = os.path.join(*tmp)
        else:
            source = None
        fonts[name] = pygame.font.Font(source, t[1])

    print('chargement fonts_n_colors *** OK!')


#
##@Singleton
##class AppConstants(BaseAppConstants):
##
##    def _define_constants(self):
##        return {
##            'program_caption': 'MobiConquest - a multiplayer game like no other',
##            'logo_filename': 'globe.png',  # anciennement 'logo32x32.png'
##
##            'scr_size': (800, 600),
##            'flags': None,  # not used at the moment, or better each option seperate?
##            'max_fps': 45,
##
##            'debug_mode': True,
##            'pack_assets': False,
##        }
