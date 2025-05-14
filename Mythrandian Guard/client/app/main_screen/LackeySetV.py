# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi

import app.main_screen.gui_description as frame


EventReceiver = kengi.event.EventReceiver
EngineEvTypes = kengi.event.EngineEvTypes
pygame = kengi.pygame


class LackeySetV(EventReceiver):
    """
    here, we describe how lackeys should be displayed (Main Screen gamestate)

    there is an interaction with a special MODEL,
    this on represents the current "configuration" the player is using.

    Indeed, lackeys can be drag'n'dropped in missions or
    """

    def __init__(self, ref_avatar):
        super().__init__()
        self._avatar = ref_avatar
        self._lackey_labels = list()
        self._pos_logos = list()

        self.refresh_infos()
        self._title_label = kengi.gui.Label('Your army:', 'salmon')
        self._title_label.rect.center = frame.CENTERPOS_LACKEY_TITLE

        self._generic_face = pygame.transform.scale(pygame.image.load('assets/portrait23.png'), (60, 60))

    def refresh_infos(self):
        ft = pygame.font.Font(None, 25)
        txtcolor = (89, 77, 121)

        # -- do the job for lackey logos
        tmp_li_names = self._avatar.get_team_desc().split('\n')
        del self._pos_logos[:]  # clear old list
        base_x_logos = 140
        base_y_logos = 233
        offsetx = 70
        for k, elt in enumerate(tmp_li_names):
            self._pos_logos.append(
                (base_x_logos + k*offsetx, base_y_logos)
            )

        del self._lackey_labels[:]
        for txt in tmp_li_names:
            tmp = ft.render(txt, True, txtcolor)
            self._lackey_labels.append(tmp)

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            self._do_paint(ev.screen)

    def _do_paint(self, scr):
        pygame.draw.rect(scr, 'black', self._title_label.rect)
        scr.blit(self._title_label.image, self._title_label.rect.topleft)

        tmp = self._avatar.get_team_desc().split('\n')
        tmp[0] = 'your hero'

        for rank, elt in enumerate(tmp):
            col = rank // frame.LACKEYS_PER_COL
            row = rank % frame.LACKEYS_PER_COL
            tpos = (
                frame.FIRST_LACKEY_POS[0] + col * frame.LACKEY_X_OFFSET,
                frame.FIRST_LACKEY_POS[1] + row * frame.LACKEY_Y_OFFSET,
            )
            scr.blit(self._generic_face, tpos)

        # draw all lackeys +their infos
        # for k, pos in enumerate(self._pos_logos):
        #     pygame.draw.rect(scr, 'orange', (self._pos_logos[k], (50, 50)))
        #     lbl = self._lackey_labels[k]
        #     scr.blit(lbl, pos)
