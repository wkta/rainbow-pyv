from . import glvars
from .glvars import pyv

pyv.bootstrap_e()

from .actors import *


def _prepare_images():
    Sprsheet = pyv.gfx.LegacySpritesheet
    #grid_rez = (32, 32)
    grid_rez = (16,16)
    # tileset:
    img = pyv.images['tileset']
    #glvars.tileset = Sprsheet(img, 2)  # use upscaling x2
    glvars.tileset = Sprsheet(img)
    glvars.tileset.set_infos(grid_rez)
    # player:
    img = pyv.images['avatar1']
    planche_avatar = Sprsheet(img) #, 2)  # upscaling x2
    planche_avatar.colorkey = (255, 0, 255)  # TODO in web ctx i dont know if this works
    planche_avatar.set_infos(grid_rez)
    glvars.avatar_img = planche_avatar.image_by_rank(0)
    # monster:
    mstr_img = pyv.images['monster']
    # downscaling
    glvars.monster_img = pyv.surface_transform(mstr_img, (16,16))
    glvars.monster_img.set_colorkey((255, 0, 255))


def init(vmst=None):
    pyv.init(3, wcaption='Roguelike actor-based')

    _prepare_images()
    # pyv.set_debug_flag()
    pyv.actors.declare_evs(
        'spawn',  # it's like a teleport
        'player_input',
        # 'player_kicks',
        'game_restart',
        'player_movement',
        'req_refresh_maze',
        'maze_generated',
        'item_destroyed',
        'player_death',
        'player_spawn'
    )

    maze_id = new_maze()
    glvars.ref_maze = maze_id
    # this allows to add a fog-of-war, plus line and sight, effect
    glvars.ref_visibility_mger = new_visibility_mger(maze_id)

    pyv.actors.trigger('terrain_gen', maze_id)  # maze will spawn a player
    glvars.ref_player = pyv.actors.peek(maze_id).ref_player  # we copy the ref
    glvars.ref_gui = new_gui()


def update(curr_t=None):
    evtypes = pyv.EngineEvTypes
    for ev in pyv.event_get():
        if ev.type == evtypes.Quit:
            pyv.set_gameover()
        elif ev.type == evtypes.Keydown:
            if ev.key == pyv.keycodes.K_ESCAPE:
                pyv.vars.gameover = True
            elif ev.key == pyv.keycodes.K_SPACE:
                pyv.post_ev('game_restart')
            elif ev.key == pyv.keycodes.K_k:  # "k" like kill
                glvars.avatar_hp = -100
                print('suicide!')
                pyv.post_ev("player_death")
            else:
                if glvars.game_paused:
                    continue
                if ev.key == pyv.keycodes.K_LEFT:
                    pyv.post_ev("player_input", dir="left")
                elif ev.key == pyv.keycodes.K_RIGHT:
                    pyv.post_ev("player_input", dir="right")
                elif ev.key == pyv.keycodes.K_UP:
                    pyv.post_ev("player_input", dir="up")
                elif ev.key == pyv.keycodes.K_DOWN:
                    pyv.post_ev("player_input", dir="down")

    pyv.post_ev('update', info_t=curr_t)
    pyv.post_ev('draw', screen=pyv.vars.screen)

    pyv.process_evq()
    pyv.flip()


def close(vmst=None):
    pyv.close_game()
    print('roguelike: over')
