from browser import bind, document
from browser import window

import katagames_sdk.capsule.engine_ground.conf_eng as cgmconf
import katagames_sdk.capsule.pygame_provider as pygprovider
from katagames_sdk.capsule import event as evmodule
from katagames_sdk.capsule.engine_ground import gfx_updater
from katagames_sdk.capsule.engine_ground.legacy import DeadSimpleManager
from katagames_sdk.capsule.engine_ground.runners import GameTicker
from katagames_sdk.capsule.event import EngineEvTypes, CgmEvent


class HackEvManager(DeadSimpleManager):
    def __init__(self, ref_pygame_pym):
        super().__init__(ref_pygame_pym)
        self.curr_pressed_keys = dict()

    # redef
    def get_pressed_keys(self):
        return self.curr_pressed_keys

    def update(self):
        super()._inject_timed_events()

        # we will assume that self._queue is the full_ev_queue,
        # so anything that needs a fix is done now
        cpt_a = len(self._queue)
        while cpt_a > 0:
            ev = self._queue[0]
            for un_id in self._listener_ids:
                liobj = self._corresp[un_id]
                liobj.proc_event(ev, None)
            del self._queue[0]
            cpt_a -= 1


##        needs_clear = len(self.browser_origin_queue) > 0
##        for ev in self.browser_origin_queue:
##            for un_id in self._listener_ids:
##                liobj = self._corresp[un_id]
##                liobj.proc_event(ev, None)
##        if needs_clear:
##            self.browser_origin_queue = list()


