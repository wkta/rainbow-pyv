import pygame
import random
from os.path import join as join_path
from coremon_main.defs import EngineEvTypes
from coremon_main.events import EventReceiver
import gamecrm.defs_mco.glvars as glvars
import coremon_main.conf_eng as cgmconf
from gamecrm.app.conquest.ConquestMod import ConquestMod
from gamecrm.defs_mco.ev_types import MyEvTypes
import gamecrm.image_helper as img_helper
from gamecrm.model.GlobOwnershipLands import GlobOwnershipLands


class ConquestView(EventReceiver):

    def __init__(self, refmod: ConquestMod):
        super().__init__()
        self._ref_mod = refmod
        self._own_infos = GlobOwnershipLands.instance()

        self._screen = cgmconf.get_screen()
        self.world = glvars.world

        self.font1 = glvars.fonts['big_pesos_display_font']
        self.font2 = glvars.fonts['default_med_font']

        self.current_w_label = self.font2.render("CURRENT", 2, (0, 0, 0, 255))
        self.player_w_label = self.font2.render("PLAYER= ", 2, (0, 0, 0, 255))

        self.surf_repr_number = dict()
        for n in range(0, 9):
            self.surf_repr_number[n] = self.font1.render(str(n), 2, (80, 0, 200, 155))

        # color for each player (actually an index)
        self.player_color = {}
        idx = 0
        print(">>>>>>>>>Graphics:", glvars.players)
        for player in glvars.players:
            self.player_color[player.get_pid()] = idx
            idx += 1

        # -- load tiles --
        dir_path = join_path('assets')
        tile_names = ['g_hexDGruen.PNG', 'g_hexGelb.PNG', 'g_hexHGruen.PNG', \
                      'g_hexOrange.PNG', 'g_hexRosa.PNG', 'g_hexRot.PNG', \
                      'g_hexTuerkis.PNG', 'g_hexViolette.PNG', 'g_hexSchwarz.PNG']
        self.tiles = []
        for name in tile_names:
            path = join_path(dir_path, name)
            img = pygame.image.load(path).convert()
            img.set_colorkey((0x80, 0x00, 0x80))
            self.tiles.append(img)

        # generate map image with borders
        self.map_img = None
        self.generate_borders()

        random.shuffle(self.tiles[:-1])
        if len(self.tiles) != len(self.player_color):
            print("num tiles:", len(self.tiles), "num player:", len(self.player_color))
        self.current = None
        ##        self.reg_event_func(eventtypes.ATTACKRESULT, self.on_attack_result)
        # self.reg_event_func(eventtypes.NEWTURN, self.on_newturn)

        self.bg_img = pygame.image.load(img_helper.filename_bg()).convert()

    def proc_event(self, ev, source):
        # TODO retire update( ) de cette classe, utilise event PAINT...
        # if ev.type == MyEvTypes.TurnBegins:
        # #if ev.type == eventtypes.NEWTURN:
        #     self.on_newturn(ev)

        if ev.type == EngineEvTypes.PAINT:
            self._on_paint(ev.screen)

    def generate_borders(self):
        adhoc_colorkey = img_helper.get_t_colorkey()
        borders = []
        for elt in img_helper.filenames_4borders():
            img = pygame.image.load(elt).convert()
            img.set_colorkey(adhoc_colorkey)
            borders.append(img)

        self.map_img = pygame.Surface(self.world.grid.get_size()).convert()
        self.map_img.fill(adhoc_colorkey)  # fill with color_key
        self.map_img.set_colorkey(adhoc_colorkey)

        # draw borders
        num_cells = self.world.grid.get_num_cells()
        for posy in range(num_cells[1]):
            for posx in range(num_cells[0]):
                cell_land = self.world.cells[(posx, posy)]
                # get adj cells
                adj_cells = self.world.grid.get_adj_cells((posx, posy), True)
                # calculate position to blit
                blitx, blity = self.world.grid.grid_to_abs((posx, posy))
                # TODO: hack!!
                blitx -= self.world.grid.offset_x
                blity -= self.world.grid.offset_y
                # go through adj and check if they are from a different land
                for idx, adjcell in enumerate(adj_cells):
                    # check if cell is on map
                    if adjcell in self.world.cells:
                        if cell_land != self.world.cells[adjcell]:
                            self.map_img.blit(borders[idx], (blitx, blity))
                    else:
                        if cell_land:
                            self.map_img.blit(borders[idx], (blitx, blity))

    def _on_paint(self, screen):
        screen.blit(self.bg_img, (0, 0))

        tiles = self.tiles
        grid_toabs = self.world.grid.grid_to_abs
        cached_tile = None

        # this draws small hex images
        full_list = self.world.get_lands()
        for land in full_list:
            for cell in land.cells:
                if land.selected:
                    screen.blit(tiles[-1], grid_toabs(cell))
                else:
                    player_cod = self._own_infos[land.get_id()]
                    idx = self.player_color[player_cod]
                    screen.blit(tiles[idx], grid_toabs(cell))
                    if self._ref_mod.get_current_player() == player_cod:
                        cached_tile = tiles[idx]

        # - - ++ debug ++ - -
        # with this line we can display id of a land
        # self.draw_string2(screen, str(full_list[0].get_id()), grid_toabs(full_list[0].cells[0]))

        # this draws borders for all regions!
        screen.blit(self.map_img, grid_toabs((0, 0)))

        # displays current player info
        if cached_tile:
            screen.blit(self.current_w_label, (660, 300))
            screen.blit(self.player_w_label, (660, 330))
            screen.blit(cached_tile, (765, 330))

        # this draws the number of dice on each land
        for land in self.world.get_lands():
            screen.blit(
                self.surf_repr_number[land.num_dice], grid_toabs(land.get_center_cell())
            )

    def on_attack_result(self, event):
        """
        
        """
        print("attack result animation!!")
        return False

    def on_newturn(self, event):
        self.current = event.curr_player.get_pid()  #playerid

    def draw_string(self, screen, text, where):
        i = self.font1.render(text, 2, (80, 0, 200, 155))
        screen.blit(i, where)

    def draw_string2(self, screen, text, where):
        i = self.font2.render(text, 2, (0, 0, 0, 255))
        screen.blit(i, where)