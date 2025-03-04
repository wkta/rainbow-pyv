from . import glvars


pyv = glvars.pyv


__all__ = [
    'controls_sys',
    'physics_sys',
    'rendering_sys',
    'gamectrl_sys',
    'endgame_sys'
]


def interpolate_color(x, y) -> tuple:
    # return 150, (x * 0.27) % 256, (y * 1.22) % 256
    return 150, (x * 0.45) % 256, (y * 1.42) % 256

def controls_sys(dt):
    player = pyv.ecs.find_by_archetype('player')[0]
    active_keys = pyv.get_pressed()
    if active_keys[pyv.keycodes.K_LEFT]:
        player['speed'] = -glvars.PLAYER_SPEED
    elif active_keys[pyv.keycodes.K_RIGHT]:
        player['speed'] = glvars.PLAYER_SPEED
    else:
        player['speed'] = 0.0


def endgame_sys(dt):
    classic_ftsize = 38
    ball = pyv.ecs.find_by_archetype('ball')[0]
    bpy = ball['body'].top
    if bpy > glvars.scr_height:
        ft = pyv.new_font_obj(None, classic_ftsize)
        glvars.end_game_label = ft.render('Game Over', False, (255, 255, 255))

    # has destroyed all blocks
    blocks = pyv.ecs.find_by_archetype('block')
    if not len(blocks):  # no more blocks!
        ft = pyv.new_font_obj(None, classic_ftsize)
        glvars.end_game_label = ft.render('Victory!', False, (255, 255, 255))


def physics_sys(dt):
    if glvars.end_game_label is not None:  # block all movements when game over
        return
    # PLAYER MOVEMENT
    player = pyv.ecs.find_by_archetype('player')[0]
    px, py = player['body'].topleft
    vx = player['speed']
    plwidth = player['body'].w
    targetx = px + vx * dt
    if not(targetx < 0 or targetx > glvars.scr_width-plwidth):
        player['body'].x = targetx

    # ##################BALL MOVEMENT
    ball = pyv.ecs.find_by_archetype('ball')[0]
    speed_x = ball['speed_X']
    speed_y = ball['speed_Y']
    bpx, bpy = ball['body'].topleft
    ball['body'].x = bpx + dt*speed_x
    ball['body'].y = bpy + dt*speed_y

    if bpx < 0:
        ball['speed_X'] *= -1.0
        ball['body'].x = 0
    elif ball['body'].right > glvars.scr_width:
        ball['speed_X'] *= -1.0
        ball['body'].right = glvars.scr_width
    if bpy < 0:
        ball['speed_Y'] *= -1.0
        ball['body'].top = 0

    # ######################Collision
    if player['body'].colliderect(ball['body']):
        ball['body'].bottom = player['body'].top  # stick to the pad
        ball['speed_Y'] *= -1.0

    # ######################Collision block
    blocks = pyv.ecs.find_by_archetype('block')
    for block in blocks:
        if ball['body'].colliderect(block['body']):
            ball['speed_Y'] *= -1.0
            pyv.ecs.delete_entity(block)
            break


def rendering_sys(dt):
    """
    displays everything that can be rendered
    """
    scr = pyv.get_surface()
    scr.fill(glvars.bgcolor)
    li_blocks = pyv.ecs.find_by_archetype('block')
    for b in li_blocks:
        pyv.draw_rect(scr, interpolate_color(b['body'][0], b['body'][1]), b['body'])

    pl_ent = pyv.ecs.find_by_archetype('player')[0]
    pyv.draw_rect(scr, 'white', pl_ent['body'])

    if glvars.end_game_label:
        lw, lh = glvars.end_game_label.get_size()
        scr.blit(
            glvars.end_game_label, ((glvars.scr_width-lw)//2, (glvars.scr_height-lh)//2)
        )
    else:
        ball = pyv.ecs.find_by_archetype('ball')[0]
        pyv.draw_rect(scr, 'blue', ball['body'])


def gamectrl_sys(dt):
    for ev in pyv.event_get():
        if ev.type == pyv.EngineEvTypes.Quit:
            pyv.set_gameover()
        elif ev.type == pyv.EngineEvTypes.Keydown:
            if ev.key == pyv.keycodes.K_ESCAPE:
                pyv.set_gameover()
