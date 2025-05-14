import pygame
import coremon_main.conf_eng as cgmconf
from coremon_main.events import EventReceiver, EventManager, EngineEvTypes, CgmEvent, PygameBridge
from gamecrm.defs_mco.gamestates import GameStates
from gamecrm.defs_mco.fonts_n_colors import my_colors
import gamecrm.defs_mco.glvars as glvars
import coremon_main.gui as gui


VALIGN_Y = 120
POS_TXT_INPUT1 = (VALIGN_Y, glvars.screen_height // 2)
INTER_FIELD_OFFSET = 45  # offset en px pour décaler second champ texte...

POS_BT_CONFIRM = (VALIGN_Y, 400)
POS_BT_CANCEL = (VALIGN_Y, 440)
TEXT_BT_CONFIRM = 'Login'
TEXT_BT_CANCEL = 'Exit'

LABEL0 = 'LOGIN-'
LABEL1 = 'PASSWORD-'

#T_BOUTON_A = (VALIGN_Y, 450)
#T_BOUTON_B = (VALIGN_Y, 490)
# HEAD_LOGIN = 'I already have an account'
# INFO_LOGIN = 'Press tab to go from one field to another, Enter to validate'
# FOOT_LOGIN = 'I want to join the game'

# - constantes GUI
# REGISTER_BT_TEXT = 'Sign up via internet'
# REGISTER_BT_POS = (182, 475)


class LoginView(EventReceiver):
    LABEL_TEXT = 'Welcome to M-Conquest! (an experimental multiplayer game)'
    POS_LABEL = (VALIGN_Y, 135)

    @staticmethod
    def confirm_routine():
        EventManager.instance().post(
            CgmEvent(EngineEvTypes.PUSHSTATE, state_ident=GameStates.MenuSolo)
        )

    def __init__(self, ref_mod):
        self.bg_color = pygame.Color(my_colors['fond_anto'])

        super().__init__()
        self._ref_mod = ref_mod
        self.scr = cgmconf.get_screen()  # from cgm_engine

        self._font = glvars.fonts['courier_font']
        self._buttons = list()
        self._crea_boutons()

        self.focus = 0

        def rien(txt):
            pass

        self.saisie_txt1 = gui.TextInput('>', self._font, rien, POS_TXT_INPUT1, 200)

        tmp_pos = list(POS_TXT_INPUT1)
        tmp_pos[1] += INTER_FIELD_OFFSET

        self.saisie_txt2 = gui.TextInput('>', self._font, rien, tmp_pos, 200)
        self.saisie_txt2.pwd_field = True

        self.game_label = self._font.render(self.LABEL_TEXT, True, (0x11,)*3, (0xaa, 0x0c, 0xbe))

    def _crea_boutons(self):
        bt = gui.Button(self._font, TEXT_BT_CONFIRM, POS_BT_CONFIRM, LoginView.confirm_routine)
        self._buttons.append(bt)

        def cancel_routine():
            EventManager.instance().post(
                CgmEvent(PygameBridge.QUIT)
            )

        bt = gui.Button(self._font, TEXT_BT_CANCEL, POS_BT_CANCEL, cancel_routine)
        self._buttons.append(bt)

        # TODO remettre bouton register qui fonctionne ---
        # bt = gui.Button(font, REGISTER_BT_TEXT, REGISTER_BT_POS, None)
        # self.buttons.append(bt)

    # - activation / désactivation impacte boutons également
    def turn_on(self):
        super().turn_on()
        for bt in self._buttons:
            bt.turn_on()

        self.focus = 0
        self.saisie_txt1.turn_on()
        self.saisie_txt1.focus()

        #self.saisie_txt2.on()

    def turn_off(self):
        super().turn_off()
        for bt in self._buttons:
            bt.turn_off()
        if self.focus == 0:
            self.saisie_txt1.turn_off()
        else:
            self.saisie_txt2.turn_off()

    def do_focus1(self):
        if self.focus == 1:
            return
        self.focus = 1
        self.saisie_txt1.no_focus()
        self.saisie_txt1.turn_off()
        self.saisie_txt2.focus()
        self.saisie_txt2.turn_on()

    def do_focus0(self):
        if self.focus == 0:
            return
        self.focus = 0
        self.saisie_txt1.focus()
        self.saisie_txt1.turn_on()
        self.saisie_txt2.no_focus()
        self.saisie_txt2.turn_off()

    # ---
    #  GESTION EV.
    # --- ---
    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            # dessin
            self.scr.fill(self.bg_color)
            self.scr.blit(self.game_label, self.POS_LABEL)
            for b in self._buttons:
                self.scr.blit(b.image, b.position)
            self.scr.blit(self.saisie_txt1.image, self.saisie_txt1.position)
            self.scr.blit(self.saisie_txt2.image, self.saisie_txt2.position)

        elif ev.type == PygameBridge.MOUSEBUTTONDOWN:
            if self.saisie_txt2.contains(ev.pos):
                    self.do_focus1()
            elif self.saisie_txt1.contains(ev.pos):
                    self.do_focus0()

        elif ev.type == PygameBridge.KEYDOWN:
            if ev.key == pygame.K_TAB:
                if self.focus == 0:
                    self.do_focus1()
                else:
                    self.do_focus0()

            elif ev.key == PygameBridge.K_RETURN:
                LoginView.confirm_routine()
