"""
In this module you will find some grid classes. They basically do nothing else
than converting from absolute coordinates to grid coordinates and vice versa.
"""


# TODO: perhaps a abstract super class?
# TODO: hexgrid but 30  (90) rotated
# TODO: get_offset()
# TODO: what if size of cells change, for zoom? set_cell_size()
# TODO: return center of tile in abs coord
# TODO: return topleft of tilein abs coord from abs coord


class SizeError(Exception):
    """
    raised when two sizes do not match.
    """
    def __init__(self, msg):
        Exception.__init__(self, msg)


# class RectGrid(object):
#     """
#     Rectangular grid. There are some usefull functions to convert from abs
#     coord to grid coord. Abs coord usually are pixel, but could also be
#     world coord (then you would have to convert from screen coord to world
#     coord to use this grid.
#     This does not store any information, only converts coordinates.
#     """
#
#     def __init__(self, num_cells, cell_size, offset=(0, 0)):
#         """
#         num_cells = (numX, numY)             Number of cells in each direction
#         cell_size = (cellWidth, cellHeight)  size off a cell in abs coordinates
#         offset   = (offsetX, offsetY)        offset in abs coordinates
#         """
#         object.__init__(self)
#         self._num_cell_x  = num_cells[0]
#         self._num_cell_y  = num_cells[1]
#         self._cell_width  = cell_size[0]
#         self._cell_height  = cell_size[1]
#         self._width  = self._num_cell_ x *self._cell_width
#         self._height = self._num_cell_ y *self._cell_height
#         self._offset_x = offset[0]
#         self._offset_y = offset[1]
#
#     def set_offset(self, offset):
#         """
#         set_offset(offset)
#         offset = (xoffset, yoffset) in abs coord.
#
#         """
#         self._offset_x, self._offset_y = offset
#
#     def abs_to_grid(self, abs_pos):
#         """
#         abs_to_grid(abs_pos) -> (xcell, ycell)
#         Use grid_coord_in_grid() to test is the returned coord are in the grid.
#         """
#         absx, absy = abs_pos
#         absx -= self._offset_x
#         absy -= self._offset_y
#         absx /= self._cell_width
#         absy /= self._cell_height
#         return (absx, absy)
#
#     def grid_to_abs(self, grid_coord):
#         """
#         grid_to_abs(grid_coord) -> (absx, absy)
#         """
#         return (self._offset_ x +self._cell_widt h *grid_coord[0], \
#                 self._offset_ y +self._cell_heigh t *grid_coord[1])
#
#     def abs_to_cell(self, abs_pos):
#         """
#         getCoordInCell(abs_pos) -> (locx, locy) or None
#         This are the coordinates whithin a cell. None if the abs_pos is not
#         in the grid. Even if the abs_pos is not on the grid, you will get
#         an result. To make sure abs_pos is on the gris use abs_coord_in_grid().
#         """
#         absx, absy = abs_pos
#         absx -= self._offset_x
#         absy -= self._offset_y
#         return absx % self._cell_width, absy % self._cell_height
#
#     def abs_coord_in_grid(self, abs_pos):
#         """
#         abs_coord_in_grid(abs_pos) -> True/False
#         Checks if the abs_pos is in the grid.
#         """
#         absx, absy = abs_pos
#         absx -= self._offset_x
#         absy -= self._offset_y
#         if absx < 0 or absx > self._width or absy < 0 or absy > self._height:
#             return False
#         return True
#
#     def grid_coord_in_grid(self, grid_pos):
#         """
#         grid_coord_in_grid(grid_pos) -> True/False
#         Check is an cell with that grid coord exists
#         """
#         gridx, gridy = grid_pos
#         if gridx < 0 or gridx >= self._num_cell_x or gridy < 0 or \
#                                                      gridy >= self._num_cell_y:
#             return False
#         return True
#
#     def get_adj_cells(self, grid_pos, use_diag=False):
#         """
#         get_adj_cells(grid_pos, use_diag=False) -> [cellCoord]
#         Returns a list [(ax, ay), (bx, by),...] with the adjectant cell coord
#         which are in the grid.
#         """
#         gridx, gridy = grid_pos
#         res = []
#         if use_diag:
#             adjc = [(grid x +1, grid y -1), (grid x +1, gridy), (grid x +1, grid y +1), \
#                     (gridx, grid y +1), (grid x -1, grid y +1), (grid x -1, gridy), \
#                     (grid x -1, grid y -1), (gridx, grid y -1)]
#         else:
#             adjc = [(grid x +1, gridy), (gridx, grid y +1), \
#                     (grid x -1, gridy), (gridx, grid y -1)]
#         for cell in adjc:
#             if self.grid_coord_in_grid(cell):
#                 res.append(cell)
#         return res
#
#     def get_num_cells(self):
#         """
#         get_num_cells() -> (numX, numY)
#         Number of cells in each direction.
#         """
#         return (self._num_cell_x, self._num_cell_y)
#
#     def set_num_cells(self, num_cells):
#         """
#         Set the size of the grid.
#         """
#         self._num_cell_x, self._num_cell_y = num_cells
#         self._width  = self._num_cell_ x *self._cell_width
#         self._height = self._num_cell_ y *self._cell_height
#
#     def get_size(self):
#         """
#         get_size() -> (width, height)
#         Returns the dimensions in absolute coord.
#         """
#         return (self._width, self._height)
#
#     def get_cell_size(self):
#         """
#         get_cell_size() -> (cellW, cellH)
#         """
#         return (self._cell_width, self._cell_height)


