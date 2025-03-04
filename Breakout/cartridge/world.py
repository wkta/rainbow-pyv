import random
from . import glvars


pyv = glvars.pyv


def player_create():
    player = pyv.ecs.new_from_archetype('player')
    scr_w, scr_h = pyv.get_surface().get_size()

    pyv.ecs.init_entity(player, {
        'speed': 0.0,
        'controls': {'left': False, 'right': False},
        'body': pyv.new_rect_obj(scr_w//2, scr_h-32, glvars.PL_WIDTH, glvars.PL_HEIGHT)
    })


def ball_create(xpos, ypos):
    ball = pyv.ecs.new_from_archetype('ball')
    if random.choice((True, False)):  # right or left direction, randomly
        xvel_tzero = random.uniform(0.33*glvars.MAX_SPEED_BALL, glvars.MAX_SPEED_BALL)
    else:
        xvel_tzero = random.uniform(-glvars.MAX_SPEED_BALL, -0.33 * glvars.MAX_SPEED_BALL)
    pyv.ecs.init_entity(ball, {
        'speed_X': xvel_tzero,
        'speed_Y': glvars.YSPEED_BALL,
        'body': pyv.new_rect_obj(xpos, ypos, glvars.BALL_SIZE, glvars.BALL_SIZE)
    })


def blocks_create():
    bcy = 0
    scr_w = pyv.get_surface().get_size()[0]
    LIMIT = scr_w / (glvars.BLOCK_W + glvars.BLOCK_SPACING)

    for column in range(5):
        bcy = bcy + glvars.BLOCK_H + glvars.BLOCK_SPACING
        bcx = -glvars.BLOCK_W
        for row in range(round(LIMIT)):
            bcx = bcx + glvars.BLOCK_W + glvars.BLOCK_SPACING
            rrect = pyv.new_rect_obj(0 + bcx, 0 + bcy, glvars.BLOCK_W, glvars.BLOCK_H)
            pyv.ecs.init_entity(pyv.ecs.new_from_archetype('block'), {
                'body': rrect
            })
