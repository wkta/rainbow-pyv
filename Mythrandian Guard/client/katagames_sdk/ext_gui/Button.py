from ..engine.foundation.events import EventReceiver
from .. import engine as kataen


# import pygame
pygame = kataen.pygame


class ButtonPanel(EventReceiver):

    def __init__(self, button_list=None, callbacks=None):
        super().__init__()
        self._lb = list()
        if button_list:
            self._lb.extend(button_list)

        if callbacks:
            self._callbacks = callbacks
        else:
            self._callbacks = dict()

    def proc_event(self, ev, source):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            for bobj in self._lb:
                if bobj.rect.collidepoint(ev.pos):
                    try:
                        self._callbacks[bobj.ident]()
                    except KeyError:
                        self.pev(kataen.EngineEvTypes.BTCLICK, bt_ident=bobj.ident)


class Button(pygame.sprite.Sprite):

    free_bt_identifier = 77348

    def __init__(self, pos=None, size=None, label='bt_label'):
        super().__init__()
        self.callback = None

        self.ident = Button.free_bt_identifier
        Button.free_bt_identifier += 1

        if size:
            self._w, self._h = size
        if pos:
            self.pos = list(pos)
        self.image = pygame.surface.Surface((self._w, self._h))
        self.image.fill('gray')

        tmp_font = pygame.font.Font(None, 18)
        self._lbl = tmp_font.render(label, True, 'navyblue')
        self.label = label
        offsetx = self._lbl.get_width() // 2
        offsety = self._lbl.get_height() // 2
        cx, cy = self._w//2, self._h//2
        self.image.blit(self._lbl, (cx - offsetx, cy - offsety))

        pygame.draw.rect(self.image, 'navyblue', (0, 0, self._w-1, self._h-1), 2)

        # adjust position
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
