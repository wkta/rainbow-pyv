import random
import time

import glvars
# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi

from app.main_screen.AvatarView import AvatarView
from app.main_screen.ButtonsMainV import ButtonsMainV
from app.main_screen.LackeySetV import LackeySetV
from app.main_screen.MissionSetView import MissionSetView
from app.main_screen.models import Avatar
from app.main_screen.models_mission import MissionSetModel
from game_defs import GameStates
from game_events import MyEvTypes


EngineEvTypes = kengi.event.EngineEvTypes
EventReceiver = kengi.event.EventReceiver
pygame = kengi.pygame


class ChallSelectionCtrl(EventReceiver):

    MISSION_DELAY = 2.0

    def __init__(self, mod):
        super().__init__()
        self._modele = mod
        self._timers = dict()

    def proc_event(self, ev, source=None):
        if ev.type == EngineEvTypes.LOGICUPDATE:
            if len(self._timers) > 0:
                defunct_set = set()
                for mission_idx, v in self._timers.items():
                    dt = time.time() - v
                    if dt > ChallSelectionCtrl.MISSION_DELAY:
                        defunct_set.add(mission_idx)

                for targ_idx in defunct_set:
                    del self._timers[targ_idx]
                    self._modele.flag_mission_done(targ_idx)

        elif ev.type == MyEvTypes.FightStarts:
            self.pev(EngineEvTypes.PUSHSTATE, state_ident=GameStates.Fighting)

        elif ev.type == MyEvTypes.MissionStarts:
            self._timers[ev.idx] = ev.t


class MainScreenState(kengi.BaseGameState):
    def __init__(self, gs_id):
        super().__init__(gs_id)
        self.m = self.c = None
        self.vmission = self.vgui = None
        self.vavatar = None
        self._avatar = None
        self._all_recv = None
        self.vlackeys = None

    def enter(self):
        if self._avatar:
            pass
        else:
            self._avatar = Avatar('AmumuTester', 0, random.randint(11, 37))  # random gold pieces aka GP
            self._avatar.add_xp(random.randint(872, 13125))

            glvars.the_avatar = self._avatar  # shared with other game states
        self.m = MissionSetModel()
        self.vmission = MissionSetView(self.m)
        self.vgui = ButtonsMainV(self._avatar)
        self.vavatar = AvatarView(self._avatar)
        self.vlackeys = LackeySetV(self._avatar)

        self.c = ChallSelectionCtrl(self.m)

        self._all_recv = [
            self.vmission, self.vgui, self.vavatar, self.vlackeys, self.c
        ]

        print(' MainMenuState ENTER')
        for r in self._all_recv:
            r.turn_on()

    def resume(self):
        self.vavatar.refresh_disp()
        self.vlackeys.refresh_infos()
        
        self.vgui.update_labels()
        for r in self._all_recv:
            r.turn_on()
        print(' MainMenuState RESUME')

    def release(self):
        tmp = list(self._all_recv)
        tmp.reverse()
        for r in tmp:
            r.turn_off()
        print(' MainMenuState RELEASE')

    def pause(self):
        tmp = list(self._all_recv)
        tmp.reverse()
        for r in tmp:
            r.turn_off()
        print(' MainMenuState PAUSE')
