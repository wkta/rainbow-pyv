
# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi

from game_events import MyEvTypes

EngineEvTypes = kengi.event.EngineEvTypes
EventReceiver = kengi.event.EventReceiver
pygame = kengi.pygame


class AvatarView(EventReceiver):
    """
    repr graphique avatar dans l'écran principal du jeu
    """
    def __init__(self, refmod):
        super().__init__()
        self._avatar = refmod
        self._scr_size = kengi.get_surface().get_size()

        approx_height = 80
        self._x_BASEPOS = self._scr_size[0]
        self._y_BASEPOS = (self._scr_size[1] - approx_height)//2

        self._labels = self._lblsizes = None

        self._pos_logos = list()

        self.refresh_disp()

    def refresh_disp(self):
        # two temp variables
        ft = pygame.font.Font(None, 19)
        txtcolor = (16, 16, 128)

        # -- do the job for avatar stats
        self._labels = list()
        self._lblsizes = list()
        alltexts = [
            '{}:'.format(self._avatar.name),
            'LEVEL {}'.format(self._avatar.level),
            'xp: {} / {}'.format(self._avatar.curr_xp, self._avatar.xp_next_level),
            # TODO
            #'Ini={} | En={}'.format(self._avatar.ini, self._avatar.en),
            #'Hp: {}/{}'.format(self._avatar.curr_hp, self._avatar.max_hp)
        ]
        for txt in alltexts:
            tmp = ft.render(txt, True, txtcolor)
            self._labels.append(tmp)
            self._lblsizes.append(tmp.get_size())

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            scr = ev.screen

            # draw a rect for avatar stats...
            smallest_x = float('inf')
            tempx = dict()
            for k, lbl in enumerate(self._labels):
                t = self._lblsizes[k]
                tempx[k] = self._x_BASEPOS - 8 - t[0]
                if smallest_x > tempx[k]:
                    smallest_x = tempx[k]

            trect = ((smallest_x, self._y_BASEPOS), (self._scr_size[0] - smallest_x - 8, 192))
            pygame.draw.rect(ev.screen, 'steelblue', trect, 2)

            for k, lbl in enumerate(self._labels):
                ev.screen.blit(lbl, (tempx[k], self._y_BASEPOS + 24 * k))

        elif ev.type == MyEvTypes.AvatarUpdate:
            self.refresh_disp()
