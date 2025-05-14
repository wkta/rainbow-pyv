from gamecrm.app.conquest.NetwHistory import NetwHistory
from gamecrm.shared.RemotePlayer import RemotePlayer
from gamecrm.shared.behaviors import Human, AiPassive, AiDumb, Ai1


class PlayerBehaviorFactory:
    VALID_TYPES = range(5)

    HUMAN = 0
    NETWORK = 1
    AI_PASSIVE = 2
    AI_DUMB = 3
    AI_1 = 4

    netw_history = NetwHistory()

    @staticmethod
    def build(opponent_type, data):
        print('building controller for player type[{}]'.format(opponent_type))

        # - cas particulier du remote player
        if opponent_type == PlayerBehaviorFactory.NETWORK:
            return RemotePlayer(opponent_type, data, PlayerBehaviorFactory.netw_history)

        # - cas général
        assoc_type_cls = {
            PlayerBehaviorFactory.HUMAN: Human,
            PlayerBehaviorFactory.AI_PASSIVE: AiPassive,
            PlayerBehaviorFactory.AI_DUMB: AiDumb,
            PlayerBehaviorFactory.AI_1: Ai1,
        }
        if opponent_type not in assoc_type_cls:
            raise ValueError('unknown opponent type {}'.format(opponent_type))
        adhoc_cls = assoc_type_cls[opponent_type]
        return adhoc_cls(opponent_type, data)


