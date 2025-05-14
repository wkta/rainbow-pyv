import json

from . import rpgmenu
from ... import _hub
from ... import event
from ... import pal
from ...compo import gfx


frects = _hub.polarbear.frects
pygame = _hub.pygame
EngineEvTypes = event.EngineEvTypes


class Offer:
    """
    An Offer is a single line spoken by the NPC, "effect" is
    a callable with no parameters.
    "replies" is a list of replies.
    """
    def __init__(self, msg, effect=None, replies=()):
        self.msg = msg
        self.effect = effect
        self.replies = list(replies)

    def __str__(self):
        return self.msg

    @classmethod
    def from_json(cls, jdict):
        # We spoke about not needing a json loader yet. But, in terms of hardcoding
        # a conversation, it was just as easy to write this as to hand-code a dialogue tree.
        msg = jdict.get("msg", "Hello there!")
        effect = None
        replies = list()
        for rdict in jdict.get("replies", ()):
            replies.append(Reply.from_json(rdict))
        return cls(msg, effect, replies)

    @classmethod
    def load_jsondata(cls, jsondata):
        return cls.from_json(json.loads(jsondata))


class Reply:
    """
    A Reply is a single line spoken by the PC, leading to a new offer
    """
    def __init__(self, msg, destination=None):
        self.msg = msg
        self.destination = destination

    def __str__(self):
        return self.msg

    def apply_to_menu(self, mymenu):
        mymenu.add_item(self.msg, self.destination)

    @classmethod
    def from_json(cls, jdict):
        msg = jdict.get("msg", "And you too!")
        destination = jdict.get("destination")
        if destination:
            destination = Offer.from_json(destination)
        return cls(msg, destination)


