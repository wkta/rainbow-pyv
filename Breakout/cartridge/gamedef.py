from . import glvars
from . import systems
from .world import blocks_create, player_create, ball_create


pyv = glvars.pyv


def init(vmst=None):

    pyv.init(3, wcaption='Pyv Breaker')
    
    screen = pyv.get_surface() 
    glvars.scr_width, glvars.scr_height = screen.get_size()
    glvars.bgcolor = pyv.pal.c64.darkgray

    pyv.ecs.define_archetype('player', ('body', 'speed', 'controls'))
    pyv.ecs.define_archetype('block', ('body', ))
    pyv.ecs.define_archetype('ball', ('body', 'speed_Y', 'speed_X'))

    blocks_create()
    player_create()
    ball_create(glvars.scr_width/2, glvars.scr_height/2)
    pyv.ecs.bulk_add_systems(systems)


def update(time_info=None):
    if glvars.prev_time_info:
        dt = (time_info - glvars.prev_time_info)
    else:
        dt = 0
    glvars.prev_time_info = time_info

    pyv.ecs.systems_proc(dt)
    pyv.flip()


def close(vmst=None):
    pyv.close_game()
    print('gameover!')