# class BasePlayer(metaclass=ABCMeta):
#
#     def __init__(self, type, data):
#         object.__init__(self)
#         self.type = type
#         self._data = data
#         self._player_id = data._player_id
#         self._source = data
#         self._data.unreg_all_events()
#         data.reg_event_func(eventtypes.NEWTURN, data.on_newturn)
#
#     @abstractmethod
#     def on_newturn(self, event):
#         pass
#
#     def update(self):
#         """
#
#         """
#         pass
#
#     def on_mouse_motion(self, event):
#         """
#
#         """
#         pass
#
#     def on_mouse_btn_down(self, event):
#         """
#
#         """
#         pass
#
#     def on_mouse_btn_up(self, event):
#         """
#
#         """
#         pass
#
#     def on_attack_result(self, event):
#         """
#
#         """
#         pass
#
#     def on_select_result(self, event):
#         """
#
#         """
#         pass
#
#     def on_gamestate_update(self, vent):
#         """
#
#         """
#         pass
#
#
# class Human(BasePlayer):
#
#     def __init__(self, type, data):
#         super().__init__(type, data)
#
#         data.reg_event_func(pygame.MOUSEBUTTONDOWN, data.on_mouse_btn_down)
#         data.reg_event_func(pygame.MOUSEBUTTONUP, data.on_mouse_btn_up)
#         data.reg_event_func(pygame.MOUSEMOTION, data.on_mouse_motion)
#
#     def on_newturn(self, event):
#         print('decision joueur local attendue...')
#
#     def on_mouse_btn_up(self, event):
#         """
#
#         """
#         ##        print "Human player mouse btn up"
#         if self._data._myturn:
#             if event.button == 1:
#                 pos = event.pos
#                 # TODO: hack!! need it really ref to world?
#                 land = config.world.get_land_from_abs(pos)
#                 if land:
#                     eventtypes.post_select_land(self._source, self._player_id, land.get_id())
#             else:
#                 # TODO: hack, not good, should be the "next turn" button!!
#                 self._data.send_end_turn()
# ##                eventtypes.post_end_turn(self._source, self._player_id)
# ##                self._data._myturn = False
#
#
# class RemoteHuman(BasePlayer):
#     def __init__(self, type, data):
#         super().__init__(type, data)
#         self.no_tour = 0
#
#     def on_newturn(self, event):
#         self.no_tour += 1
#         print('decision joueur DISTANT attendue pr le tour {}...'.format(self.no_tour))
#
#         ev = CgmEvent(EngineEvTypes.ASYNCREQUEST, id_req=997, msg_reseau='', cb=self.retour_direct)
#         ev.msg_reseau = 'tom/async_test_server.php?timestamp=1547310916'
#         EventManager.instance().post(ev)
#         # print('-- lands --')
#         # for land in glvars.world.get_lands():  # land est de type 'DiceLand'
#         #     ligne_txt = 'land {}'.format(land.get_id())
#         #     print(ligne_txt)
#
#     def retour_direct(self, txt_retour):
#         print('[RemoteHuman] CALLBACK TRIGGERS')
#         print(txt_retour)
#
#
# class AiPassive(BasePlayer):
#     """
#
#     """
#
#     def __init__(self, type, data):
#         super().__init__(type, data)
#
#         self._data.reg_event_func(eventtypes.ATTACKRESULT, data.on_attack_result)
#         self._data.reg_event_func(eventtypes.SELECTRESULT, data.on_select_result)
#         self._data.reg_event_func(eventtypes.GSUPDATE, data.on_gamestate_update)
#
#     def on_newturn(self, event):
#         """
#
#         """
#         self._data.send_end_turn()
#
#
# # TODO: correct implementation using selectresult!!
# class AiDumb(AiPassive):
#     """
#
#     """
#
#     def __init__(self, type, data):
#         super().__init__(type, data)
#
#         self.last_aggr = None
#
#     def on_newturn(self, event):
#         """
#
#         """
#         event = pygame.event.Event(eventtypes.GSUPDATE, {"aggressorid": self.last_aggr})
#         self.on_gamestate_update(event)
#
#     def on_gamestate_update(self, event):
#         """
#
#         """
#         if self.last_aggr == event.aggressorid:
#             lands = self._data.get_selectable_lands()
#             print("=====================dumb ai:")
#             for land, linked in lands.items():
#                 print(land.get_id(), [i.get_id() for i in linked])
#             print("---------------")
#             if len(lands):
#                 count = 0
#                 tmp = list(lands.keys())
#                 land = random.choice(tmp)
#                 while land.num_dice < 2 and count < len(tmp) and land.get_id() != self.selection:
#                     land = random.choice(tmp)
#                     count += 1
#
#                 print("dumb ai, chosen land:", land.get_id())
#                 if land.num_dice < 2:
#                     print("dumb ai: to less dices")
#                     self._data.send_end_turn()
#                 defensor = random.choice(lands[land])
#                 print("defensor:", defensor.get_id())
#                 self.last_aggr = land.get_id()
#                 eventtypes.post_select_land(self._source, self._player_id, land.get_id())
#                 eventtypes.post_select_land(self._source, self._player_id, defensor.get_id())
#             else:
#                 self._data.send_end_turn()
#
#
# class Ai1(AiPassive):
#     """
#
#     """
#
#     def __init__(self, type, data):
#         super().__init__(type, data)
#
#         self.num_qonquer = 0
#
#     def on_newturn(self, event):
#         """
#
#         """
#         self.on_gamestate_update(event)
#
#     def on_gamestate_update(self, event):
#         """
#
#         """
#
#         lands = self._data.get_selectable_lands()
#         if len(lands):
#             get_num_dice = len(lands)
#             num_dice = 0
#             for land in lands:
#                 num_dice += land.num_dice
#             max_dice = len(lands) * 8
#             full = (max_dice <= num_dice)
#             print("full:", full, "<<<<<<<<<<<<<<<<<<<")
#             if self.num_qonquer < 1:
#                 if full:
#                     self.num_qonquer = get_num_dice / 8
#                     tmp = list(lands.keys())
#                     land = random.choice(tmp)  # lands.keys())
#                     defensor = random.choice(lands[land])
#                     eventtypes.post_select_land(self._source, self._player_id, land.get_id())
#                     eventtypes.post_select_land(self._source, self._player_id, defensor.get_id())
#
#                 else:
#                     self.num_qonquer = 0
#                     self._data.send_end_turn()
#             else:
#                 print("num_qonquer", self.num_qonquer)
#                 print("max_dice", max_dice)
#                 ##            print "num_lands", num_lands
#                 print("num_dice", num_dice)
#                 self.num_qonquer -= 1
#                 tmp = list(lands.keys())
#                 land = random.choice(tmp)
#                 defensor = random.choice(lands[land])
#                 eventtypes.post_select_land(self._source, self._player_id, land.get_id())
#                 eventtypes.post_select_land(self._source, self._player_id, defensor.get_id())
#         else:
#             self.num_qonquer = 0
#             self._data.send_end_turn()
