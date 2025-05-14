import game_defs
import glvars
# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi


pygame = kengi.pygame
EventReceiver = kengi.event.EventReceiver
EngineEvTypes = kengi.event.EngineEvTypes


# Nota Bene.
# there will be no model for the collection, as the avatar already contains it!
# (in glvars.the_avatar.artifacts)

BASE_Y = 55

TAQUET_X = 50


class ShowCollectionView(EventReceiver):
    """
    dummy view,
    displays a gray square(=slot) no matter what,
    +displays a steelblue circle inside this slot if the artifact is owned
    """
    def __init__(self):
        super().__init__()
        self.reagent_names_lbl = list()
        ft = pygame.font.Font(None, 25)
        for ac in game_defs.ArtifactCodes.all_codes:
            self.reagent_names_lbl.append(
                ft.render(game_defs.ArtifactNames[ac][0], True, (87, 11, 128))
            )

        self.rituals_title_lbl = ft.render('Rituals: ', True, (87, 11, 128))

        self.ritual_spr = pygame.sprite.Sprite()
        self.ritual_spr.image = pygame.image.load('assets/ritual.png')
        self.ritual_spr.rect = self.ritual_spr.image.get_rect()
        self.ritual_spr.rect.center = (180, 434)

        self.chalice_spr = pygame.sprite.Sprite()
        self.chalice_spr.image = pygame.transform.scale(pygame.image.load('assets/chalice.png'), (150, 150))
        self.chalice_spr.image.set_colorkey((255, 0, 255))
        self.chalice_spr.rect = self.chalice_spr.image.get_rect()
        self.chalice_spr.rect.center = (385, 434)

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            self._do_paint(ev.screen)

    def _do_paint(self, scr):
        scr.fill(game_defs.BG_COLOR)

        ft = pygame.font.Font(None, 27)
        av = glvars.the_avatar

        # - draw labels
        given_y = BASE_Y
        for lbl in self.reagent_names_lbl:
            scr.blit(lbl, (TAQUET_X, given_y-32))
            given_y += 88

        # - draw slots
        given_y = BASE_Y
        circle_offset = [40, 25]
        rad = 21
        for art_code in game_defs.ArtifactCodes.all_codes:
            tmp = max(game_defs.ArtifactNames[art_code].keys())
            for num_piece in range(1, tmp+1):  # draw smth for each artifact element
                tmpx = 50+(num_piece-1)*125
                pygame.draw.rect(scr, 'darkgray', (tmpx, given_y, 80, 50))
                if av.has_artifact(art_code, num_piece):
                    tpos = (tmpx+circle_offset[0], given_y+circle_offset[1])
                    pygame.draw.circle(scr, 'steelblue', tpos, rad)

                    # also display the quantity...
                    tmp = ft.render(str(av.artifact_quant(art_code, num_piece)), False, 'orange')
                    scr.blit(tmp, (tpos[0], tpos[1]+16))
            given_y += 88

        # titre partie 2 +illustrations
        scr.blit(self.rituals_title_lbl, (TAQUET_X, 33 + scr.get_size()[1]//2))
        scr.blit(self.ritual_spr.image, self.ritual_spr.rect.topleft)
        scr.blit(self.chalice_spr.image, self.chalice_spr.rect.topleft)


class ShowCollectionCtrl(EventReceiver):
    def proc_event(self, ev, source):
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            self.pev(EngineEvTypes.POPSTATE)


class MageryState(kengi.BaseGameState):
    def __init__(self, gs_id):
        super().__init__(gs_id)
        self.m = self.v = self.c = None

    def enter(self):
        self.v = ShowCollectionView()
        self.v.turn_on()
        self.c = ShowCollectionCtrl()
        self.c.turn_on()

    def release(self):
        self.c.turn_off()
        self.v.turn_off()
        self.c = self.v = None
