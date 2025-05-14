"""
fight simulator (only the view)

this will be used both in mission & PvP (raids).

This will stay on the client-side
"""
import pygame


# ------------
# define screen positions (math coordinates)
# ------------

# format: top-left corner, bottom-right corner
math_viewport = [(-15.5, 18.0), (15.5, -2.25)]

mpositions = {
    # first team
    1: (-13.1, 6),
    2: (-11.5, 10),
    3: (-9.9, 14),
    4: (-7.9, 10),
    5: (-7.6, 6),
    6: (-4.4, 14),
    7: (-4.1, 10)
}
temp = dict()
for k, elt in mpositions.items():  # symetrie par axe x de tous les pts
    temp[-k] = (-1*elt[0], elt[1])
mpositions.update(temp)


def map_to_screen(math_sys_pos):
    yoffset = 32
    xbinf = math_viewport[0][0]
    xbsup = math_viewport[1][0]
    x = 960 * (math_sys_pos[0] - xbinf) / abs(xbsup - xbinf)
    gamma = ((math_sys_pos[1] + 2.25) / 20.25)
    y = 540 * (1 - gamma)  # map to screen coords
    y += yoffset
    return x, y


# ------------
# how to draw
# ------------
def draw_fighters(screen, right_team, col, battlemod):
    global mpositions
    ft = pygame.font.Font(None, 22)
    alive_f_li = battlemod.det_idx_live_fighters(right_team)
    for n in range(1, 8):
        i = -n if right_team else n
        if i in alive_f_li:
            x, y = map_to_screen(mpositions[i])

            fighter_obj = battlemod[i]
            if not fighter_obj.ranged:
                pygame.draw.circle(screen, col, (x, y), 8)
            else:
                pygame.draw.rect(screen, col, ((x-6, y-6), (12, 12)))

            fighterinfo = str(fighter_obj)
            for j, txtchunk in enumerate(fighterinfo.split("\n")):
                tile = ft.render(txtchunk, False, 'gray')
                screen.blit(tile, (x-tile.get_size()[0]//2, y+(j+1)*14))
