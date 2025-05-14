# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi


pygame = kengi.pygame
EngineEvTypes = kengi.event.EngineEvTypes


# constants
# it defines screen positions (math coordinates)
# format: top-left corner, bottom-right corner
math_viewport = [
    (-15.5, 18.0), (15.5, -2.25)
]
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


class DebugBattleV(kengi.event.EventReceiver):
    """
    in theory
    The Battle View is used on both missions(PvM) & raids(PvP).

    what im doing here?

    converting the most primitive view one can think of... (That is squares and disks to represent fighters)
    + blue solid color background screen)
    to the same feature but with an EventReceiver structure (->kengi style)

    """
    def __init__(self, refbattle):
        super().__init__()
        self._battle = refbattle

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            ev.screen.fill('darkblue')
            self.draw_fighters(ev.screen, 'orange', self._battle)

    def draw_fighters(self, screen, col, battlemod):
        global mpositions
        ft = pygame.font.Font(None, 22)

        for right_team in (False, True):
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