def upgrade_evt_manager(pygame_pym):
    print('web ctx -> UPGRADING evt_manager')
    
    keys_mapping = dict()
    # MAPPING letters a-z
    # , in js 65-90
    # in pygame the 'a' code is 97,
    # => delta (JS->PYG ) is +32
    letters_map = dict()
    for i in range(65, 91):
        letters_map[i] = i + 32
    keys_mapping.update(letters_map)

    # MAPPING numbers
    # same codes are used in JS and pygame,
    # zero is code 48, one 49 etc.
    for i in range(48, 58):
        keys_mapping[i] = i

    # MAPPING misc keys
    keys_mapping.update({
        32: evmodule.PygameBridge.K_SPACE,
        13: evmodule.PygameBridge.K_RETURN,
        27: evmodule.PygameBridge.K_ESCAPE,
    })

    # MAPPING so-called "SPECIAL" keys -> no unicode translation
    spe_keys_mapping = {
        16: evmodule.PygameBridge.KMOD_SHIFT,
        39: evmodule.PygameBridge.K_RIGHT,
        37: evmodule.PygameBridge.K_LEFT,
        38: evmodule.PygameBridge.K_UP,
        40: evmodule.PygameBridge.K_DOWN,
        8: evmodule.PygameBridge.K_BACKSPACE,
        9: evmodule.PygameBridge.K_TAB
    }
    keys_mapping.update(spe_keys_mapping)

    # update the manager so we avoid spamming events in emu pygame letters
    temp_ref = HackEvManager(pygame_pym)
    # & allow pygame_emu to query pressed keys...
    pygprovider.get_module().key.linkto_ev_manager = temp_ref

    for pyg_kcode in keys_mapping.values():
        temp_ref.curr_pressed_keys[pyg_kcode] = False

    # - branchements evt navigateur sur notre pgm python
    @bind(document, "keydown")
    def keyDownHandler(e):  # we shall do the mapping between js events & coremon events
        if e.keyCode not in keys_mapping:
            print('Warning: key code {} unhandled'.format(e.keyCode))
        else:
            pygame_kcode = keys_mapping[e.keyCode]

            if temp_ref.curr_pressed_keys[pygame_kcode]:  # we know it has been pressed already
                pass
            else:
                temp_ref.curr_pressed_keys[pygame_kcode] = True

                if e.keyCode in spe_keys_mapping:
                    unicode_car = ''
                else:
                    unicode_car = chr(pygame_kcode)
                    if e.keyCode in letters_map:  # this is a lower case letter!
                        if temp_ref.curr_pressed_keys[evmodule.PygameBridge.KMOD_SHIFT]:
                            unicode_car = chr(pygame_kcode - 32)  # convert to upper case

                new_evt = CgmEvent(
                    evmodule.PygameBridge.KEYDOWN,
                    key=pygame_kcode,
                    unicode=unicode_car
                )
                temp_ref.post(new_evt)

    # - - --  -bridge with JS events  - - - -  - -
    @bind(document, "keyup")
    def keyUpHandler(e):
        if e.keyCode not in keys_mapping:
            pass
        else:
            pygame_kcode = keys_mapping[e.keyCode]
            if not temp_ref.curr_pressed_keys[pygame_kcode]:  # we know it has been released already
                pass
            else:
                temp_ref.curr_pressed_keys[pygame_kcode] = False
                new_evt = CgmEvent(evmodule.PygameBridge.KEYUP, key=pygame_kcode)
                temp_ref.post(new_evt)

    def handleclick(is_mousdown, clix, cliy, js_bt_code):
        # rectjs = cgmconf.browser_canvas.getBoundingClientRect()
        # res = (clix - rectjs.left, cliy - rectjs.top)

        if is_mousdown:
            adhoctype = evmodule.PygameBridge.MOUSEBUTTONDOWN
        else:
            adhoctype = evmodule.PygameBridge.MOUSEBUTTONUP

        js_to_pygame_bt_mapping = {
            0: 1,
            2: 3
        }
        mpos = cgmconf.conv_to_vscreen(clix, cliy)
        evmodule.gl_unique_manager.post(
            CgmEvent(adhoctype, pos=mpos, button=js_to_pygame_bt_mapping[js_bt_code])
        )

    @bind(cgmconf.browser_canvas, 'mouseout')
    def fwd_mouse_out(e):
        #window.console.log('mouseout')
        #window.console.log(e)
        evmodule.gl_unique_manager.post(
            CgmEvent(pygame_pym.constants.WINDOWLEAVE)
        )

    @bind(cgmconf.browser_canvas, 'mouseover')
    def fwd_mouse_in(e):
        #window.console.log('mousein')
        evmodule.gl_unique_manager.post(
            CgmEvent(pygame_pym.constants.WINDOWENTER)
        )

    @bind(cgmconf.browser_canvas, 'mousemove')
    def fwd_movement(e):
        mpos = cgmconf.conv_to_vscreen(e.clientX, e.clientY)
        evmodule.gl_unique_manager.post(
            CgmEvent(pygame_pym.constants.MOUSEMOTION, pos=mpos)
        )
        # x = e.clientX - rect.left;
        # y = e.clientY - rect.top;

    @bind(cgmconf.browser_canvas, "mousedown")
    def forwardCanvasMousedown(e):
        # window.console.log('mousDOWN ', e.button)
        handleclick(True, e.clientX, e.clientY, e.button)

    @bind(cgmconf.browser_canvas, "mouseup")
    def forwardCanvasMouseup(e):
        # window.console.log('mousup', e.button)
        handleclick(False, e.clientX, e.clientY, e.button)

    @bind(cgmconf.browser_canvas, "contextmenu")  # here to prevent the browser from opening a ctx menu
    def blockContextMenu(e):
        e.preventDefault()

    return temp_ref


class WebCtxGameTicker(GameTicker):
    # redef
    def proc_event(self, ev, source):
        pass

    # redef
    def loop(self, opt_junk=None):
        scr = cgmconf.get_screen()
        scr.context.clearRect(0, 0, scr.width, scr.height)

        self.pev(EngineEvTypes.LOGICUPDATE)
        self.pev(EngineEvTypes.PAINT)

        self._manager.update()
        gfx_updater.display_update()

        window.requestAnimationFrame(self.loop)
