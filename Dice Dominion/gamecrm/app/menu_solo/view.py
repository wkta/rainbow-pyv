import coremon_main.gui as gui
import gamecrm.defs_mco.glvars as glvars
import gamecrm.image_helper as img_helper
import pygame
from coremon_main.events import EventReceiver, EngineEvTypes, CgmEvent, EventManager, PygameBridge
from gamecrm.defs_mco.ev_types import MyEvTypes
from gamecrm.defs_mco.fonts_n_colors import my_colors
from gamecrm.defs_mco.gamestates import GameStates
from gamecrm.defs_mco.netw_codes import *
from gamecrm.model.GlobOwnershipLands import GlobOwnershipLands
from gamecrm.shared.PlayerBehaviorFactory import PlayerBehaviorFactory
from gamecrm.custom_gui import Spinner, Item, Text
import coremon_main.conf_eng as cgmconf


class MenuOptionsView(EventReceiver):
    POS_BT_DUMP_MAP = (290, 310)

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            self.on_paint(ev)

        # - les clics sont gérés par chaque bouton / spinner lui-même
        # elif ev.type in (PygameBridge.MOUSEBUTTONDOWN, PygameBridge.MOUSEBUTTONUP):
        #     self.on_click(ev)

        elif ev.type == MyEvTypes.MapChanges:
            self.on_map_change(ev)

    def __init__(self, ref_mod):
        self.bg_color = pygame.Color(my_colors['fond_anto'])

        super().__init__()  # todo gérer priorité ? anciennement cétait 5

        self.ref_mod = ref_mod

        # - create gui elements
        self.font = glvars.fonts['courier_font']
        self.buttons = []

        self.buttons.append(gui.Button(self.font, "randomize map", (50, 350), self.ref_mod.build_world_map))

        def tmpfunc():
            EventManager.instance().post(
                CgmEvent(MyEvTypes.RequestMap)
            )
        self.buttons.append(gui.Button(self.font, 'load_map', (50, 320), tmpfunc))

        self.buttons.append(gui.Button(self.font, "randomize lands", (200, 350), glvars.world.design_land_ownership))

        self.buttons.append(gui.Button(self.font, "start", (500, 350), self.sig_wanna_start))
        self.buttons.append(gui.Button(self.font, "exit", (600, 350), self.sig_wanna_quit))

        b = gui.Button(self.font, 'dump_worldmap', self.POS_BT_DUMP_MAP, self._do_dump_map)
        self.buttons.append(b)

        self.spinners = []
        self.texts = []

        self.netw_id_spinner = Spinner(self.font, (550, 10), True)  # cyclique
        for k in range(8):
            self.netw_id_spinner.add(Item(str(k), k))
        self.netw_id_spinner.register_observer(self)
        self.netw_id_spinner.turn_on()

        # number of players
        xpos = 500
        ypos = 30
        self.texts.append(Text("number of Players: ", self.font, (xpos, ypos)))
        spinner = Spinner(self.font, (xpos + 180, ypos), False)
        for num in range(2, 9):
            spinner.add(Item(str(num), num))
        spinner.register_observer(self)
        self.spinners.append(spinner)

        # player config
        self.items = []
        self.items.append(Item("human", PlayerBehaviorFactory.HUMAN))
        self.items.append(Item("remote", PlayerBehaviorFactory.NETWORK))
        #self.items.append(gui.Item("passive AI", PlayerImplemFactory.AI_PASSIVE))
        self.items.append(Item("expander AI", PlayerBehaviorFactory.AI_DUMB))
        self.items.append(Item("AI 1", PlayerBehaviorFactory.AI_1))
        self.items.append(Item("none", None))

        for num in range(2):
            ypos += 30
            spinner = Spinner(self.font, (xpos + 100, ypos))
            if num == 2:
                self.items.insert(0, self.items.pop(-1))
            for item in self.items:
                spinner.add(item)

            spinner.register_observer(self)
            self.spinners.append(spinner)

            self.texts.append(
                Text("Player " + str(num + 1) + ": ", self.font, (xpos, ypos))
            )

        tuto_lines = (
            "How to play:",
            "LEFT click to select land/attack, RIGHT click to end turn",
            "First, select a land you own that has two or more dices on it.",
            "Second, pick an enemy adjacent land (of different color) to attack it!"
        )
        linespacing = 25  # px
        for k in range(4):
            tmp_txt_label = Text(tuto_lines[k], self.font, (10, 425 + k * linespacing))
            self.texts.append(tmp_txt_label)

        # - les composants de la vue écoutent eux aussi...
        #for spinner in self.spinners:
        #    events.RootEventSource.instance().add_listener(spinner)

        # déjà actifs de base
        #for button in self.buttons:
        #    events.RootEventSource.instance().add_listener(button)

        # - la preview
        self._preview = None
        self.refresh_map_preview()

    def _do_dump_map(self):
        serial = glvars.world.serialize()
        # - profitions-en pour sync le serial sur le serveur
        # - on détermine que par convention, c'est le joueur 0 qui cree la partie
        lemsg = 'tom/push_map.php'
        ev = CgmEvent(EngineEvTypes.ASYNCSEND, num=NETW_PUSH_MAP_TOPO, msg=lemsg, data=serial)
        print('tryin to post async...(button clicked)')
        self._manager.post(ev)

    def turn_on(self):
        for b in self.buttons:
            b.turn_on()
        for s in self.spinners:
            s.turn_on()
        super().turn_on()

    def turn_off(self):
        for b in self.buttons:
            b.turn_off()
        for s in self.spinners:
            s.turn_off()
        super().turn_off()

    def notify(self, subject):
        """
        le spinner (choix du nb de joueurs) agit en retour sur cette vue-là
        """

        # print "notify from: ", subject, " value: ", subject.get_current_value()

        if subject == self.netw_id_spinner:
            # - debug
            # print('netw_id_spinner actionné...')
            glvars.local_pid = self.netw_id_spinner.get_current_value()

        elif subject == self.spinners[0]:  # équivaut à un changement du nb de joueurs...

            if len(self.spinners)-1 > subject.get_current_value():
                spinner = self.spinners.pop()
                spinner.remove_observer(self)
                spinner.turn_off()

                # events.RootEventSource.instance().remove_listener(spinner)
                self.texts.pop()
                self.ref_mod.decrease_players()

            elif len(self.spinners)-1 < subject.get_current_value():
                # add new spinner for player
                xpos, ypos = self.spinners[-1].position
                spinner = Spinner(self.font, (xpos, ypos + 30))

                for item in self.items:
                    spinner.add(item)
                # events.RootEventSource.instance().add_listener(spinner)

                spinner.register_observer(self)
                spinner.turn_on()
                self.spinners.append(spinner)
                self.texts.append(Text("Player " + str(len(self.spinners) - 1) +\
                                    ": ", self.font, (xpos - 100, ypos + 30)))
                self.ref_mod.increase_players()

        else:
            # print('spinner op captée par view')
            indx = None
            for k in range(len(self.spinners)):
                if self.spinners[k] == subject:
                    indx = k
                    break
            #
            print('spinner {} change valeur, val= {}'.format(indx, subject.get_current_value()))
            glvars.player_infos[indx - 1] = subject.get_current_value()

    def sig_wanna_quit(self):
        self._manager.post(CgmEvent(PygameBridge.QUIT))

    def sig_wanna_start(self):
        self.do_start()

    def do_start(self):
        print('[do_start() method] appelée sur classe MenuOptionsView')
        print(
            'nb joueurs={} / nb info sur joueurs {}'.format(len(glvars.players), len(glvars.player_infos))
        )

        # revert players to player type
        for index, player in enumerate(glvars.players):
            val = self.spinners[index + 1].get_current_value()
            player.set_player_type(val)
            print('idx[{}]  type->  {}'.format(index, val))

        evt_pushstate = CgmEvent(EngineEvTypes.PUSHSTATE, state_ident=GameStates.Conquest)
        self._manager.post(evt_pushstate)

    def on_paint(self, ev):
        screen = cgmconf.get_screen()
        screen.fill(self.bg_color)

        for button in self.buttons:
            screen.blit(button.image, button.position)

        for spinner in self.spinners:
            screen.blit(spinner.image, spinner.position)
        screen.blit(self.netw_id_spinner.image, self.netw_id_spinner.position)

        for text in self.texts:
            screen.blit(text.image, text.position)

        screen.blit(self._preview, (20, 20))

    def on_map_change(self, event):
        print('MAPCHANGES capté par la vue')
        self.refresh_map_preview()

    def refresh_map_preview(self, zoom=0.6):
        own = GlobOwnershipLands.instance()
        # self._preview = pygame.Surface((0, 0))
        # self._preview.fill((255, 255, 220))

        preview_img_size = glvars.world.grid.get_size()
        map_img = pygame.Surface(preview_img_size)#.convert()
        # map_img.fill((0x80, 0x00, 0x80))
        colorkey = img_helper.get_t_colorkey()
        map_img.fill(colorkey)

        # tom: essai sans fill ca donne quoi?
        # map_img.fill((0x80, 0x00, 0x80))  # fill with color_key

        # color for each player (actually an index)
        idx = 0
        player_color = {}
        for refplayer in glvars.players:
            player_color[refplayer.get_pid()] = idx
            idx += 1

        # load tiles
        tiles = []
        for elt in img_helper.filenames_4tiles():
            img = pygame.image.load(elt).convert()
            img.set_colorkey(img_helper.get_t_colorkey())
            tiles.append(img)

        grid_toabs = glvars.world.grid.grid_to_abs
        for land in glvars.world.get_lands():
            for cell in land.cells:
                if land.selected:
                    map_img.blit(tiles[-1], grid_toabs(cell))
                else:
                    owner_code = own[land.get_id()]
                    idx = player_color[owner_code]

                    blitx, blity = grid_toabs(cell)
                    blitx -= glvars.world.grid.offset_x
                    blity -= glvars.world.grid.offset_y
                    map_img.blit(tiles[idx], (blitx, blity))

        # load borders images
        borders = []
        for elt in img_helper.filenames_4borders():
            img = pygame.image.load(elt).convert()
            img.set_colorkey(img_helper.get_t_colorkey())
            borders.append(img)

        # draw borders
        num_cells = glvars.world.grid.get_num_cells()
        for posy in range(num_cells[1]):
            for posx in range(num_cells[0]):
                cell_land = glvars.world.cells[(posx, posy)]
                # get adj cells
                adj_cells = glvars.world.grid.get_adj_cells((posx, posy), True)
                # calculate position to blit
                blitx, blity = glvars.world.grid.grid_to_abs((posx, posy))
                # TODO: hack!!
                blitx -= glvars.world.grid.offset_x
                blity -= glvars.world.grid.offset_y
                # go through adj and check if they are from a different land
                for idx, adjcell in enumerate(adj_cells):
                    # check if cell is on map
                    if adjcell in glvars.world.cells:
                        if cell_land != glvars.world.cells[adjcell]:
                            map_img.blit(borders[idx], (blitx, blity))
                    else:
                        if cell_land:
                            map_img.blit(borders[idx], (blitx, blity))

        # save result
        # map_img = pygame.transform.rotozoom(map_img, 0, zoom).convert()
        # map_img.set_colorkey((0x80, 0x00, 0x80))

        targ_size = int(zoom*preview_img_size[0]), int(zoom*preview_img_size[1])
        print('target size')
        print(targ_size)

        self._preview = pygame.transform.scale(map_img, targ_size)
        self._preview.set_colorkey(colorkey)
