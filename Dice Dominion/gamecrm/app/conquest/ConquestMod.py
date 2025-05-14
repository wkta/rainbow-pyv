import coremon_main.engine as coremon
from gamecrm.app.conquest.gamestate import GameState
import gamecrm.defs_mco.glvars as glvars
from gamecrm.defs_mco.ev_types import MyEvTypes
from coremon_main.events import CgmEvent, EventManager
from gamecrm.model.GlobOwnershipLands import GlobOwnershipLands


class ConquestMod:
    """
    contient les données de la partie courante,
    gère la logique de jeu hors évènements
    """

    def __init__(self):
        self.gamestate = GameState(len(glvars.players))
        self.selection = None  # ??

    def get_current_player(self):
        return self.gamestate.current_player

    def whos_playing(self):
        return self.gamestate.current_player

    def get_local_pid(self):
        res = glvars.local_pid
        assert isinstance(res, int)
        assert res >= 0
        return res

    def increm_turn(self, pid):
        self.gamestate.increm_turn(pid)

    def get_turn(self):
        return self.gamestate.get_turn()
