import app.main_screen.gui_description as frame
# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi

from game_events import MyEvTypes


pygame = kengi.pygame
EngineEvTypes = kengi.event.EngineEvTypes
CgmEvent = kengi.event.CgmEvent
EventReceiver = kengi.event.EventReceiver


class ReprSingleMission:
    """
    full graphical representation, can draw itself
    """
    common_bg_image = None
    gray_bg_image = None

    def __init__(self, rank, screenwidth):  # expecting int 0-2 for rank
        if not (-1 < rank < 3):
            raise NotImplemented

        self.button = None  # linked externally

        cls = self.__class__
        if cls.common_bg_image is None:
            temp_img = pygame.image.load('assets/arche.png')
            cls.common_bg_image = pygame.transform.scale(temp_img, (168, 150))

            tmpii = pygame.image.load('assets/gray_arche.png')
            cls.gray_bg_image = pygame.transform.scale(tmpii, (168, 150))

        self.centerpos = frame.pos_missions[rank]
        self.gray = False

    def draw(self, screen):
        cls = self.__class__
        aw, ay = cls.common_bg_image.get_size()
        p = self.centerpos
        if self.gray:
            adhoc_img = cls.gray_bg_image
        else:
            adhoc_img = cls.common_bg_image
        screen.blit(adhoc_img, (p[0] - aw / 2, p[1] - ay / 2))


class MissionSetView(EventReceiver):

    def __init__(self, ref_mod):
        super().__init__(self)

        self._scr_size = kengi.get_surface().get_size()

        fixed_size = (72, 66)
        offsety_bt = 25

        self._repr_missions = list()
        for k in range(3):
            temp = ReprSingleMission(k, self._scr_size[0])
            temp.button = kengi.gui.Button(
                pos=(temp.centerpos[0]-fixed_size[0]//2, temp.centerpos[1]+offsety_bt), size=fixed_size,
                label='mission{}'.format(k+1)
            )
            self._repr_missions.append(temp)

        # small red squares to tell the mission is ongoing
        self._squares = dict()
        self._model = ref_mod
        self.img_pos = (200, 180)
        self._bg_image = pygame.image.load('assets/menu_bg.png')
        # img arches

        # - create mission buttons

        # dupe 3x same kind of callback func.
        def effetm1():
            if not self._model.is_m_locked(1):
                if self._model.is_m_over(1):
                    self._model.claim_reward(1)
                else:  # therefore its open
                    self._model.start_mission(1)

        def effetm2():
            if not self._model.is_m_locked(2):
                if self._model.is_m_over(2):
                    self._model.claim_reward(2)
                else:  # therefore its open
                    self._model.start_mission(2)

        def effetm3():
            if not self._model.is_m_locked(3):
                if self._model.is_m_over(3):
                    self._model.claim_reward(3)
                else:  # therefore its open
                    self._model.start_mission(3)

        self._repr_missions[0].button.callback = effetm1
        self._repr_missions[1].button.callback = effetm2
        self._repr_missions[2].button.callback = effetm3

    def _paint_missionset_v(self, screen):
        # screen.fill(game_defs.BG_COLOR)
        screen.blit(self._bg_image, (0, 0))

        for k in range(3):
            # dessin arches
            self._repr_missions[k].draw(screen)

            # dessin bt
            bt_obj = self._repr_missions[k].button
            screen.blit(bt_obj.image, bt_obj.rect.topleft)

        for k in range(1, 4):
            if k in self._squares:
                surf, _ = self._squares[k]
                pos = self._repr_missions[k - 1].button.rect.topleft
                screen.blit(surf, pos)

    def proc_event(self, ev, source=None):
        if ev.type == EngineEvTypes.PAINT:
            self._paint_missionset_v(ev.screen)

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            for k in range(3):
                bt_obj = self._repr_missions[k].button
                if bt_obj.rect.collidepoint(ev.pos):
                    if bt_obj.callback:
                        bt_obj.callback()

        elif ev.type == MyEvTypes.MissionEnds:
            self._squares[ev.idx][0].fill((0, 255, 0))

        elif ev.type == MyEvTypes.MissionFree:
            self._repr_missions[ev.idx-1].gray = False
            del self._squares[ev.idx]

        elif ev.type == MyEvTypes.MissionStarts:
            self._repr_missions[ev.idx-1].gray = True

            tmp = pygame.Surface((80, 80))
            tmp.fill((255, 0, 0))
            adj_pos = list(frame.pos_missions[ev.idx-1])
            adj_pos[1] += 30  # y
            self._squares[ev.idx] = (tmp, adj_pos)
