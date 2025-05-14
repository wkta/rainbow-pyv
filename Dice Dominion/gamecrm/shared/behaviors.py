import random
from abc import abstractmethod

from coremon_main.events import PygameBridge, CgmEvent, EventReceiver, EventManager
from gamecrm.defs_mco import glvars as config
from gamecrm.defs_mco.ev_types import MyEvTypes


class BaseBehavior(EventReceiver):

    def __init__(self, t, data):
        super().__init__()
        self.type = t
        self._data = data
        self._player_id = data._player_id
        self._source = data

        # TODO déterminer utilité cette ligne-là:
        # self._data.unreg_all_events()
        # data.reg_event_func(eventtypes.NEWTURN, data.on_newturn)
        # self.set_active(True)

    # def set_active(self, bool_val):
    # super().set_active(bool_val)
    # self._data.set_active(bool_val)

    def proc_event(self, ev, source):

        if ev.type == MyEvTypes.TurnBegins:
            self.new_turn_hack(ev)

        if not self._data.active_player:
            return

        if ev.type == PygameBridge.MOUSEBUTTONDOWN:
            self.on_mouse_btn_down(ev)

        elif ev.type == PygameBridge.MOUSEBUTTONUP:
            self.on_mouse_btn_up(ev)

        elif ev.type == MyEvTypes.AttackResult:
            self.on_attack_result(ev)

        elif ev.type == MyEvTypes.GamestateChanges:
            self.on_gamestate_update(ev)

        # pour informer classes-fille evt capté
        # return True

    # - ancien bloc qui venait de Player...
    # register event functions
    # TODO: perhaps this should be done when entering
    #       Multigame or Singlegame
    # if ev.type == eventtypes.NEWTURN:
    #     self.on_newturn2(ev)

    # --------------- AJOUTS
    def new_turn_hack(self, event):
        temp_pid = event.curr_player

        if temp_pid == self._data.get_pid():
            print("====== joueur {} qui joue ======".format(temp_pid))
            # if self._implementation is None:
            #     self.revert_to_type(HUMAN)
            self._data.active_player = True
            self.on_newturn(event)
        else:
            self._data.active_player = False

    def on_mouse_btn_down(self, event):
        pass

    def on_mouse_btn_up(self, event):
        pass

    @abstractmethod
    def on_newturn(self, event):
        raise NotImplementedError

    def on_attack_result(self, event):
        pass

    def on_gamestate_update(self, vent):
        pass


class Human(BaseBehavior):

    def on_mouse_btn_down(self, event):
        if event.button == 1:
            pos = event.pos
            # TODO: hack!! need it really ref to world?
            land = config.world.get_land_from_abs(pos)
            if land:
                print('posting PlayerSelects playerid={} landid={}'.format(self._player_id, land.get_id()))
                ev = CgmEvent(MyEvTypes.PlayerSelects, playerid=self._player_id, landid=land.get_id())
                self._manager.post(ev)

        elif event.button == 3:  # right-click
            # TODO (as this isnt very good) we shall use a "next turn" button!!
            self._data.send_end_turn()

    def on_mouse_btn_up(self, event):
        pass

    # called by the arent (in proc_event)
    def on_newturn(self, ev):
        temp_pid = ev.curr_player
        ev = CgmEvent(MyEvTypes.PlayerPasses, old_pid=None, new_pid=temp_pid)
        self._manager.post(ev)


class AiPassive(BaseBehavior):

    def on_newturn(self, event):
        self._data.send_end_turn()


# TODO: correct implementation using selectresult!!
class AiDumb(AiPassive):

    def __init__(self, t, data):
        AiPassive.__init__(self, t, data)
        self.last_aggr = None
        self._manager = EventManager.instance()
        self.dead = False

    def on_newturn(self, event):
        ev_obj = CgmEvent(MyEvTypes.GamestateChanges, aggressorid=self.last_aggr)
        self.on_gamestate_update(ev_obj)

    def on_gamestate_update(self, event):
        if self.dead:
            return

        if self.last_aggr == event.aggressorid:
            lands = self._data.selectable_lands

            # +++ DEBUG +++
            # print("=====================dumb ai:")
            # for land, linked in lands.items():
            #     print(land.get_id(), [i.get_id() for i in linked])
            # print("---------------")

            if len(lands):
                count = 0
                tmp = list(lands.keys())
                land = random.choice(tmp)
                while land.num_dice < 2 and count < len(tmp) and land.get_id() != self.selection:
                    land = random.choice(tmp)
                    count += 1

                print("dumb ai, chosen land:", land.get_id())
                if land.num_dice < 2:
                    print("dumb ai: to less dices")
                    self._data.send_end_turn()
                defensor = random.choice(lands[land])
                print("defensor:", defensor.get_id())
                self.last_aggr = land.get_id()
                self._manager.post(
                    CgmEvent(MyEvTypes.PlayerSelects, playerid=self._player_id, landid=land.get_id())
                )
                self._manager.post(
                    CgmEvent(MyEvTypes.PlayerSelects, playerid=self._player_id, landid=defensor.get_id())
                )

            else:
                self._data.send_end_turn()


class Ai1(AiPassive):
    """

    """

    def __init__(self, t, data):
        print('construction Ai1 (*)')

        AiPassive.__init__(self, t, data)
        self.type = t
        self.num_qonquer = 0
        self._manager = EventManager.instance()
        self.dead = False

    def on_newturn(self, event):
        self.on_gamestate_update(event)

    def on_gamestate_update(self, event):
        if self.dead:
            return

        lands = self._data.selectable_lands

        if len(lands) > 0:
            get_num_dice = len(lands)
            num_dice = 0
            for land in lands:
                num_dice += land.num_dice
            max_dice = len(lands) * 8
            full = (max_dice <= num_dice)

            # print("full:", full, "<<<<<<<<<<<<<<<<<<<")

            if self.num_qonquer < 1:
                if full:
                    self.num_qonquer = get_num_dice / 8
                    tmp = list(lands.keys())
                    land = random.choice(tmp)
                    defensor = random.choice(lands[land])

                    self._manager.post(
                        CgmEvent(MyEvTypes.PlayerSelects, playerid=self._player_id, landid=land.get_id())
                    )
                    self._manager.post(
                        CgmEvent(MyEvTypes.PlayerSelects, playerid=self._player_id, landid=defensor.get_id())
                    )

                else:
                    self.num_qonquer = 0
                    self._data.send_end_turn()
            else:
                print("num_qonquer", self.num_qonquer)
                print("max_dice", max_dice)
                print("num_dice", num_dice)

                self.num_qonquer -= 1
                tmp = list(lands.keys())
                land = random.choice(tmp)
                defensor = random.choice(lands[land])

                self._manager.post(
                    CgmEvent(MyEvTypes.PlayerSelects, playerid=self._player_id, landid=land.get_id())
                )
                self._manager.post(
                    CgmEvent(MyEvTypes.PlayerSelects, playerid=self._player_id, landid=defensor.get_id())
                )

        else:
            self.num_qonquer = 0
            self._data.send_end_turn()
