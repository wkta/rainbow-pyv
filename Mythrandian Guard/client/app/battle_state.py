import time
import game_defs
# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi

import app.battle.DebugAnimV as debuganim

# aliases
from app.battle.BattleV import BattleV
from app.battle.DebugBattleV import DebugBattleV
from app.battle.bmodel import Battle

ButtonPanel, Button = kengi.gui.ButtonPanel, kengi.gui.Button
pygame = kengi.pygame
EventReceiver = kengi.event.EventReceiver
EngineEvTypes = kengi.event.EngineEvTypes

OLDTESTS = False  # deprecated (set to True if running DebugAnimV tests)


class BattleIteratorCtrl(EventReceiver):

    def __init__(self, refbattle):
        super().__init__()
        self.turn = 0
        self._bmod = refbattle

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.BTCLICK:
            print(ev)
        elif ev.type == pygame.QUIT:
            self.pev(EngineEvTypes.POPSTATE)
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            self.pev(EngineEvTypes.POPSTATE)
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                if not self._bmod.is_over():
                    self._bmod.increm_fight(self.turn)
                    if self._bmod.is_over():
                        print('battle has ended at turn {} !!!'.format(self.turn))
                    else:
                        self.turn += 1


class CustomListener(EventReceiver):
    """
    old listener for keyb
    """
    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.BTCLICK:
            print(ev)
        elif ev.type == pygame.QUIT:
            self.pev(EngineEvTypes.POPSTATE)
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            self.pev(EngineEvTypes.POPSTATE)
        elif ev.type == pygame.KEYDOWN:
            if OLDTESTS:
                if ev.key == pygame.K_SPACE:
                    debuganim.anim_attack()
                elif ev.key == pygame.K_RETURN:
                    debuganim.anim_defend()
                elif ev.key == pygame.K_BACKSPACE:
                    debuganim.anim_hit()
            else:
                print('key strokes cb not implemented for recent tests...')


class BattleState(kengi.BaseGameState):
    def __init__(self, gs_id):
        super().__init__(gs_id)
        self.m = self.v = self.c = None

    def enter(self):
        print('entree - MenuAventuresState')

        # old tests(play animations)
        # >you can plug it back if needed<
        # self.v = debuganim.DebugAnimV()

        # recent tests (march22), two lines of code
        b = Battle.sample_example()
        self.v = BattleV(b)

        # -- end of tests --
        self.v.turn_on()

        # old:
        # self.c = CustomListener()
        # new:
        self.c = BattleIteratorCtrl(b)
        self.c.turn_on()

    def release(self):
        print('sortie - MenuAventuresState')
        self.v.turn_off()
        self.c.turn_off()
