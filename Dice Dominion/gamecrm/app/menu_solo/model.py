import random
from coremon_main.events import EventManager, CgmEvent
from gamecrm.defs_mco.ev_types import MyEvTypes
import gamecrm.defs_mco.glvars as glvars
from gamecrm.model.GlobOwnershipLands import GlobOwnershipLands
from gamecrm.shared.PlayerBehaviorFactory import PlayerBehaviorFactory
from gamecrm.shared.PlayerMod import PlayerMod
from gamecrm.shared.WorldMap import WorldMap


class MenuOptionsMod:
    MIN_NB_PLAYERS = 2
    MAX_NB_PLAYERS = 8

    def __init__(self):
        self._running = True
        self._nb_of_player_chosen = 2

        # TODO fix: why do we need graphics-related stuff here?!
        #oddlocator = pygame.image.load(os.path.join('data', 'images', 'oddLocator.PNG')).convert()
        #evenlocator = pygame.image.load(os.path.join('data', 'images', 'evenLocator.PNG')).convert()
        #grid = grids.HexagonGrid((30, 27), oddlocator, evenlocator, (50, 10))
        # rq TOM c utile de le faire là??
        # glvars.world = WorldMap.gen_random(glvars.gr_size, glvars.gr_offset, percent_grid_fill=0.8, add_dices=True)

        # players
        glvars.players = list()
        glvars.player_infos = list()
        for plcode in range(self._nb_of_player_chosen):
            pobj = PlayerMod(plcode, PlayerBehaviorFactory.HUMAN)
            glvars.players.append(pobj)
            glvars.player_infos.append(plcode)

        # - premier rand_map
        self.build_world_map()

    def build_world_map(self):
        print("building a new world map... ", end='')
        # REF unique!
        glvars.world = WorldMap.gen_random(glvars.gr_size, glvars.gr_offset, percent_grid_fill=0.75, add_dices=True)
        glvars.world.design_land_ownership()

    def decrease_players(self):
        if self._nb_of_player_chosen <= self.MIN_NB_PLAYERS:
            raise ValueError()

        self._nb_of_player_chosen -= 1

        glvars.players.pop()
        glvars.player_infos.pop()

        glvars.world.design_land_ownership()

    def increase_players(self):
        if self._nb_of_player_chosen >= self.MAX_NB_PLAYERS:
            raise ValueError()

        self._nb_of_player_chosen += 1

        glvars.players.append(PlayerMod(self._nb_of_player_chosen - 1, PlayerBehaviorFactory.HUMAN))
        glvars.player_infos.append(self._nb_of_player_chosen - 1)

        glvars.world.design_land_ownership()
