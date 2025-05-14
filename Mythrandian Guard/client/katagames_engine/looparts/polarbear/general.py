import random
import weakref

from . import frects
from . import image
from .image import TEXT_COLOR, truncline, render_text
from ... import _hub
from ...compo import vscreen


pygame = _hub.pygame


class KeyObject(object):
    """A catcher for multiple inheritence. Subclass this instead of object if
       you're going to use multiple inheritence, so that erroneous keywords
       will get caught and identified."""

    def __init__(self, **keywords):
        for k, i in keywords.items():
            print("WARNING: KeyObject got parameters {}={}".format(k, i))


class SingletonMeta(type):
    def __str__(cls):
        return cls.name


class Singleton(object, metaclass=SingletonMeta):
    """For rules constants that don't need to be instanced."""
    name = "Singleton"
    def __init__(self):
        raise NotImplementedError("Singleton can't be instantiated.")


class Border(object):
    def __init__(self, border_width=16, tex_width=32, border_name="", tex_name="", padding=16, tl=0, tr=0, bl=0, br=0,
                 t=1, b=1, l=2, r=2, transparent=True):
        # tl,tr,bl,br are the top left, top right, bottom left, and bottom right frames
        # Bug: The border must be exactly half as wide as the texture.
        self.border_width = border_width
        self.tex_width = tex_width
        self.border_name = border_name
        self.tex_name = tex_name
        self.border = None
        self.tex = None
        self.padding = padding
        self.tl = tl
        self.tr = tr
        self.bl = bl
        self.br = br
        self.t = t
        self.b = b
        self.l = l
        self.r = r
        self.transparent = transparent

    def render(self, dest, scr=None):
        """Draw this decorative border at dest on screen."""
        if scr is None:
            scr = vscreen.get_screen()

        # We're gonna draw a decorative border to surround the provided area.
        if self.border == None:
            self.border = image.Image(self.border_name, self.border_width, self.border_width)
        if self.tex_name and not self.tex:
            self.tex = image.Image(self.tex_name, self.tex_width, self.tex_width)
            if self.transparent:
                self.tex.bitmap.set_alpha(224)

        # Draw the backdrop.
        if self.tex:
            self.tex.tile(dest.inflate(self.padding, self.padding))

        # Expand the dimensions to their complete size.
        # The method inflate_ip doesn't seem to be working... :(
        fdest = dest.inflate(self.padding, self.padding)

        self.border.render((fdest.x - self.border_width // 2, fdest.y - self.border_width // 2), self.tl)
        self.border.render((fdest.x - self.border_width // 2, fdest.y + fdest.height - self.border_width // 2), self.bl)
        self.border.render((fdest.x + fdest.width - self.border_width // 2, fdest.y - self.border_width // 2), self.tr)
        self.border.render(
            (fdest.x + fdest.width - self.border_width // 2, fdest.y + fdest.height - self.border_width // 2), self.br)

        fdest = dest.inflate(self.padding - self.border_width, self.padding + self.border_width)
        scr.set_clip(fdest)
        for x in range(0, fdest.w // self.border_width + 2):
            self.border.render((fdest.x + x * self.border_width, fdest.y), self.t)
            self.border.render((fdest.x + x * self.border_width, fdest.y + fdest.height - self.border_width), self.b)

        fdest = dest.inflate(self.padding + self.border_width, self.padding - self.border_width)
        scr.set_clip(fdest)
        for y in range(0, fdest.h // self.border_width + 2):
            self.border.render((fdest.x, fdest.y + y * self.border_width), self.l)
            self.border.render((fdest.x + fdest.width - self.border_width, fdest.y + y * self.border_width), self.r)
        scr.set_clip(None)


# Monkey Type these definitions to fit your game/assets.
default_border = Border(border_width=8, tex_width=16, border_name="assets/sys_defborder.png", tex_name="assets/sys_defbackground.png",
                        tl=0, tr=3, bl=4, br=5, t=1, b=1, l=2, r=2)
notex_border = Border(border_width=8, border_name="assets/sys_defborder.png", padding=4, tl=0, tr=3, bl=4, br=5, t=1, b=1, l=2,
                      r=2)
# map_border = Border( border_name="sys_mapborder.png", tex_name="sys_maptexture.png", tl=0, tr=1, bl=2, br=3, t=4, b=6, l=7, r=5 )
# gold_border = Border( border_width=8, tex_width=16, border_name="sys_rixsborder.png", tex_name="sys_rixstexture.png", tl=0, tr=3, bl=4, br=5, t=1, b=1, l=2, r=2 )

WHITE = (255, 255, 255)
GREY = (160, 160, 160)

INFO_GREEN = (50, 200, 0)
INFO_HILIGHT = (100, 250, 0)
ENEMY_RED = (250, 50, 0)


class GameState(object):
    def __init__(self, screen=None):
        self.screen = screen
        self.physical_screen = None
        self.view = None
        self.got_quit = False
        self.widgets = list()
        self.widgets_active = True
        self.active_widget_hilight = False
        self._active_widget = None
        self.widget_clicked = False
        self.audio_enabled = True
        self.music = None
        self.music_name = None
        self.music_library = dict()
        self.anim_phase = 0
        self.standing_by = False
        self.notifications = list()

        self.mouse_pos = (0, 0)

    def render_widgets(self):
        if self.widgets:
            for w in self.widgets:
                w.super_render()
        elif self.active_widget_hilight:
            self.active_widget_hilight = False

    def render_notifications(self):
        for n in list(self.notifications):
            n.render()
            if n.is_done():
                self.notifications.remove(n)

    def do_flip(self, show_widgets=True, reset_standing_by=True):
        self.widget_tooltip = None
        if show_widgets:
            self.render_widgets()
        if self.notifications:
            self.render_notifications()
        if self.widget_tooltip:
            x, y = self.mouse_pos
            x += 16
            y += 16
            if x + 200 > self.screen.get_width():
                x -= 200
            myimage = render_text(self.small_font, self.widget_tooltip, 200)
            myrect = myimage.get_rect(topleft=(x, y))
            default_border.render(myrect)
            self.screen.blit(myimage, myrect)
        self.anim_phase = (self.anim_phase + 1) % 6000
        if reset_standing_by:
            self.standing_by = False
        pygame.display.flip()


    def _set_active_widget(self, widj):
        if widj:
            self._active_widget = weakref.ref(widj)
        else:
            self._active_widget = None

    def _get_active_widget(self):
        if self._active_widget:
            return self._active_widget()

    def _del_active_widget(self):
        self._active_widget = None

    active_widget = property(_get_active_widget, _set_active_widget, _del_active_widget)

    def _get_all_kb_selectable_widgets(self, wlist):
        mylist = list()
        for w in wlist:
            if w.active:
                if w.is_kb_selectable():
                    mylist.append(w)
                if w.children:
                    mylist += self._get_all_kb_selectable_widgets(w.children)
        return mylist

    def activate_next_widget(self, backwards=False):
        wlist = self._get_all_kb_selectable_widgets(self.widgets)
        awid = self.active_widget
        if awid and awid in wlist:
            if backwards:
                n = wlist.index(awid) - 1
            else:
                n = wlist.index(awid) + 1
                if n >= len(wlist):
                    n = 0
            self.active_widget = wlist[n]
        elif wlist:
            self.active_widget = wlist[0]

    def resize(self):
        w, h = self.physical_screen.get_size()
        self.screen = pygame.Surface((max(800, 600 * w // h), 600))


INPUT_CURSOR = None
SMALLFONT = None
TINYFONT = None
ITALICFONT = None
BIGFONT = None
ANIMFONT = None
MEDIUMFONT = None
ALTTEXTFONT = None  # Use this instead of MEDIUMFONT when you want to shake things up a bit.
POSTERS = list()

my_state = GameState()
# fix: add ref to screen
my_state.screen = vscreen.get_screen()

# The FPS the rules runs at.
FPS = 30

# Use a timer to control FPS.
TIMEREVENT = pygame.USEREVENT

# Remember whether or not this unit has been initialized, since we don't need
# to initialize it more than once.
INIT_DONE = False


def wrap_with_records(fulltext, font, maxwidth):
    # Do a word wrap, but also return the length of each line including whitespace and newlines.
    done = 0
    wrapped = list()
    line_lengths = list()

    for text in fulltext.splitlines(True):
        done = 0
        while not done:
            nl, done, stext = truncline(text, font, maxwidth)
            wrapped.append(stext.lstrip())
            # wrapped.append(stext)
            line_lengths.append(nl + 1)
            text = text[nl:]
    return wrapped, line_lengths


def wait_event():
    # Wait for input, then return it when it comes.
    ev = pygame.event.wait()

    # Record if a quit event took place
    if ev.type == pygame.QUIT:
        my_state.got_quit = True
    elif ev.type == TIMEREVENT:
        pygame.event.clear(TIMEREVENT)

    # Inform any interested widgets of the event.
    my_state.widget_clicked = False
    if my_state.widgets_active:
        for w in my_state.widgets:
            w.respond_event(ev)

    # If the view has a check_event method, call that.
    if my_state.view and hasattr(my_state.view, "check_event"):
        my_state.view.check_event(ev)

    return ev




def alert(text, font=None):
    if not font:
        font = my_state.medium_font
    # mydest = pygame.Rect( my_state.screen.get_width() // 2 - 200, my_state.screen.get_height()//2 - 100, 400, 200 )
    mytext = render_text(font, text, 400)
    mydest = mytext.get_rect(center=(my_state.screen.get_width() // 2, my_state.screen.get_height() // 2))

    pygame.event.clear([TIMEREVENT, pygame.KEYDOWN])
    while True:
        ev = wait_event()
        if (ev.type == pygame.MOUSEBUTTONUP) or (ev.type == pygame.QUIT) or (ev.type == pygame.KEYDOWN):
            return ev
        elif ev.type == TIMEREVENT:
            if my_state.view:
                my_state.view()
            default_border.render(mydest)
            my_state.screen.blit(mytext, mydest)
            my_state.do_flip()


def alert_display(display_fun):
    pygame.event.clear([TIMEREVENT, pygame.KEYDOWN])
    while True:
        ev = wait_event()
        if (ev.type == pygame.MOUSEBUTTONUP) or (ev.type == pygame.QUIT) or (ev.type == pygame.KEYDOWN):
            break
        elif ev.type == TIMEREVENT:
            if my_state.view:
                my_state.view()
            display_fun()
            my_state.do_flip()


ALLOWABLE_CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890()-=_+,.?"'


def input_string(font=None, redrawer=None, prompt="Enter text below", prompt_color=(255, 255, 255),
                 input_color=TEXT_COLOR, border=default_border):
    # Input a string from the user.
    it = []
    keep_going = True

    if not font:
        font = BIGFONT

    myrect = pygame.Rect(my_state.screen.get_width() / 2 - 200, my_state.screen.get_height() / 2 - 32, 400, 64)
    prompt_image = font.render(prompt, True, prompt_color)

    while keep_going:
        ev = wait_event()

        if ev.type == TIMEREVENT:
            if redrawer != None:
                redrawer()
            border.render(myrect)
            mystring = "".join(it)
            myimage = font.render(mystring, True, input_color)
            my_state.screen.blit(prompt_image, (my_state.screen.get_width() / 2 - prompt_image.get_width() / 2,
                                                my_state.screen.get_height() / 2 - prompt_image.get_height() - 2))
            my_state.screen.set_clip(myrect)
            my_state.screen.blit(myimage, (
            my_state.screen.get_width() / 2 - myimage.get_width() / 2, my_state.screen.get_height() / 2))
            INPUT_CURSOR.render(
                (my_state.screen.get_width() / 2 + myimage.get_width() / 2 + 2, my_state.screen.get_height() / 2),
                ( my_state.anim_phase // 3 ) % 4)
            my_state.screen.set_clip(None)
            my_state.do_flip(False)


        elif ev.type == pygame.KEYDOWN:
            if (ev.key == pygame.K_BACKSPACE) and (len(it) > 0):
                del it[-1]
            elif (ev.key == pygame.K_RETURN) or (ev.key == pygame.K_ESCAPE):
                keep_going = False
            elif (ev.unicode in ALLOWABLE_CHARACTERS) and (len(ev.unicode) > 0):
                it.append(ev.unicode)
        elif ev.type == pygame.QUIT:
            keep_going = False
    return "".join(it)


def please_stand_by(caption=None):
    if not my_state.standing_by:
        img = pygame.image.load(random.choice(POSTERS)).convert()
        dest = img.get_rect(center=(my_state.screen.get_width() // 2, my_state.screen.get_height() // 2))
        my_state.screen.fill((0, 0, 0))
        my_state.screen.blit(img, dest)
        if caption:
            mytext = BIGFONT.render(caption, True, TEXT_COLOR)
            dest2 = mytext.get_rect(topleft=(dest.x + 32, dest.y + 32))
            default_border.render(my_state.screen, dest2)
            my_state.screen.blit(mytext, dest2)
        my_state.standing_by = True
        my_state.do_flip(False, reset_standing_by=False)


class BasicNotification(frects.Frect):
    IP_INFLATE = 0
    IP_DISPLAY = 1
    IP_DEFLATE = 2
    IP_DONE = 3

    def __init__(self, text, font=None, dx=16, dy=16, w=256, h=10, anchor=frects.ANCHOR_UPPERLEFT,
                 border=default_border, count=60, **kwargs):
        font = font or my_state.big_font
        w = min(w, font.size(text)[0])
        self.text_bitmap = render_text(font, text, w)
        h = max(h, self.text_bitmap.get_height())
        super().__init__(dx, dy, w, h, anchor, **kwargs)
        self.border = border
        self.count = count
        self._inflation_phase = self.IP_INFLATE
        self._inflation_count = 0
        my_state.notifications.append(self)

    def render(self):
        if self._inflation_phase == self.IP_INFLATE:
            # Inflating
            mydest = self.get_rect()
            mydest.inflate_ip(-(self.w * (5 - self._inflation_count)) // 6,
                              -(self.h * (5 - self._inflation_count)) // 6)
            self.border.render(mydest)
            self._inflation_count += 1
            if self._inflation_count >= 5:
                self._inflation_phase = self.IP_DISPLAY
        elif self._inflation_phase == self.IP_DISPLAY and self.count > 0:
            self.border.render(self.get_rect())
            my_state.screen.blit(self.text_bitmap, self.get_rect())
            self.count -= 1
        else:
            mydest = self.get_rect()
            mydest.inflate_ip(-(self.w * (5 - self._inflation_count)) // 6,
                              -(self.h * (5 - self._inflation_count)) // 6)
            self.border.render(mydest)
            self._inflation_count -= 1
            if self._inflation_count <= 0:
                self._inflation_phase = self.IP_DONE

    def is_done(self):
        return self._inflation_phase == self.IP_DONE


# PG2 Change
# FULLSCREEN_FLAGS = pygame.FULLSCREEN | pygame.SCALED
# WINDOWED_FLAGS = pygame.RESIZABLE | pygame.SCALED
# FULLSCREEN_RES = (800,600)

# -
# FULLSCREEN_FLAGS = pygame.FULLSCREEN
# WINDOWED_FLAGS = pygame.RESIZABLE
# if sys.platform.startswith("linux"):
#     FULLSCREEN_RES = (800, 600)
# else:
#     FULLSCREEN_RES = (0, 0)
