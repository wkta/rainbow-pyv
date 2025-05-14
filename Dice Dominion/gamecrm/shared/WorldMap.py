import json
import random

import pygame

import gamecrm.defs_mco.glvars as glvars
import gamecrm.image_helper as img_helper
from coremon_main.events import CogObject
from gamecrm.defs_mco.ev_types import MyEvTypes
from gamecrm.model import diceland
from gamecrm.model.GlobOwnershipLands import GlobOwnershipLands
from gamecrm.model.diceland import DiceLand
from gamecrm.shared import grids


class WorldMap(CogObject):

    def __init__(self, grid_size, grid_offset, store_cells, store_owner):
        """
        :param grid_size:
        :param grid_offset:
        :param store_cells: dictionnaire associant region_id à une liste de cellules
        :param store_owner: dictionnaire associant region_id à un identifiant de joueur
        """
        super().__init__()

        # -- base du constructeur
        # create grid
        (odd_loc_fn, even_loc_fn) = img_helper.odd_n_even_img_filenames()
        odd_loc_img = pygame.image.load(odd_loc_fn)
        even_loc_img = pygame.image.load(even_loc_fn)
        self.grid = grids.HexagonGrid(
            glvars.grid_myst_parameter, odd_loc_img, even_loc_img, offset=grid_offset
        )
        self.grid.set_num_cells(grid_size)

        # create cells
        self.cells = dict()  # dict in the form of {(cx, cy):Land}, it holds Land references
        for xnum in range(grid_size[0]):
            for ynum in range(grid_size[1]):
                self.cells[(xnum, ynum)] = None

        # set-up lands
        self.__lid_to_land = dict()
        self.__lands = []
        for land_id in store_cells.keys():
            k = int(land_id)
            cell_list = store_cells[land_id]
            land = diceland.DiceLand(self, k)
            self.ajoutland(land)
            for cell in cell_list:
                land.add_cell(tuple(cell))
        for land in self.__lands:  # link the lands
            for adjland in land.get_adj_lands():
                land.link(adjland)

        # set-up ownership
        self._own_infos = GlobOwnershipLands.instance()
        self._own_infos.inject_state(store_owner)

        # -- rab constructeur
        self._islands = []  # [[lands],[lands],...] => len(islands)>=1
        self._num_filled_cells = 0  # how many cells should be filled
        self._num_cells_in_land = 0  # how many cells are in a land
        self._num_lands = len(self.__lid_to_land)  # how many lands are on the map

    def ajoutland(self, ref_lan):
        self.__lands.append(ref_lan)
        self.__lid_to_land[ref_lan.get_id()] = ref_lan

    # TODO rendre traitement/chainage des méthodes plus propre...
    @classmethod
    def gen_random(cls, gr_size, gr_offset, num_lands=30, cells_in_land=None, percent_grid_fill=0.8, add_dices=False):
        obj = WorldMap(gr_size, gr_offset, {}, {})
        obj.__do_randomize(num_lands, cells_in_land, percent_grid_fill)
        return obj

    def __do_randomize(self, num_lands, cells_in_land, percent_grid_fill):
        """
        Creates a new map. You to call this function before you can use the 
        map. To tune you map there are some parameter that you can change:

        num_lands         : number of Land this map must have

        cells_in_land     : there you can define how many cell a land has
                            if this is None the number of cells in a land is
                            calculated cells_in_land = numFilledCells/num_lands
        percent_grid_fill : percentage 0.0-1.0 of how many cell of the map 
                            should be occupied, only works 
                            if cells_in_land==None
        """
        numgrid_x, numgrid_y = self.grid.get_num_cells()
        self._num_filled_cells = int(numgrid_x * numgrid_y * percent_grid_fill)
        if cells_in_land:
            self._num_cells_in_land = cells_in_land
        else:
            self._num_cells_in_land = self._num_filled_cells / num_lands
        self._num_lands = num_lands

        # --------------------
        # Gnerates a new random layout of the map.
        # --------------------

        # remove old lands and links
        self._create()

        self._find_islands()  # stores results in self._islands
        n = 0
        while len(self._islands) > 1:
            self._create()
            self._find_islands()
            n += 1
            print("map gen tries:", n)

        if len(self._islands) > 1:
            # not all have been reached islands has been detected
            print(len(self._islands), "island lands:")
            for island in self._islands:
                for node in island:
                    print(node.get_id())
                print("------------------")

    def _create(self):
        # on retire tt reference aux land objects existants
        del self.__lands[:]
        self.__lid_to_land.clear()
        self.cells.clear()

        # init nouvelle grille, et objets type DiceLand
        numgrid_x, numgrid_y = self.grid.get_num_cells()
        for gridx in range(numgrid_x):
            for gridy in range(numgrid_y):
                self.cells[(gridx, gridy)] = None

        for k in range(self._num_lands):
            self.ajoutland(DiceLand(self))

        # set random cells for starting
        chosen_cells = random.sample(self.cells.keys(), self._num_lands)

        # lets add some lands to the grid
        idx = 0
        for cell in chosen_cells:
            self.cells[cell] = self.__lands[idx]
            self.__lands[idx].add_cell(cell)
            idx += 1

        num_cells = int(self._num_cells_in_land)
        for i in range(num_cells):
            ##        while num_cells: # not good, eventually endless loop!
            # for each land
            for land in random.sample(self.__lands, len(self.__lands)):
                # as long number of cells per land is not reached
                if len(land.cells) < self._num_cells_in_land:
                    growth = land.grow()
                    num_cells -= growth

        # old land generation code, first try
        ##        num_cells = self._num_cells_in_land
        ##        for i in range(num_cells):
        ##            # for each land
        ##            for land in self._lands:
        ##                # 0 get cells of land
        ##                cells = list(land.cells)
        ##                # 1 if num_cells>=cellperLand -> quit
        ##                if len(cells)<self._num_cells_in_land:
        ##                    for dumy in cells:
        ##                        # 2 chose a cell
        ##                        c = random.choice(cells)
        ##                        # 3 get adjectants
        ##                        adjCells = self.grid.getAdjCells(c)
        ##                        # 4 remove all taken ones
        ##                        for ac in list(adjCells):
        ##                            if self.cells[ac]!=None:
        ##                                self.cells[c].link(self.cells[ac])
        ##                                adjCells.remove(ac)
        ##                        # 5 if non left remove chosen cell and goto 2
        ##                        if len(adjCells):
        ##                            # 6 chose one of adjlist
        ##                            ac = random.choice(adjCells)
        ##                            # 7 occupi it
        ##                            self.cells[ac] = land
        ##                            land.addCell(ac)
        ##                            break;
        ##                        else:
        ##                            num_cells += 1

        # TODO: check for not reachable (*) lands and do something against
        # like move it, put an additional land between, ...
        # (*): graph algo that check if every node is reachable!

        # link the lands
        for land in self.__lands:
            for adj_land in land.get_adj_lands():
                land.link(adj_land)

    ###            if len(land._links)<2: #TODO: parameter
    ##            if len(land.get_linked_lands())<2: # does not guarantee that no island exists
    ##                print "Warning: land not Linked!"
    ##                num = 1000
    ##                while len(land.get_linked_lands())<2 and num:
    ##                    land.grow()
    ##                    for adjl in land.get_adj_lands():
    ##                        land.link(adjl)
    ##                    num -= 1

    def _find_islands(self):
        """
        
        """
        # DepthFirstSearch algo
        # to find out if there are islands
        islands = []
        nodes = list(self.__lands)
        while len(nodes):
            visited = []
            stack = []  # use append() and pop()
            start_node = nodes.pop()
            visited.append(start_node)
            stack.append(start_node)
            while len(stack):
                current_node = stack.pop()
                for adj_node in current_node._links:
                    if adj_node not in visited:
                        stack.append(adj_node)
                        visited.append(adj_node)
                        if adj_node in nodes:
                            nodes.remove(adj_node)
            islands.append(visited)
        self._islands = islands

    def get_land_from_abs(self, pos):
        """
        Returns the Land at absPos or None if there isnt one.
        """
        gridpos = self.grid.abs_to_grid(pos)
        if self.grid.grid_coord_in_grid(gridpos):
            return self.cells[gridpos]

    def design_land_ownership(self):
        # TODO optimiser ce bordel pr moins de création de listes...
        print("+random ownership of lands...", end='')
        own = GlobOwnershipLands.instance()
        own.rand_giveaway(glvars.world.dump_all_ids(), len(glvars.players))

        # notify the view
        print('done!')
        self.pev(MyEvTypes.MapChanges)

    # -------------------------------------
    #  Getters
    # -------------------------------------
    def dump_all_ids(self):
        res = list()
        for lan in self.__lands:
            res.append(lan.get_id())
        return res

    def get_lands(self):
        return self.__lands

    def get_land_by_id(self, land_id):
        # TODO trouver origine bug chiant
        #  return self.__lid_to_land[land_id]

        for lan in self.__lands:
            if lan.get_id() == land_id:
                return lan
        raise ValueError

    # ----------
    # mécanismes de sérialisation
    # ----------
    def serialize(self):
        """
        :return: a serial (str) in the following format:
        [
            [nbcells_w, nbcells_h],
            [offsetx, offsety],
            {IDof_cell1: [x_cell1, y_cell1], IDof_cell2: [..., ... ], ... },
            {IDof_cell1: belongcode_cell1, IDof_cell2: belongcode_cell2, ...}
        ]
        """
        # remark/future refactoring idea: should save number of dices in dict too?
        # store_a = dict()
        # store_b = dict()

        res = "["
        res += "[{}, {}],".format(*self.grid.get_num_cells())
        res += "[{}, {}],".format(*self.grid.get_offset())
        res += "{"

        worldsig = self.get_lands()
        tworld = len(worldsig)

        for k in range(tworld):
            land = worldsig[k]
            tempp = list(map(list, land.cells))  # convert all tuples to list
            res += '"{}": '.format(land.get_id()) + json.dumps(tempp)
            if k < tworld - 1:
                res += ","

        res += "},"

        # ownership...
        # for k in range(tworld):
        #     land = worldsig[k]
        #     res += '"{}": {}'.format(land.get_id(), land.get_pid())
        #     if k < tworld - 1:
        #         res += ","
        res += self._own_infos.serialize()

        res += "]"

        # for land in self.get_lands():
        #     k = land.get_id()
        #     store_a[k] = land.cells
        #     store_b[k] = land.get_pid()
        # res = (self.grid.get_num_cells(), self.grid.get_offset(), store_a, store_b)
        # return json.dumps(res)

        return res

    @classmethod
    def deserialize(cls, given_serial):
        print('xx')
        print(given_serial)
        print('yy')
        obj = json.loads(given_serial)
        grid_size, grid_offset, store_a, ownership = obj
        return cls(grid_size, grid_offset, store_a, ownership)
