import random

from coremon_main.events import CgmEvent, EventManager
from gamecrm.defs_mco.ev_types import MyEvTypes
from gamecrm.shared.PlayerMod import PlayerMod


class Land:
    """
    A Land is a conjunction of some cells on the map. This class has usefull
    functions to perform operations.
    The Lands form a graph when thy are linked together.
    """
    _free_id = 1

    def __init__(self, mapref, given_landid=None):
        self._manager = EventManager.instance()
        self._world = mapref  # ref. to the world this Land belongs to

        if given_landid is None:
            self._land_id = Land._free_id
            Land._free_id += 1
        else:
            self._land_id = given_landid

        self._links = []  # adjectant Lands, next time better using LandID
        self._cells = []  # [(x,y),...] cells owned by this land

        self.selected = False
        self._cached_cc = None  # a trick to optimize gfx paint speed, contains coords of the center cell
        # FOR MORE INFO, see: self.get_center_cell

    def get_id(self):
        """
        Returns the land id.
        """
        return self._land_id

    def _get_cells(self):
        """
        Returns a copy of the cells list of this Land.
        """
        return list(self._cells)

    cells = property(_get_cells, None, None, "a copy of cells used by this land, read only")

    def link(self, other_land):
        """
        Connects this Land to the other and vice versa to form a graph (double
        linked nodes).
        """
        if other_land not in self._links and other_land != self:
            self._links.append(other_land)
            other_land.link(self)

    def unlink(self, other):
        """
        Deletes the link between this and the other Land.
        """
        if other in self._links:
            self._links.remove(other)
            other.unlink(self)

    def set_pid(self, given_pid):
        raise NotImplementedError

    def set_player(self, player):
        raise NotImplementedError

        # """
        # Set the player this Land belongs to.
        # Player must implement follwing methods:
        #     removeLand(land)
        #     addLand(land)
        # """
        # ownership_changes = False
        #
        # if player is None:
        #     self._player = None
        # else:
        #     if player != self._player:
        #         ownership_changes = True
        #
        # if ownership_changes:
        #     if self._player is not None:
        #         self._player.remove_land(self)
        #
        #     self._player = player
        #     player.add_land(self)
        #
        #     pid_now = player.get_pid()
        #     self._manager.post(
        #         CgmEvent(MyEvTypes.LandOwnerChanges, pid=pid_now, land_id=self._land_id, owner_pid=player.get_pid())
        #     )

    def add_cell(self, cell: tuple):
        """
        Add a cell of the map grid to belong to this land.
        """
        self._cells.append(cell)
        if cell in self._world.cells:
            land = self._world.cells[cell]
            if land and land != self:
                land.removeCell(cell)
            self._world.cells[cell] = self

    def remove_cell(self, cell):
        """
        Removes a cell from this Land.
        """
        if cell in self._cells:
            self._cells.remove(cell)
            self._world.cells[cell] = None

    def grow(self, num_cells=1):
        """
        This will let the Land grow about the number of cells you provide.
        Default growth is 1 cell. It will chose an adjectant cell randomly and
        add it if the cell is not taken yet.
        """
        added_cells = 0
        ##        for i in range(num_cells):
        while num_cells > 0:
            num_cells -= 1
            cells = self.get_empty_adj_cells()
            if len(cells):
                self.add_cell(random.choice(cells))
                added_cells += 1
        return added_cells

    def get_adj_cells(self, diag=False):
        """
        -> [(),()]
        Returns a list of any adjectant cells on the map grid (empty and taken
        cells). Could be an empty list (then this Land would occupy the whole
        map).
        """
        adj_cells = []
        for cell in self._cells:
            for adjcell in self._world.grid.get_adj_cells(cell, diag):
                if adjcell not in self._cells:
                    adj_cells.append(adjcell)
        return adj_cells

    def get_empty_adj_cells(self):
        """
        ->[(),()]
        Returns a list of empty, adjectand cells. This list could be empty.
        """
        empty = []
        for adjcell in self.get_adj_cells():
            if self._world.cells[adjcell] is None:
                empty.append(adjcell)
        return empty

    def get_adj_lands(self):
        """
        Returns the Land that are adjectant on the map. This are not
        necesairely the lands this land is linked with.
        """
        adj_lands = []
        for cell in self.get_adj_cells():
            land = self._world.cells[cell]
            if land:
                adj_lands.append(land)
        return adj_lands

    def get_linked_lands(self):
        """
        This returns the lands which has been linked with this land. These
        lands dont need to bee the adjectant ones.
        """
        return list(self._links)

    def destroy(self):
        """
        Destroys this object, actually delete all references so garbage
        collector can remove it.
        """
        for other in self._links:
            self.unlink(other)
        self.setPlayer(None)
        self._world = None

    # -------------------
    # TODO: trouver fix
    # problème ceci concerne le graphisme et pas le modèe...
    # -------------------

    # ------testing---------------#FF0000#FFFF---------------
    # see: Schwerpunk-Flaeche.png, no because center of mass can be outside!
    def get_center_cell(self):
        """
        Returns the cell witch is in the center of the land.
        """
        if self._cached_cc:
            res = self._cached_cc
        else:
            xsum = 15
            ysum = 15
            for cell in self._cells:
                # xcoord, ycoord = cell
                xcoord, ycoord = self._world.grid.grid_to_abs(cell)
                xsum += xcoord
                ysum += ycoord
            num_cells = len(self._cells)
            xsum /= num_cells
            ysum /= num_cells
            # xsum = int(round(xsum))
            # ysum = int(round(ysum))
            # center_cell = (xsum, ysum)
            center_cell = self._world.grid.abs_to_grid((xsum, ysum))
            if center_cell not in self._cells:
                for cell in self._world.grid.get_adj_cells(center_cell):
                    if cell in self._cells:
                        center_cell = cell
                        break
            self._cached_cc = res = center_cell
        return res

    # ++ ALTERNATIVE mthod ++
    # +++++++++++++++++++++++
    #
    # def get_center_cell_tmp2(self):
    #     """
    #     Returns the cell witch is in the center of the land.
    #     """
    #     xmax = 0
    #     xmin = 10000000
    #     ymax = 0
    #     ymin = 10000000
    #     for cell in self._cells:
    #         # xcoord, ycoord = cell
    #         xcoord, ycoord = self._world.grid.grid_to_abs(cell)
    #         if xcoord > xmax:
    #             xmax = xcoord
    #         if ycoord > ymax:
    #             ymax = ycoord
    #
    #         if xcoord < xmin:
    #             xmin = xcoord
    #         if ycoord < ymin:
    #             ymin = ycoord
    #
    #     centerx = (xmin + xmax) / 2 + 1
    #     centery = (ymin + ymax) / 2 + 1
    #
    #     center_cell = self._world.grid.abs_to_grid((centerx, centery))
    #     if center_cell not in self._cells:
    #         for cell in self._world.grid.get_adj_cells(center_cell):
    #             if cell in self._cells:
    #                 center_cell = cell
    #                 break
    #
    #     return center_cell
