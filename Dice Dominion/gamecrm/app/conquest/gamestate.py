import gamecrm.defs_mco.glvars as glvars
from coremon_main.events import EventReceiver, CgmEvent
from gamecrm.defs_mco.ev_types import MyEvTypes
from gamecrm.model.GlobOwnershipLands import GlobOwnershipLands
from gamecrm.shared.PlayerMod import PlayerMod


class GameState(EventReceiver):

    NOT_STARTED, PLAYIN, ENDED = range(3)

    def __init__(self, nbplayers):
        super().__init__()

        self._own_infos = GlobOwnershipLands.instance()
        self._nb_players = nbplayers
        self._curr_pid = 0  # PlayerMod.retrieve_by_pid(0)  # par convention cest le pl 0 qui démarre

        self.state = GameState.NOT_STARTED
        self._numero_tour = 0

        # register it directly to source
        # events.RootEventSource.instance().add_listener(self, prio=1)
        self.turn_on()

    @property
    def current_player(self):
        return self._curr_pid

    def proc_event(self, ev, source):
        adhoc_method = {
            # eventtypes.NEWTURN: self.on_newturn,
            MyEvTypes.PlayerDies: self.on_playerdead,
            MyEvTypes.PlayerWins: self.on_playerwin,

            MyEvTypes.ConquestGameStart: self.on_startgame,  # anciennement STARTGAME

            MyEvTypes.AttackResult: self.on_attackresult,

            MyEvTypes.GameEnds: self.on_endgame,
            MyEvTypes.DropDice: self.on_dropdice,

            # ol_eventtypes.CONNINTERRUPT: self.on_connectioninterrupt,
            # ol_eventtypes.PLAYERRECONN: self.on_playerreconnect
        }

        if ev.type in adhoc_method:
            meth = adhoc_method[ev.type]
            meth(ev)


#---eventfuncions----##FFff00
    def on_attackresult(self, event):
        """
        
        """
        aggr_pips, def_pips = event.results
        def_pips, def_sum   = def_pips
        aggr_pips, aggr_sum = aggr_pips
        aggr_land = self.get_land_by_id(event.aggressorid)
        def_land  = self.get_land_by_id(event.defensorid)
        attacker_pid = self._own_infos[event.aggressorid]

        if aggr_sum > def_sum:  # aggressor wins
            # move num_dices-1 into conquered land
            target_amount = aggr_land.num_dice-1
            def_land.set_num_dice(target_amount)

            # - notify
            ev = CgmEvent(MyEvTypes.LandValueChanges, pid=self._curr_pid, land_id=event.defensorid, num_dice=target_amount)
            self._manager.post(ev)

            # add conquered land to the winner player
            self._own_infos.transfer(event.defensorid, attacker_pid)
            ev = CgmEvent(MyEvTypes.LandOwnerChanges, pid=self._curr_pid, land_id=event.defensorid, owner_pid=attacker_pid)
            self._manager.post(ev)

        # only one dice remains in land
        aggr_land.set_num_dice()

        # - notify
        self._manager.post(
            CgmEvent(MyEvTypes.LandValueChanges, pid=self.current_player, land_id=event.aggressorid, num_dice=1)
        )
        self._manager.post(
            CgmEvent(MyEvTypes.GamestateChanges, source=self, aggressorid=event.aggressorid,
                     defensorid=event.defensorid)
        )

##    def on_endturn(self, event):
##        """
##        
##        """
##        self.current_player = None

    def increm_turn(self, pid):
        self._numero_tour += 1
        self._curr_pid = pid  #PlayerMod.retrieve_by_pid(pid)
        print('tour de jeu n°{}'.format(self._numero_tour))
        print('le joueur # {} joue '.format(pid))

    def get_turn(self):
        return self._numero_tour

    def on_playerdead(self, event):
        player = PlayerMod.retrieve_by_pid(event.playerid)
        player.dead = True
        print("[gamestate: pl.", str(event.playerid), "died]")
        
    def on_playerwin(self, event):
        # TODO: implement: what to do?
        print("[gamestate: pl." + str(event.playerid) + " won]")
        
    def on_startgame(self, event):
        self.state = GameState.PLAYIN
        print("[gamestate: game has started...]")
        
    def on_endgame(self, event):
        self.state = GameState.ENDED
        for land in glvars.world.get_lands():
            land.selected = False
        print("[gamestate: game ended]")

    def on_dropdice(self, event):
        # mise à jour des régions suite à des placements de dés aléatoires
        if len(event.data) == 0:
            return

        for land_id, num_dice in event.data.items():
            land = self.get_land_by_id(land_id)
            land.set_num_dice(num_dice)

            # - notify
            ev = CgmEvent(MyEvTypes.LandValueChanges, pid=self.current_player, land_id=land_id, num_dice=num_dice)
            self._manager.post(ev)

            # -- deprec CASE:
            # -- land by id gives None
            # else:
            #     # TODO: ?
            #     print( "WARNING: no land foun to drop dice, land id:", land_id)
        
    def on_connectioninterrupt(self, event):
        pass
        
    def on_playerreconnect(self, event):
        pass

    # - other methods #ffff00
    def get_land_by_id(self, land_id):
        return glvars.world.get_land_by_id(land_id)

    def test_can_play_by_pid(self, pid):
        return not PlayerMod.retrieve_by_pid(pid).dead

    # def get_alive_players(self):
    #     alive = []
    #     for player in glvars.players:
    #         if not player.dead:
    #             alive.append(player)
    #     return alive
    
    def update(self):
        for player in glvars.players:
            player.update()
