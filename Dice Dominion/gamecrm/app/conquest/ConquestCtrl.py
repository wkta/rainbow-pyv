import random

import gamecrm.defs_mco.glvars as glvars
from coremon_main.events import EventReceiver, EventManager, CgmEvent, EngineEvTypes, PygameBridge
from gamecrm.app.conquest.ConquestMod import ConquestMod
from gamecrm.defs_mco.ev_types import MyEvTypes
from gamecrm.model.GlobOwnershipLands import GlobOwnershipLands
from gamecrm.shared.PlayerBehaviorFactory import PlayerBehaviorFactory
from gamecrm.shared.PlayerMod import PlayerMod


# - legacy -
def post_select_result(source, land_id, result):
    """
    landid  : id of the land which was selected
    ressult : 0=select, 1=deselect
    """
    EventManager.instance().post(
        CgmEvent(MyEvTypes.SelectResult, source=source, landid=land_id, result=result)
    )


def post_player_win(source, player_id):
    # playerid: id of the player which is dead
    EventManager.instance().post(
        CgmEvent(MyEvTypes.PlayerWins, source=source, playerid=player_id)
    )


def post_player_dead(source, player_id):
    # playerid: id of the player which is dead
    EventManager.instance().post(
        CgmEvent(MyEvTypes.PlayerDies, source=source, playerid=player_id)
    )


def post_attack_result(source, aggresor_id, defensor_id, results):
    """
    aggressorid : land id which is attacking
    defensorid  : land id which is defensing
    results     : result of the attack -> ((dice pips, sum),(dice pips, sum))
    """
    EventManager.instance().post(
        CgmEvent(MyEvTypes.AttackResult, source=source, aggressorid=aggresor_id, defensorid=defensor_id, results=results)
    )


