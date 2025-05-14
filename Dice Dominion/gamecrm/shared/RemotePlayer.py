import json
import gamecrm.defs_mco.glvars as glvars
from coremon_main.events import CgmEvent, EngineEvTypes
from gamecrm.app.conquest.NetwPusherCtrl import NetwPusherCtrl
from gamecrm.model.GlobOwnershipLands import GlobOwnershipLands
from gamecrm.shared.behaviors import BaseBehavior
from gamecrm.defs_mco.ev_types import  MyEvTypes
from gamecrm.defs_mco.netw_codes import *


class RemotePlayer(BaseBehavior):
    """
    a BasePlayer that uses the network (remote player playing)
    """
    def __init__(self, t, data, netw_history):
        super().__init__(t, data)
        self._timestamp = None
        self._netw_history = netw_history

    def _on_recv(self, ev):
        if ev.num == NETW_ASK_LAND_ST:
            print('*** _on_recv dans RemotePlayer ***')
            obj = json.loads(ev.msg)
            stream = obj['data_from_file']
            self._timestamp = obj['timestamp']

            # - we process stream to keep only new stuff i.e. actions that were unknown so far
            li_tmp = stream.split('@')
            li_tmp.pop()
            full_history = list()
            for elt in li_tmp:
                full_history.append(json.loads(elt))

            new_chunk = self._netw_history.update(full_history)

            # lets apply all actions described by new_chunk
            # i.e.  execute received actions on this LOCAL client...
            if new_chunk:
                for elt in new_chunk:
                    tag = elt[1]
                    if tag == NetwPusherCtrl.T_NUM_DICE_CHANGES:
                        land_id, num_dice = elt[2], elt[3]
                        land_obj = glvars.world.get_land_by_id(land_id)
                        land_obj.set_num_dice(num_dice)

                        # None indique que cetait injecté, pas joué par un joueur en particulier
                        # self._manager.post(
                        #     CgmEvent(MyEvTypes.LandValueChanges, pid=None, land_id=land_obj.get_id(), num_dice=res)
                        # )

                    elif tag == NetwPusherCtrl.T_OWNER_CHANGES:
                        land_id, owner_pid = elt[2], elt[3]
                        GlobOwnershipLands.instance().transfer(land_id, owner_pid)
                        self._manager.post(
                            CgmEvent(MyEvTypes.LandValueChanges, pid=owner_pid, land_id=land_id, num_dice=None)
                        )

                    elif tag == NetwPusherCtrl.T_PLAYER_PASSES:
                        # le tag 'passes' provoque un post event type MyEvTypes.RemotePlayerPasses
                        print('Remote sait que la main passe de {} a {}'.format(elt[2], elt[3]))
                        self.passe_la_main()
                        return

            self.ask_sync_from_netw()  # loop, if

    def ask_sync_from_netw(self):
        # self.listen_mode = True
        # self.switching_to_listen_mode = False

        # asking for the current network state...
        ressource = 'tom/get_lands.php?timestamp={}'.format(self._timestamp)
        ev = CgmEvent(EngineEvTypes.ASYNCSEND, num=NETW_ASK_LAND_ST, msg=ressource, data=None)
        self._manager.post(ev)

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.ASYNCRECV:
            self._on_recv(ev)
        #elif ev.type == NEWTURN:
        elif ev.type == MyEvTypes.TurnBegins:
            print(str(ev))
            if ev.curr_player == self._data.get_pid():
                self.on_newturn(ev)

        # ----
        # tmp = super().proc_event(ev, source)
        # if tmp:
        #     return
        #
        # if ev.type == MyEvTypes.RemotePlayerPasses:
        #     self.passe_la_main()
        # --------

        #if ev.type == eventtypes.NEWTURN:
        #        self.on_newturn_moi(ev)

        #elif ev.type == EngineEvTypes.ASYNCRECV:
        #  self._traite_reception(ev)

    def passe_la_main(self):
        self._data.send_end_turn()

    def on_newturn(self, event):
        print('un remote prend la main')
        self._timestamp = None
        self.ask_sync_from_netw()
        #ev = CgmEvent(MyEvTypes.ForceEcoute)
        #self._manager.post(ev)

    def _traite_reception(self, ev):
        print('-je traite !!! -')
        print(str(ev))

        # - on passe son tour, sans rien faire !
        self._data.send_end_turn()

    def _do_test_network(self):  # suite à la pression bouton
        ressource = 'tom/async_test_server.php?timestamp=none'
        t = EngineEvTypes.ASYNCSEND
        new_ev = CgmEvent(t, num=999, msg=ressource)  # , cb=self.junk_cb_func)
        self._manager.post(new_ev)
