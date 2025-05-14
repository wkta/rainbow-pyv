import gamecrm.defs_mco.glvars as glvars
from coremon_main.events import EventManager, CgmEvent
from coremon_main.structures import BaseGameState
from gamecrm.app.conquest.ConquestCtrl import ConquestCtrl
from gamecrm.app.conquest.ConquestMod import ConquestMod
from gamecrm.app.conquest.NetwPusherCtrl import NetwPusherCtrl
from gamecrm.app.conquest.ConquestView import ConquestView
from gamecrm.defs_mco.ev_types import MyEvTypes
from gamecrm.shared.PlayerBehaviorFactory import PlayerBehaviorFactory


class ConquestState(BaseGameState):
    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)

        self.m = None
        self.conquest_gfx = None
        self.c = None
        self.nework_push_ctrl = None

    def enter(self):
        self.m = ConquestMod()
        glvars.gl_conquest_mod = self.m  # permettra dinjecter données depuis réseau

        self.conquest_gfx = ConquestView(self.m)
        self.conquest_gfx.turn_on()

        self.c = ConquestCtrl(self.m)

        glvars.multiplayer_mode = False
        for ref_player in glvars.players:

            if ref_player.is_remote():
                glvars.multiplayer_mode = True
                self.nework_push_ctrl = NetwPusherCtrl(PlayerBehaviorFactory.netw_history)
                self.nework_push_ctrl.turn_on()
                break

        self.c.turn_on()

        # send an event that acts like a signal to say the conquest game begins
        EventManager.instance().post(CgmEvent(MyEvTypes.ConquestGameStart))

    def release(self):
        EventManager.instance().soft_reset()

        self.m = glvars.gl_conquest_mod = None
        self.conquest_gfx = None
        self.c = None
        self.nework_push_ctrl = None
