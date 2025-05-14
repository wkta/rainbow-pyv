from gamecrm.app.menu_solo.ctrl import MenuSoloCtrl
from gamecrm.app.menu_solo.model import MenuOptionsMod
from gamecrm.app.menu_solo.view import MenuOptionsView
from coremon_main.events import EventManager
from coremon_main.structures import BaseGameState


##class MenuSoloState(BaseGameState):
##    def __init__(self, gs_id, name):
##        super().__init__(gs_id, name)
##        self.c = None
##
##    def enter(self):
##        self.c = MenuSoloCtrl()
##        self.c.set_active(True)
##
##    def release(self):
##        EventManager.instance().soft_reset()
##
##    def resume(self):
##        self.c.rand_lands()
##        self.c.setup_map()
##        self.c.set_active(True)
##
##    def pause(self):
##        EventManager.instance().soft_reset()
##        self.c.set_active(False)


class MenuSoloState(BaseGameState):

    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)

        self.m = self.v = self.c2 = None

    def enter(self):
        self.m = MenuOptionsMod()
        self.v = MenuOptionsView(self.m)
        self.c2 = MenuSoloCtrl(self.m)
        self.resume()

    def resume(self):
        self.v.turn_on()
        self.c2.turn_on()

    def pause(self):
        EventManager.instance().soft_reset()

    def release(self):
        EventManager.instance().soft_reset()
        self.m = self.v = self.c2 = None