class HexagonGrid:
    """
    Hexagonal grid. There are some usefull functions to convert from abs 
    coord to grid coord. Abs coord usually are pixel, but could also be
    world coord (then you would have to convert from screen coord to world 
    coord to use this grid).
    This does not store any information, only converts coordinates.
    """
# TODO: use the image to generate an array, its faster to lookup
    def __init__(self, num_cells, odd_row_locator, even_row_locator, offset=(0, 0)):
        """
        num_cells = (numX, numY)             number of cells in each direction
        cell_size = (cellWidth, cellHeight)  size off a cell in abs coordinates
        odd_row_locator  = image              special image (pygame.Surface)to 
                                            identify in wich  hexagonal cell 
                                            we are (should look like a Y, left
                                            red, right green and up blue)
        even_row_locator = image              special image (pygame.Surface)
                                            (topleft blue, topright red and 
                                            lower part green)
        offset   = (offsetX, offsetY)       offset in abs coordinates
        """
        # TODO: var name clean up odd <-> even

        self._num_cell_x = num_cells[0]
        self._num_cell_y = num_cells[1]
        self._cell_width, self._cell_height = odd_row_locator.get_size()

        width, height = even_row_locator.get_size()

        if self._cell_width != width or self._cell_height != height:
            err_msg = "HexagonGrid.__init__: "
            err_msg += "odd_row_locator and even_row_locator must have same size!"
            raise SizeError(err_msg)

        self._even_offset = self._cell_width / 2
        self._width = self._num_cell_x * self._cell_width
        self._height = self._num_cell_y * self._cell_height

        self.offset_x = int(offset[0])
        self.offset_y = int(offset[1])

        self._odd_locator = odd_row_locator
        self._even_locator = even_row_locator

    def get_offset(self):
        return self.offset_x, self.offset_y

    def set_offset(self, offset):
        """
        set_offset(offset) 
        offset = (xoffset, yoffset) in abs coord.
        
        """
        self.offset_x, self.offset_y = int(offset[0]), int(offset[1])

    @staticmethod
    def pure_blue(color):
        #  == (0, 0, 255, 255)
        return (not color[0]) and (not color[1]) and (color[2] == 255) and color[3] == 255

    @staticmethod
    def pure_red(color):
        # (255, 0, 0, 255)
        return color[0] == 255 and (not color[1]) and (not color[2]) and color[3] == 255

    def abs_to_grid(self, abs_pos):
        """
        abs_to_grid(abs_pos) -> (xcell, ycell) 
        Use grid_coord_in_grid() to test is the returned coord are in the grid.
        """
        gridx, gridy = abs_pos
        gridx -= self.offset_x
        gridy -= self.offset_y
        
        locx = int(gridx % self._cell_width)
        locy = int(gridy % self._cell_height)
        
        gridx /= self._cell_width
        gridy /= self._cell_height
        
        decalage = (0, 0)
        if int(gridy) & 1:  # odd row
            color = self._odd_locator.get_at((locx, locy))
            if HexagonGrid.pure_red(color):
                decalage = (-1, 0)
            if HexagonGrid.pure_blue(color):
                decalage = (0, -1)

        else:  # even row
            color = self._even_locator.get_at((locx, locy))
            if HexagonGrid.pure_red(color):
                decalage = (0, -1)
            if HexagonGrid.pure_blue(color):
                decalage = (-1, -1)

        gridx += decalage[0]
        gridy += decalage[1]
        return int(gridx), int(gridy)

    # def grid_to_abs(self, grid_coord):
    #     """
    #     grid_to_abs(grid_coord) -> (absx, absy)
    #
    #     we return int values
    #     """
    #     gridx, gridy = grid_coord
    #
    #     if int(gridy) & 1:  # odd row add offset of cellW/2
    #         res = (
    #             self._cell_width * gridx + self.offset_x + self._even_offset,
    #             self._cell_height * gridy + self.offset_y
    #         )
    #
    #     else:  # even row
    #         res = (
    #             self._cell_width * gridx + self.offset_x,
    #             self._cell_height * gridy + self.offset_y
    #         )
    #
    #     return int(res[0]), int(res[1])

    # trying to optimize
    def grid_to_abs(self, grid_coord):
        """
        grid_to_abs(grid_coord) -> (absx, absy)
        """
        a = self.offset_x + grid_coord[0]*self._cell_width
        b = self.offset_y + grid_coord[1]*self._cell_height
        if grid_coord[1] % 2 == 1:  # is an odd row => add offset cellW/2
            a += self._even_offset
            return int(a), b
        else:
            return a, b

    def abs_to_cell(self, abs_pos):
        """
        Not implemented ( which coord system to use? TODO: position on hextile)
        """
        raise NotImplementedError
        
    def abs_coord_in_grid(self, abs_pos):
        """
        abs_coord_in_grid(abs_pos) -> True/False
        Checks if the abs_pos is in the grid.
        """
        return self.grid_coord_in_grid( self.abs_to_grid(abs_pos) )
        
    def grid_coord_in_grid(self, grid_pos):
        """
        grid_coord_in_grid(grid_pos) -> True/False
        Checks whether a cell with that grid coord exists
        """
        # gridx, gridy = grid_pos
        # if gridx < 0 or gridx >= self._num_cell_x or gridy < 0 or gridy >= self._num_cell_y:
        #     return False
        # return True

        return (self._num_cell_x > grid_pos[0] > 0) and (self._num_cell_y > grid_pos[1] > 0)
    
    # TODO: all arg for all other classes too
    def get_adj_cells(self, grid_pos, all=False, use_diag=False):
        """
        get_adj_cells(grid_pos, use_diag=False) -> [cellCoord]
        Returns a list [(ax, ay), (bx, by),...] with the adjectant cell coord
        which are in the grid.
        """
        gridx, gridy = grid_pos
        if int(gridy) & 1:  # odd
            res = []
            adjc = [
                (gridx + 1, gridy - 1),
                (gridx + 1, gridy),
                (gridx + 1, gridy + 1),
                (gridx, gridy + 1),
                (gridx - 1, gridy),
                (gridx, gridy-1)
            ]
            for cell in adjc:
                if self.grid_coord_in_grid(cell) or all:
                    res.append(cell)
            return res
        else:
            res = []
            adjc = [
                (gridx, gridy - 1),
                (gridx + 1, gridy),
                (gridx, gridy + 1),
                (gridx - 1, gridy + 1),
                (gridx - 1, gridy),
                (gridx - 1, gridy - 1)
            ]
            for cell in adjc:
                if self.grid_coord_in_grid(cell) or all:
                    res.append(cell)
            return res
        
    def get_num_cells(self):
        """
        get_num_cells() -> (numX, numY)
        Number of cells in each direction.
        """
        return self._num_cell_x, self._num_cell_y
    
    def set_num_cells(self, num_cells):
        """
        Set the size of the grid.
        """
        self._num_cell_x, self._num_cell_y = num_cells
        self._width = self._num_cell_x * self._cell_width
        self._height = self._num_cell_y * self._cell_height
    
    def get_size(self):
        """
        get_size() -> (width, height)
        Returns the dimensions in absolute coord.
        """
        sqrt1div12 = 0.28867513459481292  # == sqrt(1./12.)
        return self._width + self._even_offset, self._height + self._width*sqrt1div12

    def get_cell_size(self):
        """
        get_cell_size() -> (cellW, cellH)
        It returns the size of the hex tile.
        """
        return self._cell_width, self._cell_height
        # int(\
        #        round((self._cell_widt h * 0.28867513459481292))) # == sqrt(1./12.)