class ConquestCtrl(EventReceiver):
    def __init__(self, ref_mod: ConquestMod):
        super().__init__()

        self._ref_mod = ref_mod
        self.state = ref_mod.gamestate
        self._own_infos = GlobOwnershipLands.instance()

        self.li_pl_ctrl = list()

    # ---
    #  GESTION EV.
    # --- ---
    def proc_event(self, ev, source):
        if ev.type == PygameBridge.KEYDOWN and ev.key == PygameBridge.K_ESCAPE:
            self._manager.post(CgmEvent(EngineEvTypes.POPSTATE))

        else:
            assoc_evtype_meth = {
                MyEvTypes.ConquestGameStart: self.on_startgame,  # anciennement STARTGAME
                MyEvTypes.TurnEnds: self.on_endturn,  # anciennement ENDTURN
                MyEvTypes.TurnBegins: self._on_newturn,  # anciennement NEWTURN
                MyEvTypes.PlayerSelects: self.on_select,
                MyEvTypes.DropDice: self.on_drop_dice,
            }
            if ev.type in assoc_evtype_meth:
                meth = assoc_evtype_meth[ev.type]
                meth(ev)

    def _on_newturn(self, event):
        temp_pid = event.curr_player
        assert isinstance(temp_pid, int)
        assert temp_pid >= 0

        self._ref_mod.increm_turn(temp_pid)

    def on_endturn(self, event):
        if self.state.state != 1:
            print("ERROR: game is not in playing.")
            return

        tmp = PlayerMod.retrieve_by_pid(event.playerid)
        if not tmp.is_remote():
            after_lands = self.__effets_fin_tour()
        else:
            after_lands = {}

        # meme si pas de dés ajoutés => on force refresh graphique là aussi (effets de bord)
        self._manager.post(
            CgmEvent(MyEvTypes.DropDice, data=after_lands)
        )

        # TODO respecte un peu l'encapsulation, boy!
        # remove selection
        if self._ref_mod.selection:
            self._ref_mod.selection.selected = False
            self._ref_mod.selection = None

    def on_drop_dice(self, event):
        old_idx = self.state.current_player
        nb_players = len(glvars.players)

        candidate_idx = (old_idx + 1) % nb_players
        while not self.state.test_can_play_by_pid(candidate_idx):
            candidate_idx = (candidate_idx + 1) % nb_players

        # notify player change
        self.pev(MyEvTypes.PlayerPasses, old_pid=old_idx, new_pid=candidate_idx)
        self.pev(MyEvTypes.TurnBegins, curr_player=candidate_idx)

    def on_select(self, event):
        # print('event .PlayerSelects recu par ConquestCtrl')
        if self.state.current_player != event.playerid:  # PlayerMod.retrieve_by_pid(event.playerid):
            return

        land = self.state.get_land_by_id(event.landid)
        # first select?
        if self._ref_mod.selection is None:
            # is it cur_palyer land?
            if self._own_infos[land.get_id()] != self.state.current_player:
                print("land does not belong to current player.")
                post_select_result(self, land.get_id(), 2)  # not possible
                return False
            # has it more than 1 dice
            if land.num_dice < 2:
                print("land has only 1 dice!.")
                post_select_result(self, land.get_id(), 2)  # not possible
                return False
            # has it adj lands to attack?
            pot_defensors = []
            for lnk in land.get_linked_lands():
                if self._own_infos[lnk.get_id()] != self.state.current_player:
                    pot_defensors.append(lnk)

            if len(pot_defensors) == 0:
                print("land has no adj land to attack.")
                post_select_result(self, land.get_id(), 2)  # not possible
                return False
            # -> SELECTRESULT

            self._ref_mod.selection = land
            land.selected = True
            # useless
            # post_select_result(self, event.landid, 0)  # ok

        else:
            # second select
            # belongs it to same player?
            if self._own_infos[land.get_id()] == self.state.current_player:
                # same as selection? -> deselect -> SELECTRESULT
                if self._ref_mod.selection == land:
                    self._ref_mod.selection.selected = False
                    self._ref_mod.selection = None
                    # post_select_result(self, event.landid, 1)  # deselect
                    return False
                else:
                    print("Cant select two land of same player, selection:", self._ref_mod.selection.get_id(), "land:",
                          land.get_id())
                    post_select_result(self, land.get_id(), 2)  # not possible
                    return False
            # is it adj to first selection?
            if land not in self._ref_mod.selection.get_linked_lands():
                print("land is not adj to the selection, selection:", self._ref_mod.selection.get_id(), "not adj", land.get_id())
                post_select_result(self, land.get_id(), 2)  # not possible
                return False

            # perform attack
            self.attack(self._ref_mod.selection, land)
            # -> SELECTRESULT

            # deselect all!
            land.selected = False
            self._ref_mod.selection.selected = False
            self._ref_mod.selection = None
            # post_select_result(self, event.landid, 1)
            # post_select_result(self, self._ref_mod.selection.get_id(), 1)


    def on_startgame(self, event):
        # init. nombre de dés par DiceLand

        for land in glvars.world.get_lands():
            # -- TOM DEBUG --
            # previously:
            # land.set_num_dice(1)
            # now:
            res = land.set_num_dice(random.randint(2, 8))
            pid_now = self._ref_mod.whos_playing()
            ev = CgmEvent(MyEvTypes.LandValueChanges, pid=pid_now, land_id=land.get_id(), num_dice=res)
            self._manager.post(ev)

        for player in glvars.players:
            player.dead = False

        # post_new_turn(self, self.state.players[0].get_pid())
        self.pev(MyEvTypes.TurnBegins, curr_player=self._ref_mod.get_current_player())

    def on_connectioninterrupt(self, event):
        """

        """
        pass

        ##    def on_event(self, event):
        ##        print "gamelogic:"
        ##        print event
        ##        return False

        # ---methods---##ffff00

    def attack(self, aggressor, defensor):
        """

        """
        # roll dice
        aggr_pips, aggr_sum = aggressor.roll_dice()
        def_pips, def_sum = defensor.roll_dice()

        # -> RESULT
        post_attack_result(
            self, aggressor.get_id(), defensor.get_id(), ((aggr_pips, aggr_sum), (def_pips, def_sum))
        )

        print(aggressor.get_id(), "attacked", defensor.get_id(), " result:", aggr_sum, ":", def_sum, "    ", aggr_pips,
              ":", def_pips)

        if aggr_sum <= def_sum:  # aggressor looses
            return

        # or wins!
        # check if opponent has died
        loser_pid = self._own_infos[defensor.get_id()]
        if self._own_infos.calc_score(loser_pid) == 1:
            # if len(defensor.get_player().owned_lands) == 1:

            print("gamelogic: player", loser_pid, "is dead")
            post_player_dead(self, loser_pid)

            # check if player is victorious
            winner_pid = self._own_infos[aggressor.get_id()]
            if self._own_infos.calc_score(winner_pid) == self._own_infos.total - 1:

                # if len(self.state.get_alive_players()) == 2:
                print("gamelogic: player", winner_pid, "wins")
                post_player_win(self, winner_pid)

                print("gamelogic: post end game!")
                self._manager.post(
                    CgmEvent(MyEvTypes.GameEnds)
                )

    def __effets_fin_tour(self):
        """
        format retour: {
            land_id_1: int,
            land_id_2: int,
            ...
        }
        """
        result = dict()
        curr_pid = self.state.current_player
        nb_bonus_dices = GlobOwnershipLands.instance().calc_score(curr_pid)
        print('bonus dices exp= {}'.format(nb_bonus_dices))

        select_queue = PlayerMod.retrieve_by_pid(curr_pid).owned_lands

        # need to filter out candidates that have 8+ dices
        non_eligible_lands = set()
        for refland in select_queue:
            if refland.num_dice >= 8:
                non_eligible_lands.add(refland)

        for elt in non_eligible_lands:
            select_queue.remove(elt)

        # sprinkle bonus dices, until its gone
        while nb_bonus_dices > 0 and len(select_queue) > 0:
            # choix alea
            pick = random.randint(0, len(select_queue) - 1)
            refland = select_queue[pick]
            lid = refland.get_id()

            # ajout dice et update candidats
            if lid not in result:
                result[lid] = refland.num_dice
            result[lid] += 1
            if result[lid] == 8:
                select_queue.remove(refland)
            # keep track how many bonus dice are left
            nb_bonus_dices -= 1

        return result

    # --- ---
    #  REDÉFINITIONS
    # ---
    def turn_on(self):
        for player_obj in glvars.players:
            t = player_obj.get_player_type()
            print(str(t))

            ctrl_adhoc = PlayerBehaviorFactory.build(t, player_obj)
            self.li_pl_ctrl.append(ctrl_adhoc)
            ctrl_adhoc.turn_on()

        super().turn_on()

    def turn_off(self):
        for e in self.li_pl_ctrl:
            e.turn_off()
        del self.li_pl_ctrl[:]

        super().turn_off()
