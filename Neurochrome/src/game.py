from pygame import mixer

from level import Level
from menu import *
from settings import *
from ui import UI


class Game:
    def __init__(self):
        pygame.init()
        # sound
        mixer.init()
        pygame.mixer.music.load('audio/Detox.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1, 0.2, 5000)

        self.landing_fx = pygame.mixer.Sound('audio/sfx/landing_grunt.wav')
        self.landing_fx.set_volume(0.2)
        self.melee_fx = pygame.mixer.Sound('audio/sfx/woosh.wav')
        self.melee_fx.set_volume(0.2)
        self.save_fx = pygame.mixer.Sound('audio/sfx/save.wav')
        self.save_fx.set_volume(0.2)
        self.blaster_fx = pygame.mixer.Sound('audio/sfx/blaster.wav')
        self.blaster_fx.set_volume(0.3)
        self.railgun_fx = pygame.mixer.Sound('audio/sfx/railgun.wav')
        self.railgun_fx.set_volume(0.3)
        self.collect_fx = pygame.mixer.Sound('audio/sfx/collect.wav')
        self.collect_fx.set_volume(0.3)
        self.neobit_fx = pygame.mixer.Sound('audio/sfx/neobit.wav')
        self.neobit_fx.set_volume(0.2)
        self.jetpack_fx = pygame.mixer.Sound('audio/sfx/engine.wav')
        self.jetpack_fx.set_volume(0.2)
        self.load_fx = pygame.mixer.Sound('audio/sfx/load.wav')
        self.load_fx.set_volume(0.3)
        self.unload_fx = pygame.mixer.Sound('audio/sfx/unload.wav')
        self.unload_fx.set_volume(0.3)
        self.double_jump_fx = pygame.mixer.Sound('audio/sfx/electroshot.wav')
        self.double_jump_fx.set_volume(0.5)

        with open('settings.json', 'r') as fp:
            settings_json_content = json.load(fp)
            self.max_health = settings_json_content['max_health']
            self.max_fps = settings_json_content['max_fps']

        with open('gamesave.json', 'r') as json_file:
        	json_data = json.load(json_file)

        print(json_data)
        self.load_gun_data(json_data)
        self.load_pickup_data(json_data)
        self.load_map_data(json_data)
        self.load_extra_healths_data(json_data)

        self.running = True
        self.playing = False
        self.actions = {'left': False, 'right': False, 'up': False, 'down': False, 'return': False, 'back': False, 'm': False,
                        'space': False, 'tab': False, 'z': False, 'x': False, 'escape': False, 'l': False, 'd': False, 'i': False, 'y': False, 'n': False}

        self.display = pygame.Surface((WIDTH, HEIGHT))
        self.screen = pygame.display.set_mode(((WIDTH, HEIGHT)))

        self.font_name = 'font/failed attempt.ttf'
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.clock = pygame.time.Clock()

        # states
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.quit = QuitMenu(self)
        # temporarly disabled
        # self.reset = ResetMenu(self)
        self.level = Level(self, json_data['additional_data']['save_point'], 0, json_data['additional_data']['block_position'],
                           0, False, self.screen, self.create_level, self.update_neobits, self.update_health)

        self.current_menu = self.main_menu

        # constant player data
        if json_data:
            self.neobits = json_data['neobit_data']['neobits']
        else:
            self.neobits = 0

        # self.start_health = defs.MAX_HEALTH
        self.current_health = self.max_health
        self.ui = UI(self.screen)

    def update_neobits(self, amount):
        self.neobits += amount

    def update_health(self, max_health_increment, current_health_increment):
        self.max_health += max_health_increment
        self.current_health += current_health_increment

    def create_level(self, new_level, entry_pos, new_block_position, current_gun, gun_showing):
        self.level = Level(self, new_level, entry_pos, new_block_position, current_gun,
                           gun_showing, self.screen, self.create_level, self.update_neobits, self.update_health)
        self.level.gun_equipped()

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.level.player.alive and self.actions['up'] and not self.level.player.hold and not self.level.player.hovering and \
                    not (self.level.player.on_elevator and self.level.player.vel.x == 0) and not (self.level.player.going_up or self.level.player.going_down):
                self.level.player.jump()
            elif self.actions['space'] and self.level.player.alive:
                self.level.show_map()
            elif self.actions['tab']:
                self.level.player.change_gun()
                self.level.show_new_gun()
            elif self.actions['z'] and not self.level.player.hold:
                self.level.show_gun()
            elif self.actions['d']:
                self.level.player.dash()
            elif self.actions['i']:
                print('current health:', self.level.game.current_health)
            # 	self.level.show_inventory()
            if not self.level.player.alive:
                if self.actions['y']:
                    self.level.load_point()
                    self.neobits = 0
                    # self.max_health = load_data['max_health']
                    self.current_health = self.max_health
                elif self.actions['n']:
                    self.playing = False
                    self.level.load_point()

            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_neobits(self.neobits)

            if self.level.map_showing and self.actions['escape']:
                self.playing = False
                self.level.load_point()

            self.reset_keys()
            pygame.display.update()
            self.clock.tick(self.level.game.max_fps)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.level.load_point()
                self.quit_and_dump_data()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.actions['return'] = True
                if event.key == pygame.K_BACKSPACE:
                    self.actions['back'] = True
                if event.key == pygame.K_UP:
                    self.actions['up'] = True
                if event.key == pygame.K_DOWN:
                    self.actions['down'] = True
                if event.key == pygame.K_SPACE:
                    self.actions['space'] = True
                if event.key == pygame.K_TAB:
                    self.actions['tab'] = True
                if event.key == pygame.K_m:
                    self.actions['m'] = True
                if event.key == pygame.K_z:
                    self.actions['z'] = True
                if event.key == pygame.K_x:
                    self.actions['x'] = True
                if event.key == pygame.K_l:
                    self.actions['l'] = True
                if event.key == pygame.K_d:
                    self.actions['d'] = True
                if event.key == pygame.K_i:
                    self.actions['i'] = True
                if event.key == pygame.K_y:
                    self.actions['y'] = True
                if event.key == pygame.K_n:
                    self.actions['n'] = True
                if event.key == pygame.K_ESCAPE:
                    self.actions['escape'] = True

    def draw_text(self, text, size, pos):
        font = pygame.font.Font(self.font_name, size)
        text_surf = font.render(text, True, self.WHITE)
        text_rect = text_surf.get_rect(center=pos)
        self.display.blit(text_surf, text_rect)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def load_gun_data(self,json_data):
            gun_data.clear()
            gun_data.update(json_data['gun_data'])

    def load_pickup_data(self, json_data):
            pickup_data.clear()
            pickup_data.update(json_data['pickup_data'])

    def load_map_data(self,json_data):
            levels_visited.clear()
            levels_visited.update(json_data['map_data'])

    def load_extra_healths_data(self,json_data):
        extra_healths_collected.clear()
        extra_healths_collected.update(json_data['extra_healths_data'])

    def quit_and_dump_data(self):
        # (disabled by Tom)
        # TODO: check the utility of this dump
        all_data = {
			"gun_data": gun_data,
			"pickup_data": pickup_data,
			"map_data": levels_visited,
			"extra_healths_data": extra_healths_collected,
			"neobit_data": neobit_data,
			"health_data": health_data,
			"additional_data": {
				"save_point": self.current_level,
				"block_position": self.new_block_position,
				"current_gun": self.current_gun,
				"gun_showing": self.gun_showing
			}
		}
        
        with open('gamesave.json', 'w') as json_file:
            json.dump(all_data, json_file, indent=4)

        self.running = False
        self.playing = False
        self.current_menu.run_display = False


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.current_menu.display_menu()
        g.game_loop()