class ConversationView(event.EventReceiver):
    """
    The View is used by the conversation when conversing.
    It has a "text" property and "render", "get_menu" methods.
    """
    TEXT_AREA = frects.Frect(-75, -100, 300, 100)
    MENU_AREA = frects.Frect(-75, 30, 300, 80)
    PORTRAIT_AREA = frects.Frect(-240, -110, 150, 225)
    BGCOL = (11, 24, 11)  # pal.c64['darkgrey']  # pal.punk['nightblue']
    MENU_BORDER_COL = pal.punk['gray']
    DEBUG = True

    def __init__(self, root_offer, chosen_font, ft_size, portrait_fn=None, pre_render=None, li_alt_font_obj=None):
        # --------------------
        #  constructor
        # --------------------
        super().__init__()

        # n.b: need to use EmbeddedCfont, or no?
        if li_alt_font_obj:  # defaults to capello ft
            self.capfont = li_alt_font_obj
            # self.capfont = [
            #     gfx.JsonBasedCfont(capfont_path_prfix + '-b'),  # blue-ish
            #     gfx.JsonBasedCfont(capfont_path_prfix+'-a'),  # orange
            # ]
        else:
            self.capfont = None

        # - slight optim:
        self.text_rect = None
        self.menu_rect = None
        self.portrait_rect = None

        # can be used to make things faster for webctx
        self._primitive_style = False
        self.zombie = False
        self.text = ''
        self.root_offer = root_offer
        self.pre_render = pre_render
        self.font = pygame.font.Font(chosen_font, ft_size)
        if portrait_fn:
            self.portrait = pygame.image.load(portrait_fn).convert_alpha()
        else:
            self.portrait = None
        self.curr_offer = root_offer
        self.dialog_upto_date = False
        self.existing_menu = None

    def proc_event(self, ev, source):
        if self.existing_menu:  # forward event to menu if it exists
            self.existing_menu.proc_event(ev, None)

        if ev.type == EngineEvTypes.LOGICUPDATE:  # TODO: using L.u. isnt great!
            self.update_dialog()

        elif ev.type == EngineEvTypes.PAINT:
            if self.primitive_style:
                self._primitiv_render(ev.screen)
            else:
                self._reg_render(ev.screen)

        elif ev.type == EngineEvTypes.CONVCHOICE:  # ~ iterate over the conversation...
            print('ConvChoice event received by', self.__class__.__name__)
            self.dialog_upto_date = False
            self.curr_offer = ev.value

    def _primitiv_render(self, refscreen):
        pygame.draw.rect(refscreen, self.BGCOL, self.glob_rect)  # fond de fenetre
        pygame.draw.rect(refscreen, self.BGCOL, self.text_rect)

        #if not self.capfont:
            # old fashion

        _hub.polarbear.image.draw_text(
            self.capfont[0] if self.capfont else self.font, self.text, self.text_rect)

        #else:  # we've overriden the basic behavior
            # signatur is:
            #  text_to_surf(self, w, refsurf, start_pos, spacing=0, bgcolor=None)
        #    self.capfont[0].text_to_surf(self.text, refscreen, (self.text_rect[0], self.text_rect[1]))

        if self.portrait:
            refscreen.blit(self.portrait, self.portrait_rect)
        pygame.draw.rect(refscreen, self.BGCOL, self.menu_rect)

        if self.existing_menu:  # draw what the player can SAY
            if not self.capfont:
                # old fashion
                self.existing_menu.render(refscreen)
            else:  # we've overriden the basic behavior
                self.existing_menu.alt_render(refscreen, self.capfont[0], self.capfont[1])
            #    self.existing_menu.alt_render(refscreen, self.capfont[0], self.capfont[1])

        # pourtour menu
        pygame.draw.rect(refscreen, self.MENU_BORDER_COL, (self.taquet_portrait, 148, self.dim_menux, 88), 2)

    def _reg_render(self, refscreen):
        if self.pre_render:
            self.pre_render()
        text_rect = self.TEXT_AREA.get_rect()
        dborder = _hub.polarbear.default_border
        dborder.render(text_rect)
        _hub.polarbear.draw_text(self.font, self.text, text_rect)
        dborder.render(self.MENU_AREA.get_rect())
        if self.existing_menu:
            self.existing_menu.render(refscreen)
        if self.portrait:
            refscreen.blit(self.portrait, self.PORTRAIT_AREA.get_rect())

    @property
    def primitive_style(self):
        return self._primitive_style

    @primitive_style.setter
    def primitive_style(self, v):
        self._primitive_style = v

        # modify locations as we know that (Primitive style => upscaling is set to x3)
        x = 48
        w = 192
        self.refxxx = x

        self.TEXT_AREA = frects.Frect(-x, -66, w, 80)
        self.MENU_AREA = frects.Frect(-x, 33, w, 80)
        self.PORTRAIT_AREA = frects.Frect(-x-100, -66, 90, 128)

        # optim:
        self.dim_menux = w+104

        self.text_rect = self.TEXT_AREA.get_rect()
        self.menu_rect = self.MENU_AREA.get_rect()
        self.portrait_rect = self.PORTRAIT_AREA.get_rect()
        self.taquet_portrait = self.portrait_rect[0]
        self.glob_rect = pygame.Rect(self.portrait_rect[0], 53, self.dim_menux, 182)

    def update_dialog(self):
        if self.zombie:
            return

        if self.curr_offer is None:
            # auto-close everything
            self.pev(EngineEvTypes.CONVENDS)
            # let the full program remove the listener
            # self.turn_off()
            self.zombie = True
            return

        if self.dialog_upto_date:
            return

        self.dialog_upto_date = True
        self.text = self.curr_offer.msg

        # create a new Menu inst.
        if self.capfont:
            adhocft = self.capfont[0]
        else:
            adhocft = self.font
        self.existing_menu = rpgmenu.Menu(
            self.MENU_AREA.dx, self.MENU_AREA.dy, self.MENU_AREA.w, self.MENU_AREA.h,
            border=None, predraw=None, font=adhocft
        )
        # predraw: self.render

        mymenu = self.existing_menu
        for i in self.curr_offer.replies:
            i.apply_to_menu(mymenu)
        if self.text and not mymenu.items:
            mymenu.add_item("[Continue]", None)
        else:
            mymenu.sort()
        nextfx = self.curr_offer.effect
        if nextfx:
            nextfx()
