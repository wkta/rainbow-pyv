import gamecrm.defs_mco.glvars as glvars
from coremon_main.events import CgmEvent, EventManager
from gamecrm.defs_mco.ev_types import MyEvTypes
from gamecrm.model.GlobOwnershipLands import GlobOwnershipLands
from gamecrm.shared.PlayerBehaviorFactory import PlayerBehaviorFactory


class PlayerMod:
    """
    Player of the game. It will hold some information about the player like 
    which lands he posses.
    """

    _indexed_players = dict()

    @classmethod
    def retrieve_by_pid(cls, pid_value):
        return PlayerMod._indexed_players[pid_value]

    def is_human(self):
        return self._player_type == PlayerBehaviorFactory.HUMAN

    def is_remote(self):
        return self._player_type == PlayerBehaviorFactory.NETWORK

    def __init__(self, pid, player_type=PlayerBehaviorFactory.HUMAN):
        self._manager = EventManager.instance()
        self._own_infos = GlobOwnershipLands.instance()

        self._player_id = pid
        self._player_type = player_type

        self.dead = False
        self.active_player = False

        PlayerMod._indexed_players[pid] = self

    # --- ---
    #  MÉTHODES MÉTIER
    # ---
    def get_pid(self):
        """
        Returns the id of the player.
        """
        return self._player_id

    def get_player_type(self):
        return self._player_type

    def set_player_type(self, val):
        assert val in PlayerBehaviorFactory.VALID_TYPES
        print('settin player type <- {}'.format(val))
        self._player_type = val

    @property
    def owned_lands(self):
        own = GlobOwnershipLands.instance()
        myland_ids = own.list_land_ids(self._player_id)
        res = list()
        for lan in glvars.world.get_lands():
            if lan.get_id() in myland_ids:
                res.append(lan)
        return res

    # REQUIRED, for example: the class Human(BaseBehavior) calls this...
    def send_end_turn(self):
        self.active_player = False
        self._manager.post(
            CgmEvent(MyEvTypes.TurnEnds, playerid=self._player_id)
        )
    # def remove_land(self, land):
    #     """
    #     Removes the land from this player.
    #     """
    #     if land in self._lands:
    #         self._lands.remove(land)
    #         land.set_player(None)

    # def get_lands(self):
    #     """
    #     Returns a list of all lands owned by this player.
    #     """
    #     # TODO: remove this dirty fix...
    #     # on retire de lands les lands avec 0 dés dessus
    #     tmp_l = list()
    #     for land in self._lands:
    #         if land.num_dice > 0:
    #             tmp_l.append(land)
    #     return tmp_l

    @property
    def selectable_lands(self):
        """
        format retourné:
        {
            aggresor_a: [defensor1a, defensor2a, ...],
            aggresor_b: [defensor1b, defensor2b, ...],
            ...
        }
        """

        info_selectable_lands = dict()

        for refland in self.owned_lands:
            if refland.num_dice < 2:
                continue

            for neighbor in refland.get_linked_lands():
                if self._own_infos[neighbor.get_id()] == self._player_id:
                    continue
                # neighbor est voisin de refland, possédé par qqun dautre
                if refland not in info_selectable_lands:
                    info_selectable_lands[refland] = list()

                info_selectable_lands[refland].append(neighbor)

        return info_selectable_lands
