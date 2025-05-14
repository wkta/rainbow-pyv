import json
import time

import gamecrm.defs_mco.glvars as glvars
from coremon_main.events import EventReceiver, EngineEvTypes, CgmEvent
from gamecrm.defs_mco.ev_types import MyEvTypes
from gamecrm.defs_mco.netw_codes import *


class NetwPusherCtrl(EventReceiver):
    """
    capte des évènements de jeu:
    - 'NumDiceChanges' qui contient land_id, num_dice
    - 'OwnerChanges' qui contient land_id, owner_pid
    - 'LocalPlayerPasses' qui contient active_pid ; identifiant du joueur courant

    convertit ceux-là en quadruplet
    (avec un n° de séquence)
    et les place dans un buffer...

    Lorsque buffer a plus de 0.2sec, on envoie sur le réseau

    /!\ sert à impacter le serveur (data client > server) uniquement /!\

    """
    BUFFER_DELAY = 0.2  # sec

    # codes pr communiquer sur le réseau
    T_NUM_DICE_CHANGES = -1
    T_OWNER_CHANGES = -2
    T_PLAYER_PASSES = -3

    def __init__(self, netw_history):
        super().__init__()

        self._netw_history = netw_history

        # date à laquelle le buffer reçoit 1+ éléments
        self._buffer_content = list()
        self._t_buffer_non_vide = None

        # - detection du local_pid
        tmp = None
        for pl_obj in glvars.players:
            if pl_obj.is_human():
                if tmp is not None:
                    raise ValueError('anomalie: 2+ humains jouent en local et NetwPusherCtrl est instancié')
                else:
                    tmp = pl_obj

        self._local_pid = tmp.get_pid()
        assert isinstance(self._local_pid, int)
        assert self._local_pid >= 0

    # ---
    #  GESTION EVT
    # --- ---
    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.LOGICUPDATE:
            if self._t_buffer_non_vide:
                self._on_update(ev)

        elif ev.type == MyEvTypes.LandValueChanges:
            if ev.pid == self._local_pid:
                print('MyEvTypes.NumDiceChanges pr joueur local')
                self._buffer_add(ev)

        elif ev.type == MyEvTypes.LandOwnerChanges:
            if ev.pid == self._local_pid:
                print('MyEvTypes.OwnerChanges pr joueur local')
                self._buffer_add(ev)

        elif ev.type == MyEvTypes.PlayerPasses:
            if ev.old_pid == self._local_pid:
                print('MyEvTypes.PlayerPasses')
                self._buffer_add(ev)

    def _on_update(self, ev):
        delta = ev.curr_t - self._t_buffer_non_vide
        if delta > self.BUFFER_DELAY:
            self._do_push_to_network()

    def _buffer_add(self, ev):
        # -- conv. evenement jeu en élément de buffer (forme de quadruplet)
        seq = self._netw_history.get_free_seq_nb()
        quad_form = [seq, None, None, None]

        if ev.type == MyEvTypes.LandValueChanges:
            quad_form[1] = self.T_NUM_DICE_CHANGES
            quad_form[2] = ev.land_id
            quad_form[3] = ev.num_dice

        elif ev.type == MyEvTypes.LandOwnerChanges:
            quad_form[1] = self.T_OWNER_CHANGES
            quad_form[2] = ev.land_id
            quad_form[3] = ev.owner_pid

        elif ev.type == MyEvTypes.PlayerPasses:
            quad_form[1] = self.T_PLAYER_PASSES
            quad_form[2] = ev.old_pid
            quad_form[3] = ev.new_pid

        # history local reste à jour
        elt = list(quad_form)
        self._netw_history.add(elt)

        # envoi réseau imminent...
        self._buffer_content.append(elt)
        if self._t_buffer_non_vide is None:
            self._t_buffer_non_vide = time.time()

    # ---
    #  MÉTIER
    # --- ---
    def _do_push_to_network(self):
        """
        push all buffer content to the network
        :return: None
        """

        res = ''
        for elt in self._buffer_content:
            res += json.dumps(elt) + "@"
        ev = CgmEvent(EngineEvTypes.ASYNCSEND, num=NETW_PUSH_LAND_ST, msg='tom/push_lands.php',
                      data=res)
        self._manager.post(ev)

        #if self.switching_to_listen_mode:
        #    self.ask_sync_from_netw()
        self._reset_buffer()

    def _reset_buffer(self):
        del self._buffer_content[:]
        self._t_buffer_non_vide = None
