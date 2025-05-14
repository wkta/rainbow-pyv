import random
from itertools import repeat
import glvars
from modules.muda import load_img, Scene, draw_background, shake, image_at, scale_rect, draw_hpbar
from modules.spawner import Spawner
from modules.sprites import Player
from modules.widgets import *
from .scenes import GameOverScene
import XInput

class GameScene(Scene):
    def __init__(self, P_Prefs):
        # Player Preferences
        self.P_Prefs = P_Prefs
        self.vibrate_delay = 0

        # SCENE DEFINES
        self.g_diff = DIFFICULTIES[self.P_Prefs.game_difficulty]
        self.score = 0
        self.score_multiplier = SCORE_MULTIPLIER[self.g_diff]
        self.win_offset = repeat((0, 0))
        self.hp_pref = HP_OPTIONS[self.P_Prefs.hp_pref]
        self.gg_timer = get_ticks()
        self.gg_delay = 3000
        self.is_gg = False
        self.can_pause = self.P_Prefs.can_pause
        self.paused = False

        # PLAYER AND BULLET IMAGES - If you are reading this...uhh...good luck lol
        PLAYER_SPRITESHEET = load_img("player_sheet.png", IMG_DIR, SCALE)
        PLAYER_IMGS = {
            "SPAWNING": [
                image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0, 144, 16, 16]), True),
                image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16, 144, 16, 16]), True),
                image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32, 144, 16, 16]), True),
                image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48, 144, 16, 16]), True)
            ],
            "NORMAL": {
                "LV1": {
                    "FORWARD": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0, 0, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16, 0, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32, 0, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48, 0, 16, 16]), True)
                    ],
                    "LEFT": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0, 16, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16, 16, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32, 16, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48, 16, 16, 16]), True)
                    ],
                    "RIGHT": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0, 32, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16, 32, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32, 32, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48, 32, 16, 16]), True)
                    ]
                },
                "LV2": {
                    "FORWARD": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0, 48, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16, 48, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32, 48, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48, 48, 16, 16]), True)
                    ],
                    "LEFT": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0, 64, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16, 64, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32, 64, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48, 64, 16, 16]), True)
                    ],
                    "RIGHT": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0, 80, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16, 80, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32, 80, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48, 80, 16, 16]), True)
                    ]
                },
                "LV3": {
                    "FORWARD": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0, 96, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16, 96, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32, 96, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48, 96, 16, 16]), True)
                    ],
                    "LEFT": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0, 112, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16, 112, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32, 112, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48, 112, 16, 16]), True)
                    ],
                    "RIGHT": [
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0, 128, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16, 128, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32, 128, 16, 16]), True),
                        image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48, 128, 16, 16]), True)
                    ]
                }
            },
            "LEVELUP": {
                "1-2": [
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0, 160, 16, 16]), True),
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16, 160, 16, 16]), True),
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32, 160, 16, 16]), True),
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48, 160, 16, 16]), True)
                ],
                "2-3": [
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [0, 176, 16, 16]), True),
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [16, 176, 16, 16]), True),
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [32, 176, 16, 16]), True),
                    image_at(PLAYER_SPRITESHEET, scale_rect(SCALE, [48, 176, 16, 16]), True)
                ]
            }
        }
        BULLET_SPRITESHEET = load_img("bullet_sheet.png", IMG_DIR, SCALE)
        BULLET_IMG = image_at(BULLET_SPRITESHEET, scale_rect(SCALE, [16, 0, 8, 8]), True)

        # BG AND PARALLAX IMAGES & DEFINES
        self.BG_IMG = load_img("background.png", IMG_DIR, SCALE)
        self.bg_rect = self.BG_IMG.get_rect()
        self.bg_y = 0
        self.PAR_IMG = load_img("background_parallax.png", IMG_DIR, SCALE)
        self.par_rect = self.BG_IMG.get_rect()
        self.par_y = 0

        # HP Bar Image
        self.hp_surf = pygame.Surface((128, 16))
        self.hpbar_outline = load_img("hpbar_outline.png", IMG_DIR, SCALE)
        self.hpbar_color = load_img("hpbar_color.png", IMG_DIR, SCALE)

        # HP Pie Image
        PIE_SHEET = load_img("hppie_sheet.png", IMG_DIR, SCALE)  # It's not a sheet for hippies
        self.pie_surf = pygame.Surface((32, 32))
        self.pie_health = image_at(PIE_SHEET, scale_rect(SCALE, [0, 0, 16, 16]), True)
        self.pie_outline = image_at(PIE_SHEET, scale_rect(SCALE, [16, 0, 16, 16]), True)
        self.pie_rect = self.pie_surf.get_rect()
        self.pie_rect.x = WIN_RES["w"] * 0.77
        self.pie_rect.y = 4

        # Difficulty icons
        DIFFICULTY_SPRITESHEET = load_img("difficulty_sheet.png", IMG_DIR, SCALE)
        self.DIFFICULTY_ICONS = {
            "EASY": {
                "EARLY": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [0, 0, 16, 16]), True),
                "MID": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [16, 0, 16, 16]), True),
                "LATE": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [32, 0, 16, 16]), True)
            },
            "MEDIUM": {
                "EARLY": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [0, 16, 16, 16]), True),
                "MID": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [16, 16, 16, 16]), True),
                "LATE": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [32, 16, 16, 16]), True)
            },
            "HARD": {
                "EARLY": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [0, 32, 16, 16]), True),
                "MID": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [16, 32, 16, 16]), True),
                "LATE": image_at(DIFFICULTY_SPRITESHEET, scale_rect(SCALE, [32, 32, 16, 16]), True)
            }
        }
        self.difficulty_icon = pygame.Surface((32, 32))

        # Clear the sprite groups
        all_sprites_g.empty()
        hostiles_g.empty()
        p_bullets_g.empty()
        powerups_g.empty()
        e_bullets_g.empty()
        sentries_g.empty()
        hellfighters_g.empty()

        # Initialize the player
        self.player = Player(PLAYER_IMGS, BULLET_IMG, self.P_Prefs)
        all_sprites_g.add(self.player)

        # Create a spawner
        self.spawner = Spawner(self.player, self.g_diff)

        # Exit progress bar
        self.exit_bar = pygame.Surface((32, 32))
        self.exit_timer = kataen.import_pygame().time.get_ticks()
        self.exit_delay = 2000
        self.is_exiting = False
        self.timer_resetted = False

        # Killfeed
        self.scorefeed = Scorefeed()

        # Sounds
        self.sfx_explosions = [
            load_sound("sfx_explosion1.wav", SFX_DIR, self.P_Prefs.sfx_vol),
            load_sound("sfx_explosion2.wav", SFX_DIR, self.P_Prefs.sfx_vol),
            load_sound("sfx_explosion3.wav", SFX_DIR, self.P_Prefs.sfx_vol)
        ]
        self.sfx_hits = [
            load_sound("sfx_hit1.wav", SFX_DIR, self.P_Prefs.sfx_vol),
            load_sound("sfx_hit2.wav", SFX_DIR, self.P_Prefs.sfx_vol),
            load_sound("sfx_hit3.wav", SFX_DIR, self.P_Prefs.sfx_vol)
        ]
        self.sfx_powerup_gun = load_sound("sfx_powerup_gun.wav", SFX_DIR, self.P_Prefs.sfx_vol)
        self.sfx_powerup_hp = load_sound("sfx_powerup_hp.wav", SFX_DIR, self.P_Prefs.sfx_vol)
        self.sfx_powerup_coin = load_sound("sfx_powerup_coin.wav", SFX_DIR, self.P_Prefs.sfx_vol)
        self.sfx_powerup_sentry = load_sound("sfx_powerup_sentry.wav", SFX_DIR, self.P_Prefs.sfx_vol)

    def handle_events(self, events):
        for event in events:
            # ------ ajout 18/11 (joystick) ----
            if event.type == pygame.JOYAXISMOTION:
                glvars.jhandler[event.joy].axis[event.axis] = event.value

            elif event.type == pygame.JOYBALLMOTION:
                glvars.jhandler[event.joy].ball[event.ball] = event.rel

            elif event.type == pygame.JOYHATMOTION:
                glvars.jhandler[event.joy].hat[event.hat] = event.value

            elif event.type == pygame.JOYBUTTONUP:
                glvars.jhandler[event.joy].button[event.button] = 0
                print('button<-0 :', event.button)

            elif event.type == pygame.JOYBUTTONDOWN:
                glvars.jhandler[event.joy].button[event.button] = 1
                print('button<-1 :', event.button)

            # --------------- fin joystick

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l and DEBUG_MODE:
                    self.player.gun_level += 1

                if self.can_pause and not self.is_gg:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused  # Dirty toggling hack

                    if event.key == pygame.K_x and self.paused:
                        self.manager.go_to(glvars.title_scene)

        if not self.is_gg and not self.can_pause:
            pressed = pygame.key.get_pressed()
            if pressed[self.P_Prefs.key_back] or pressed[pygame.K_ESCAPE]:
                self.is_exiting = True
                if self.timer_resetted == False:
                    self.exit_timer = get_ticks()
                    self.timer_resetted = True
            else:
                self.is_exiting = False
                self.timer_resetted = False

        self.spawner.handle_events(events)

    def update(self, dt):
        if self.vibrate_delay < 0:
            self.vibrate_delay += dt
            if self.vibrate_delay >= 0:
                XInput.set_vibration(0, 0, 0)

        if not self.paused:
            # Update parallax and background
            self.bg_y += BG_SPD * dt
            self.par_y += PAR_SPD * dt

            # Exit progress
            if self.is_exiting:
                now = get_ticks()
                if now - self.exit_timer > self.exit_delay:
                    self.player.health -= PLAYER_HEALTH * 999
                    self.win_offset = shake(30, 5)
                    self.is_exiting = False

            # Collisions
            if not self.is_gg:
                self._handle_collisions()

            # END GAME IF PLAYER HAS LESS THAN 0 HEALTH
            if self.player.health <= 0 and not self.is_gg:
                # Play sound
                random.choice(self.sfx_explosions).play()

                # Spawn big explosion on player
                bullet_x = self.player.rect.centerx
                bullet_y = self.player.rect.centery
                bullet_pos = Vec2(bullet_x, bullet_y)
                self.spawner.spawn_explosion(bullet_pos, "BIG")
                self.vibrate_delay = -0.8
                XInput.set_vibration(0, 0.7, 0.7)


                # Spawn explosion particles
                self.spawner.spawn_exp_particles(
                    (self.player.rect.centerx, self.player.rect.centery),
                    (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                    100
                )

                # Generate screen shake
                self.win_offset = shake(30, 5)

                # Set to game over
                self.player.kill()
                self.is_gg = True
                self.gg_timer = get_ticks()

            # Transition to game over scene if game is over
            if self.is_gg:
                now = get_ticks()
                if now - self.gg_timer > self.gg_delay:
                    self.P_Prefs.score = self.score
                    self.manager.go_to(GameOverScene(self.P_Prefs))

            self.spawner.update(self.score)
            self.scorefeed.update()
            all_sprites_g.update(dt)

    def draw(self, window):
        if not self.paused:
            # Draw background
            draw_background(window, self.BG_IMG, self.bg_rect, self.bg_y)
            draw_background(window, self.PAR_IMG, self.par_rect, self.par_y)

            # Draw sprites
            all_sprites_g.draw(window)

            # Draw score feed
            self.scorefeed.draw(window)

            # Draw exit progress
            self._draw_exitprogress(window)

            # Draw score
            cur_score = str(int(self.score)).zfill(6)
            draw_text2(window, f"{cur_score}", GAME_FONT, int(FONT_SIZE * 1.4), (12, 10), HP_RED2, italic=True)
            draw_text2(window, f"{cur_score}", GAME_FONT, int(FONT_SIZE * 1.4), (12, 8), "white", italic=True)

            # Draw hp bar
            self._draw_hpbar(window)

            # Draw difficulty icon
            self.difficulty_icon = self.DIFFICULTY_ICONS[self.g_diff][self.spawner.current_stage]
            window.blit(self.difficulty_icon, (window.get_width() * 0.885, 4))

            if self.is_gg:
                draw_text2(
                    window,
                    "GAME OVER",
                    GAME_FONT,
                    int(FONT_SIZE * 3),
                    (window.get_width() / 2, window.get_height() * 0.4),
                    "white",
                    italic=True,
                    align="center"
                )

            # Draw debug text
            self._draw_debugtext(window)
        else:
            self._draw_pausetext(window)

    def _handle_collisions(self):
        # Call collision functions
        self._hostile_playerbullet_collide()
        self._player_enemybullet_collide()
        self._player_enemy_collide()
        self._player_powerup_collide()
        self._player_enemy_collide()
        self._sentry_enemy_collide()
        self._sentry_enemybullet_collide()

    def _hostile_playerbullet_collide(self):
        # HOSTILES - PLAYER BULLET COLLISION
        for bullet in p_bullets_g:
            hits = pygame.sprite.spritecollide(bullet, hostiles_g, False, pygame.sprite.collide_circle)
            for hit in hits:
                # Play sound
                random.choice(self.sfx_hits).play()

                # Deduct enemy health
                hit.health -= self.player.BULLET_DAMAGE

                # Spawn small explosion
                bullet_x = bullet.rect.centerx
                bullet_y = bullet.rect.centery
                bullet_pos = Vec2(bullet_x, bullet_y)
                self.spawner.spawn_explosion(bullet_pos, "SMALL")

                # Spawn explosion particles
                self.spawner.spawn_exp_particles(
                    (hit.rect.centerx, hit.rect.centery),
                    (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                    3
                )

                # Set boolean to True for flash effect
                hit.is_hurt = True

                # Kill bullet
                bullet.kill()

                # Logic if enemy is dead
                if hit.health <= 0:
                    # Play sound
                    random.choice(self.sfx_explosions).play()

                    # Kill sprite
                    hit.kill()

                    # Add score
                    score_worth = hit.WORTH * self.score_multiplier
                    self.score += score_worth
                    self.scorefeed.add(score_worth)

                    # Spawn powerup
                    spawn_roll = random.randrange(1, 100)
                    if spawn_roll <= POWERUP_ROLL_CHANCE[self.g_diff]:
                        self.spawner.spawn_powerup(hit.position)

                    # Spawn big explosion
                    bullet_x = hit.rect.centerx
                    bullet_y = hit.rect.centery
                    bullet_pos = Vec2(bullet_x, bullet_y)
                    self.spawner.spawn_explosion(bullet_pos, "BIG")

                    # Spawn explosion particles
                    self.spawner.spawn_exp_particles(
                        (hit.rect.centerx, hit.rect.centery),
                        (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                        30
                    )

                    # Generate screen shake
                    self.win_offset = shake(10, 5)

    def _player_enemybullet_collide(self):
        # PLAYER - ENEMY BULLET COLLISION
        hits = pygame.sprite.spritecollide(self.player, e_bullets_g, True, pygame.sprite.collide_circle)
        if len(hits):
            self.vibrate_delay = -0.25
            XInput.set_vibration(0, 0.2, 0.2)

        for hit in hits:
            # Play sound
            random.choice(self.sfx_hits).play()

            # Damage player
            self.player.health -= hit.DAMAGE

            # Spawn small explosion
            bullet_x = hit.rect.centerx
            bullet_y = hit.rect.centery
            bullet_pos = Vec2(bullet_x, bullet_y)
            self.spawner.spawn_explosion(bullet_pos, "SMALL")

            # Spawn explosion particles
            self.spawner.spawn_exp_particles(
                (hit.rect.centerx, hit.rect.centery),
                (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                5
            )

            # Generate screen shake
            self.win_offset = shake(10, 5)

            # Hurt player
            self.player.is_hurt = True

    def _player_enemy_collide(self):
        # PLAYER - ENEMY COLLISION
        hits = pygame.sprite.spritecollide(self.player, hostiles_g, True, pygame.sprite.collide_circle)
        if len(hits):
            self.vibrate_delay = -0.5
            XInput.set_vibration(0, 0.44, 0.44)

        for hit in hits:
            # Play sound
            random.choice(self.sfx_explosions).play()

            self.player.health -= ENEMY_COLLISION_DAMAGE

            # Spawn big explosion on player
            bullet_x = self.player.rect.centerx
            bullet_y = self.player.rect.centery
            bullet_pos = Vec2(bullet_x, bullet_y)
            self.spawner.spawn_explosion(bullet_pos, "BIG")

            # Spawn big explosion on hit
            bullet_x = hit.rect.centerx
            bullet_y = hit.rect.centery
            bullet_pos = Vec2(bullet_x, bullet_y)
            self.spawner.spawn_explosion(bullet_pos, "BIG")

            # Spawn explosion particles
            self.spawner.spawn_exp_particles(
                (hit.rect.centerx, hit.rect.centery),
                EP_COLORS,
                30
            )

            # Generate screen shake
            self.win_offset = shake(20, 5)

            hit.kill()

    def _player_powerup_collide(self):
        # PLAYER - POWERUP COLLISION
        hits = pygame.sprite.spritecollide(self.player, powerups_g, True)
        for hit in hits:
            particles_color = ((255, 255, 255))  # Default case
            if hit.POW_TYPE == "GUN":
                # Play sound
                self.sfx_powerup_gun.play()

                # Gun level limit check / increase
                if self.player.gun_level >= PLAYER_MAX_GUN_LEVEL:
                    self.player.gun_level = 3
                else:
                    self.player.gun_level += 1

                # Set particle colors
                particles_color = GP_COLORS

            elif hit.POW_TYPE == "HEALTH":
                # Play sound
                self.sfx_powerup_hp.play()

                self.player.health += POWERUP_HEALTH_AMOUNT[self.g_diff]
                if self.player.health >= PLAYER_MAX_HEALTH:
                    self.player.health = PLAYER_MAX_HEALTH
                # Set particle colors
                particles_color = HP_COLORS

            elif hit.POW_TYPE == "SCORE":
                # Play sound
                self.sfx_powerup_coin.play()

                # Add score
                p_score = POWERUP_SCORE_BASE_WORTH * self.score_multiplier
                self.score += p_score
                self.scorefeed.add(p_score)

                # Set particle colors
                particles_color = SCR_COLORS

            elif hit.POW_TYPE == "SENTRY":
                # Play sound
                self.sfx_powerup_sentry.play()

                # Spawn sentry
                self.spawner.spawn_sentry()

                # Set particle colors
                particles_color = SP_COLORS

            # Spawn explosion particles
            self.spawner.spawn_exp_particles(
                (hit.rect.centerx, hit.rect.centery),
                particles_color,
                30
            )

            # Produce a flashing effect
            # The player is not really hurt, the variable is just named that way because I was stupid
            # enough not to foresee other uses...now im too lazy to change it.
            self.player.is_hurt = True

    def _sentry_enemy_collide(self):
        # SENTRY - ENEMY COLLISION
        for sentry in sentries_g:
            hits = pygame.sprite.spritecollide(sentry, hostiles_g, False, pygame.sprite.collide_circle)
            for hit in hits:
                # Play sound
                random.choice(self.sfx_explosions).play()

                sentry.kill()
                hit.kill()

                # Spawn big explosion on sentry
                bullet_x = sentry.rect.centerx
                bullet_y = sentry.rect.centery
                bullet_pos = Vec2(bullet_x, bullet_y)
                self.spawner.spawn_explosion(bullet_pos, "BIG")

                # Spawn big explosion on hit
                bullet_x = hit.rect.centerx
                bullet_y = hit.rect.centery
                bullet_pos = Vec2(bullet_x, bullet_y)
                self.spawner.spawn_explosion(bullet_pos, "BIG")

                # Spawn explosion particles
                self.spawner.spawn_exp_particles(
                    (hit.rect.centerx, hit.rect.centery),
                    (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                    30
                )

    def _sentry_enemybullet_collide(self):
        # SENTRY - ENEMY BULLET COLLISION
        for sentry in sentries_g:
            hits = pygame.sprite.spritecollide(sentry, e_bullets_g, True, pygame.sprite.collide_circle)

            for hit in hits:
                # Play sound
                random.choice(self.sfx_hits).play()

                # Deduct sentry health
                sentry.health -= hit.DAMAGE

                # Set boolean to True for flash effect
                sentry.is_hurt = True

                # Spawn small explosion
                bullet_x = hit.rect.centerx
                bullet_y = hit.rect.centery
                bullet_pos = Vec2(bullet_x, bullet_y)
                self.spawner.spawn_explosion(bullet_pos, "SMALL")

                # Spawn explosion particles
                self.spawner.spawn_exp_particles(
                    (hit.rect.centerx, hit.rect.centery),
                    (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                    5
                )

                if sentry.health <= 0:
                    # Play sound
                    random.choice(self.sfx_explosions).play()

                    # Spawn big explosion
                    bullet_x = sentry.rect.centerx
                    bullet_y = sentry.rect.centery
                    bullet_pos = Vec2(bullet_x, bullet_y)
                    self.spawner.spawn_explosion(bullet_pos, "BIG")

                    # Spawn explosion particles
                    self.spawner.spawn_exp_particles(
                        (sentry.rect.centerx, sentry.rect.centery),
                        (EP_YELLOW1, EP_YELLOW2, EP_YELLOW3),
                        30
                    )

                    sentry.kill()

    def _draw_exitprogress(self, window):
        if self.is_exiting:
            now = get_ticks()
            bar_length = int((now - self.exit_timer) / 8)
            bar_color = "white"
            if now - self.exit_timer > self.exit_delay / 2:
                bar_color = HP_RED1
            self.exit_bar = pygame.Surface((bar_length, 16))
            self.exit_bar.fill(bar_color)
            draw_text2(
                self.exit_bar,
                "EXITING",
                GAME_FONT,
                FONT_SIZE,
                (self.exit_bar.get_width() / 2, 0),
                "black",
                align="center"
            )
            window.blit(
                self.exit_bar,
                (window.get_width() / 2 - self.exit_bar.get_width() / 2, window.get_height() / 2)
            )

    def _draw_hpbar(self, window):
        if True:  # self.hp_pref == HP_OPTIONS[1]:
            # Draw square hp bar
            self.hp_surf.fill("black")
            self.hp_surf.set_colorkey("black")
            draw_hpbar(self.hp_surf, self.hpbar_color, (4, 4, 96, 8), self.player.health, "white")
            self.hp_surf.blit(self.hpbar_outline, (0, 0))
            window.blit(self.hp_surf,
                        (
                            (window.get_width() / 2) - 38,
                            10
                        )
                        )

        # elif self.hp_pref == HP_OPTIONS[0]:
        #     # Draw circle hp bar
        #     semicirc_size = 32
        #     semicirc_end = 360 - (self.player.health * (360 / PLAYER_MAX_HEALTH)) + 270
        #     semicirc = Image.new("RGBA", (semicirc_size, semicirc_size))
        #     semicirc_d = ImageDraw.Draw(semicirc)
        #     semicirc_d.pieslice((0, 0, semicirc_size-1, semicirc_size-1), 271, semicirc_end + 1, fill="black")
        #     semicirc_surf = pygame.image.fromstring(semicirc.tobytes(), semicirc.size, semicirc.mode)
        #
        #     self.pie_surf.fill("black")
        #     self.pie_surf.set_colorkey("black")
        #     self.pie_surf.blit(self.pie_health, (0,0))
        #     self.pie_surf.blit(semicirc_surf, (0,0))
        #     self.pie_surf.blit(self.pie_outline, (0,0))
        #     window.blit(self.pie_surf,
        #         (
        #             window.get_width()/2,
        #             4
        #         )
        #     )

    def _draw_debugtext(self, window):
        # Debug mode stats
        if DEBUG_MODE:
            draw_text(window, f"{int(self.score)}", FONT_SIZE, GAME_FONT, 48, 8, "white", "centered")
            draw_text(window, f"HP: {int(self.player.health)}", FONT_SIZE, GAME_FONT, 48, 16 + FONT_SIZE, "white",
                      "centered")
            draw_text(window, f"STAGE: {self.spawner.current_stage}", FONT_SIZE, GAME_FONT, 48, 32 + FONT_SIZE, "white")
            draw_text(window, f"DIFF: {self.g_diff}", FONT_SIZE, GAME_FONT, 48, 64 + FONT_SIZE, "white", )

        window.blit(window, next(self.win_offset))

    def _draw_pausetext(self, window):
        draw_text2(
            window,
            "PAUSED",
            GAME_FONT,
            int(FONT_SIZE * 3),
            (window.get_width() / 2, window.get_height() * 0.4),
            "white",
            italic=True,
            align="center"
        )
        draw_text2(
            window,
            "ESC to Resume",
            GAME_FONT,
            int(FONT_SIZE * 2),
            (window.get_width() / 2, window.get_height() * 0.5),
            "white",
            align="center"
        )
        draw_text2(
            window,
            "X to Exit",
            GAME_FONT,
            int(FONT_SIZE * 2),
            (window.get_width() / 2, window.get_height() * 0.55),
            "white",
            align="center"
        )
