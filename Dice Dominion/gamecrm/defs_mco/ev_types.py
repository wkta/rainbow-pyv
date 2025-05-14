from coremon_main.events import CgmEvent
from coremon_main.defs import enum_for_custom_event_types


MyEvTypes = enum_for_custom_event_types(

    'PlayerDies',
    'PlayerWins',

    # 'AddDices',

    'ConquestGameStart',
    'ConquestGameOver',

    'LandValueChanges',  # contient: pid, land_id, num_dice
    'LandOwnerChanges',  # exemple >>>_pid=self._curr_pid, land_id=..., owner_pid=attacker_pid  (qui remporte land)

    # NEWTURN      = __game  # playerid
    'TurnBegins',
    # ENDTURN      = __game+1  # playerid
    'TurnEnds',

    # SELECT       = __game+2  # playerid, landid
    'PlayerSelects',
    # SELECTRESULT = __game+3  # landid, result 0=ok, 1=deselect, 2=notpossible (ai)
    'SelectResult',
    # GSUPDATE     = __game+4  # None
    'GamestateChanges',  # contains: source, aggressorid, defensorid
    # ATTACKRESULT = __game+5  # aggressorid, defensorid, results
    'AttackResult',

    # # PLAYERDISCONN= __game+6  # playerid
    # PLAYERDEAD   = __game+7  # playerid
    # PLAYERWIN    = __game+8  # playerid
    # DROPDICE     = __game+9  # data ={land_id:num_dice}
    'DropDice',
    # STARTGAME    = __game+10  # None
    # ENDGAME      = __game+11  # playerid of winner
    'GameEnds',
    # PLAYERRECONN = __game+12  # playerid


    'MapChanges',
    #'NewTurn',
    #'MatchBegins',

    # --

    #'PlayerDies',
    #'NewTurn',

    'RemotePlayerPasses',  # grâce à ça, le ctrl réseau peut forcer ctrl RemotePlayer à rendre la main normalement

    'PlayerPasses',  # contient [old_pid, new_pid]
    'ForceEcoute',

    # -- réseau
    'RequestMap'
)
CgmEvent.inject_custom_names(MyEvTypes)  # pour avoir les noms affichés par CgmEvent.__str__
