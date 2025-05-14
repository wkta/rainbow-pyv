# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi
import game_defs


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


class MyAnimSpr(kengi.anim.AnimatedSprite):
    def draw(self, scr, flipped=False):
        scr.blit(pygame.transform.flip(self.image, flip_x=flipped, flip_y=0), self.rect.topleft)


class BattleV(kengi.event.EventReceiver):
    """
    in theory
    The Battle View is used on both missions(PvM) & raids(PvP).

    This is the LEGIT view that uses animations (& spritesheets)
     to display whats going on during the battle
    what im doing here?

    converting the most primitive view one can think of... (That is squares and disks to represent fighters)
    + blue solid color background screen)
    to the same feature but with an EventReceiver structure (->kengi style)

    """
    def __init__(self, refbattle):
        # we can have up to 14 fighters to display
        super().__init__()

        self.slot_2fighter_asprite = dict()
        for alpha in (1, -1):
            for idx in range(1, 8):
                ke = alpha*idx
                print(ke)
                if refbattle.has_fighter_at(ke):
                    tmp = refbattle[ke]  # TODO use infos from model to pick the anim spr!

                    temp_asprite = MyAnimSpr('assets/knightye_sheet')
                    temp_asprite.preload()
                    # set animated sprite position
                    math_sys_pos = mpositions[ke]
                    temp_asprite.rect.center = map_to_screen(math_sys_pos)
                    self.slot_2fighter_asprite[ke] = temp_asprite

        self._battle = refbattle

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            ev.screen.fill(game_defs.BG_COLOR)
            self.draw_fighters(ev.screen, self._battle)

    def draw_fighters(self, screen, battlemod):
        global mpositions
        ft = pygame.font.Font(None, 22)

        for right_team in (False, True):
            alive_f_li = battlemod.det_idx_live_fighters(right_team)
            for n in range(1, 8):
                i = -n if right_team else n
                if i in alive_f_li:
                    # x, y = map_to_screen(mpositions[i])
                    x, y = self.slot_2fighter_asprite[i].rect.center
                    y+=33

                    fighter_obj = battlemod[i]
                    # if not fighter_obj.ranged:
                    #     pygame.draw.circle(screen, col, (x, y), 8)
                    # else:
                    #     pygame.draw.rect(screen, col, ((x-6, y-6), (12, 12)))

                    self.slot_2fighter_asprite[i].draw(screen, not right_team)  # flip if left team

                    fighterinfo = str(fighter_obj)
                    for j, txtchunk in enumerate(fighterinfo.split("\n")):
                        tile = ft.render(txtchunk, False, 'black')
                        screen.blit(tile, (x-tile.get_size()[0]//2, y+(j+1)*14))
