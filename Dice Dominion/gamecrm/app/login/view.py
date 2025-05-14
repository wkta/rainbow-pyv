import cgm_engine
from defs import glvars
from gamecrm.app import AffichageBoiteLogin
from gamecrm.app import DispCredentials
# from basis.PygameEvTypes import PygameEvTypes
# from core.gui.BaseConnectorUsingGui import BaseConnectorUsingGui

# - deprecated !

from cgm_engine import EventReceiver, EngineEvTypes, EventManager, CgmEvent
from defs import *

# from engine.GameComponent import GameComponent
# from engine.UnitedEvent import UnitedEvent
# from engine.utils import PygameEvTypes, EngineEvTypes
# from engine.view import retrieve_pygame_surf
# from shared.view.DispOnePicture import DispOnePicture
# from shared.view.DispSolidColor import DispSolidColor

from gamecrm import gui

POS_BOITE_LOGIN = (13, 160)
T_BOUTON_A = (285, 36)
T_BOUTON_B = (140, 34)

HEAD_LOGIN = 'I already have an account'
INFO_LOGIN = 'Press tab to go from one field to another, Enter to validate'
FOOT_LOGIN = 'I want to join the game'
PSEUDO = 'LOGIN-'
MDP = 'PASSWORD-'


# - constantes GUI
CONFIRM_BT_TEXT = 'Login'
CANCEL_BT_TEXT = 'Cancel'
REGISTER_BT_TEXT = 'Sign up via internet'

CONFIRM_BT_POS = (180, 398)
CANCEL_BT_POS = (330, 398)
REGISTER_BT_POS = (182, 475)


class VueEcranLogin(EventReceiver):  #(BaseConnectorUsingGui):
    def __init__(self, ref_mod):
        super().__init__()

        # on enchaine quelques afficheurs pr obtenir exactement ce que l'on souhaite!
        #fond_uni = DispSolidColor('fond_anto')
        #self.disp1 = DispOnePicture(fond_uni, 'bg_login.png', True)

        # TODO revoir affichage boite login / données saisies...
        self.disp2 = AffichageBoiteLogin(None)  #self.disp1)

        self.aff_cred = DispCredentials(
            self.disp2,
            ref_mod.isFocusingLogin(),
            ref_mod.getLoginStr(),
            ref_mod.getPwdStr()
        )

        font = glvars.fonts['courier_font']

        # --- bloc de création des boutons
        self.buttons = list()

        def confirm_routine():
            EventManager.instance().post(
                CgmEvent(EngineEvTypes.CHANGESTATE, state_ident=GameStates.MenuSolo)
            )

        bt = gui.Button(font, CONFIRM_BT_TEXT, CONFIRM_BT_POS, confirm_routine)
        self.buttons.append(bt)

        def cancel_routine():
            EventManager.instance().post(
                CgmEvent(cgm_engine.PygameBridge.QUIT)
            )
        bt = gui.Button(font, CANCEL_BT_TEXT, CANCEL_BT_POS, cancel_routine)
        self.buttons.append(bt)

        # TODO remettre bouton register qui fonctionne ---
        # bt = gui.Button(font, REGISTER_BT_TEXT, REGISTER_BT_POS, None)
        # self.buttons.append(bt)

        # - fin du bloc de création des boutons

        self.change_save_pwd(ref_mod.get_save_pwd())

        #super().__init__(0, self.aff_cred)
        # self.scr = retrieve_pygame_surf()
        self.scr = cgm_engine.screen

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            self.on_paint(ev)
        else:
            for b in self.buttons:
                b.proc_event(ev, source)

    # def switch_on(self):
    #     self.buttons[0].switch_on()
    #     super().switch_on()

    def on_paint(self, ev):
        self.scr.fill((200, 30, 50))
        for b in self.buttons:
            self.scr.blit(b.image, b.position)

    def free_gfx_mem(self):
        self.disp1.free_mem()
        self.disp1 = None
        self.disp2 = None
        self.aff_cred = None

    # --------------------------------
    #  MÉCANISME CALLBACK
    # --------------------------------

    # wtf ?!!
    # def list_extended_interactions(self):
    #     return {
    #         CredentialsChangedEvent: self._proc_credential_changed,
    #         FocusChangedEvent: self._proc_focus_changed,
    #
    #         PygameEvTypes.MOUSEBUTTONUP:  self.__proc_pygame,
    #         # PygameEvTypes.MOUSEMOTION: self.__proc_pygame,
    #     }

    def _proc_mouse_click(self, ev):
        super()._proc_mouse_click(ev)
        # transmettre pr popup / composants pgu
        self.__proc_pygame(ev)

    def __proc_pygame(self, ev):
        self.aff_cred.input_pygame_evt(ev)

    def _proc_focus_changed(self, ev):  # on va devoir ajuster le cadre
        # suffit d'appeler la méthode métier deplaceCadreFocus...
        self._compo_gui.deplaceCadreFocus(ev.focusing_login)

    def _proc_credential_changed(self, ev):  # nouvelles val. apparues ds le modele
        if ev.l_actu is not None:
            self._compo_gui.renderLogin(ev.l_actu)  # sur le dessus des elt de GUI on a normalement *AffichageCred*

        if ev.p_actu is not None:
            self._compo_gui.renderPwd(ev.p_actu)

    def affiche_erreur(self, tmp):
        self.aff_cred.setErreurLogin(tmp)

    def change_save_pwd(self, save):
        self.aff_cred.setSavePwd(save)