# TODO: Isometric variante fuer 2:1 ratio
# map ander rum: x,y sind auf map rechtwinklige Koord

# http://www.wired-weasel.com/users/serhid/tutos/tut5.html
# http://www.wired-weasel.com/users/serhid/tutos/tut6.html


##    def screen_to_tile(self, pos):
##        """
##        Returns a tile coord of a screen coord
##        """
##        mx,my = pos
##        mx -= self.offset[0]
##        my -= self.offset[1]
##        x0 = mx - (self.tile_size[0]/2)
##        y0 = my
##        x = y0 + (x0 / 2)
##        y = y0 - (x0 / 2)
##        x /= self.tile_size[0]/2
##        y /= self.tile_size[0]/2
##        return (x, y)
##
##    def tile_to_screen( self, pos ):
##        """
##        Returns topleft position on screen of the tile coord.
##        """
##        pos_x, pos_y = pos
##        screen_x = self.tile_size[0]/2*(pos_x-pos_y)+self.offset[0]
##        screen_y = self.tile_size[1]/2*(pos_x+pos_y)+self.offset[1]
##        return screen_x, screen_y


# class IsometricGrid(object):
#     """
#     Isometric grid. There are some usefull functions to convert from abs
#     coord to grid coord. Abs coord usually are pixel, but could also be
#     world coord (then you would have to convert from screen coord to world
#     coord to use this grid).
#     This does not store any information, only converts coordinates.
#
#     links:
#
#     http://www.ul.ie/~rynnet/keanea/HomePage.html
#     http://rhysd.syntesis.org/tutorial/index.php
#     """
#
#     def __init__(self, num_cells, iso_locator, offset=(0, 0)):
#         """
#         num_cells = (numX, numY)             number of cells in each direction
#         cell_size = (cellWidth, cellHeight)  size off a cell in abs coordinates
#         odd_row_locator  = image              special image to identify in wich
#                                             hexagonal cell we are (should look
#                                             like a Y, left red, right green and
#                                             up blue)
#         even_row_locator = image              special image (topleft blue,
#                                             topright red and lower part green)
#         offset   = (offsetX, offsetY)       offset in abs coordinates
#         """
#         object.__init__(self)
#         self._num_cell_x  = num_cells[0]
#         self._num_cell_y  = num_cells[1]
#         self._cell_width, self._cell_height = iso_locator.get_size()
#         self._odd_row_offset = self._cell_widt h /2
#         self._odd_col_offset = self._cell_heigh t /2
#         self._width  = self._num_cell_ x *self._cell_width
#         self._height = self._num_cell_ y *self._cell_height
#         self._offset_x = offset[0]
#         self._offset_y = offset[1]
#         self._locator = iso_locator
#
#     def set_offset(self, offset):
#         """
#         set_offset(offset)
#         offset = (xoffset, yoffset) in abs coord.
#
#         """
#         self._offset_x, self._offset_y = offset
#
#     def abs_to_grid(self, abs_pos):
#         """
#         abs_to_grid(abs_pos) -> (xcell, ycell)
#         Use grid_coord_in_grid() to test is the returned coord are in the grid.
#         """
    #     gridx, gridy = abs_pos
    #     gridx -= self._offset_x
    #     gridy -= self._offset_y
    #
    #     locx = gridx % self._cell_width
    #     locy = gridy % self._cell_height
    #
    #     gridx /= self._cell_width
    #     gridy /= self._cell_height
    #     gridy *= 2
    #     displacement = (0, 0)
    #     color = self._locator.get_at((locx, locy))
    #     if color == (255, 0, 0, 255):
    #         displacement = (-1, -1) # red
    #     if color ==(0, 0, 255, 255):
    #         displacement = (0, 1)   # blue
    #     if color ==(0, 255, 0, 255):
    #         displacement = (0, -1)  # green
    #     if color ==(0, 0, 0, 255):
    #         displacement = (-1, 1)  # black
    #     gridx += displacement[0]
    #     gridy += displacement[1]
    #     return gridx, gridy
    #
    # def grid_to_abs(self, grid_coord):
    #     """
    #     grid_to_abs(grid_coord) -> (absx, absy)
    #     """
    #     gridx, gridy = grid_coord
    #     if gridy & 1: # odd row add offset of cellW/2
    #         return (self._cell_width * gridx + self._offset_x +  \
    #                                                     self._odd_row_offset\
    #                , self._cell_height * (gridy /2) + self._offset_y +  \
    #                                                     self._odd_col_offset)
    #     else: # even row
    #         return (self._cell_width * gridx + self._offset_x, \
    #                 self._cell_height * (gridy /2) + self._offset_y)
    #
    # def abs_to_cell(self, abs_pos):
    #     """
    #     Not implemented ( which coord system to use? TODO: position on isotile)
    #     """
    #     raise NotImplementedError
    #
    # def abs_coord_in_grid(self, abs_pos):
    #     """
    #     abs_coord_in_grid(abs_pos) -> True/False
    #     Checks if the abs_pos is in the grid.
    #     """
    #     return self.grid_coord_in_grid( self.abs_to_grid(abs_pos) )
    #
    # def grid_coord_in_grid(self, grid_pos):
    #     """
    #     grid_coord_in_grid(grid_pos) -> True/False
    #     Check is an cell with that grid coord exists
    #     """
    #     gridx, gridy = grid_pos
    #     if gridx < 0 or gridx >= self._num_cell_x or gridy < 0 or \
    #                                                  gridy >= self._num_cell_y:
    #         return False
    #     return True
    #
    # def get_adj_cells(self, grid_pos, use_diag=False):
    #     """
    #     get_adj_cells(grid_pos, use_diag=False) -> [cellCoord]
    #     Returns a list [(ax, ay), (bx, by),...] with the adjectant cell coord
    #     which are in the grid.
    #     """
    #     gridx, gridy = grid_pos
    #     res = []
    #     adjc = []
    #     if grid y &1: # odd
    #         if use_diag:
    #             adjc = [(grid x +1, grid y -1), (grid x +1, gridy), \
    #                  (grid x +1, grid y +1), (gridx, grid y +2), (gridx, grid y +1), \
    #                  (grid x +1, gridy), (gridx, grid y -1), (gridx, grid y -2)]
    #         else:
    #             adjc = [(grid x +1, grid y -1), (grid x +1, grid y +1), \
    #                  (gridx, grid y +1), (gridx, grid y -1)]
    #     else: # even
    #         if use_diag:
    #             adjc = [(gridx, grid y -1), (grid x +1, gridy), \
    #                  (gridx, grid y +1), (gridx, grid y +2), (grid x -1, grid y +1), \
    #                  (grid x +1, gridy), (grid x -1, grid y -1), (gridx, grid y -2)]
    #         else:
    #             adjc = [(gridx, grid y -1), (gridx, grid y +1), \
    #                  (grid x -1, grid y +1), (grid x -1, grid y -1)]
    #
    #     for cell in adjc:
    #         if self.grid_coord_in_grid(cell):
    #             res.append(cell)
    #     return res
    #
    # def get_num_cells(self):
    #     """
    #     get_num_cells() -> (numX, numY)
    #     Number of cells in each direction.
    #     """
    #     return (self._num_cell_x, self._num_cell_y)
    #
    # def set_num_cells(self, num_cells):
    #     """
    #     Set the size of the grid.
    #     """
    #     self._num_cell_x, self._num_cell_y = num_cells
    #     self._width  = self._num_cell_ x *self._cell_width
    #     self._height = self._num_cell_ y *self._cell_height
    #
    # def get_size(self):
    #     """
    #     get_size() -> (width, height)
    #     Returns the dimensions in absolute coord.
    #     """
    #     return (self._widt h +self._odd_row_offset, self._height +\
    #                                                 self._odd_col_offset)
    #
    # def get_cell_size(self):
    #     """
    #     get_cell_size() -> (cellW, cellH)
    #     It returns the size of the hex tile.
    #     """
    #     return (self._cell_width, self._cell_height  )# == sqrt(1./12.)
