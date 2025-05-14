from pygame.locals import *
# from shared.LocalStorage import LocalStorage
from coremon_main.events import PygameBridge, EventReceiver, EngineEvTypes


class LoginCtrl(EventReceiver):
    def __init__(self, ref_mod, ref_view):
        super().__init__()
        self.ref_mod = ref_mod
        self.ref_view = ref_view

    # ---
    #  GESTION EV.
    # --- ---
    def proc_event(self, ev, source):
        if ev.type == PygameBridge.KEYDOWN:
            self.on_key(ev)
        elif ev.type == PygameBridge.QUIT:
            self.on_quit(ev)


    def on_quit(self, ev):
        self.pev(EngineEvTypes.POPSTATE)

    # ---
    #  PRIVÉ
    # --- ---
    def __proc_lettre(self, ev):
        if ev.char is not None:
            self.ref_mod.ajoute_lettre(ev.char)
        self.ref_view.affiche_erreur(False)

    def __proc_rem_field_car(self, ev):
        self.ref_mod.suppr_lettre()
        self.ref_view.affiche_erreur(False)

    def __proc_change_focus(self, ev):
        self.ref_mod.toggleFocus()

    # def __proc_trigger(self, ev):
    #     self.ref_view.affiche_erreur(False)
    #     if ev.trigger_ident == TRIG_FOCUS_MAIL and not self.ref_mod.isFocusingLogin():
    #         self.ref_mod.toggleFocus()
    #     elif ev.trigger_ident == TRIG_FOCUS_PWD and self.ref_mod.isFocusingLogin():
    #         self.ref_mod.toggleFocus()
    #
    #     elif ev.trigger_ident == LOGIN_INSCRIPTION:
    #         self._manager.post(
    #             UnitedEvent(Dingus2EvTypes.PUSHSTATE, state_ident=ST_INSCRIPTION)
    #         )
    #
    #     elif ev.trigger_ident == LOGIN_RESET:
    #         self.ref_mod.resetAll()
    #
    #     elif ev.trigger_ident == LOGIN_VALIDATION:
    #         self.go_submit_cred()
    #
    #     elif ev.trigger_ident == TRIG_CHECKBOX_MEM_MDP:
    #         self.change_pwd_checkbox()
    #
    #     elif ev.trigger_ident == ID_TRIG_CLICK_ENGLISH:
    #         self.change_lang(0)
    #
    #     elif ev.trigger_ident == ID_TRIG_CLICK_FRENCH:
    #         self.change_lang(1)

    def on_key(self, ev):
        #print('******')
        #print(ev.unicode)

        if ev.key == K_RETURN:
            self.go_submit_cred()
            return

        elif ev.key == K_BACKSPACE:
            # self._manager.post(
            #    RemoveCharInField()
            # )
            print('backspace detecte')
            return

        elif ev.key == K_TAB:
            print('tab detecte')
            return

        elif ev.key == K_ESCAPE:
            print('esc')
            return

        # envoi de la lettre à traiter au modèle
        print(str(ev.unicode))
        print('ajout lettre ds modele')
        self.ref_mod.ajoute_lettre(ev.unicode)

    @staticmethod
    def persister_login_mdp(l_soumis, p_soumis):
        print('warning appel à persister_login_mdp(...) qui est un mockup')
        return
        # ud = LocalStorage.instance()
        # ud.set_val('stored_username', l_soumis)
        # ud.set_val('stored_pwd', p_soumis)

    def change_pwd_checkbox(self):
        tmp = self.ref_mod.change_pwd_save()
        self.ref_view.change_save_pwd(tmp)

    def change_lang(self, lang):
        print('warning appel à change_lang(...) qui est un mockup')
        return
        # ud = LocalStorage.instance()
        # ud.set_val('lang', lang)

    def go_submit_cred(self):
        """
        essaye de s'authentifier auprès du serveur (LegacyApp) avec ce qui ns a été fourni
        :return: soit None, si échec authentification, soit instance de LegacyAppAuthConnection
        """

        # cfg = ConfigReseau.instance()
        # cfg.renseigneLoginPwd((self.curr_login, self.curr_pwd))
        # try:
        #    tmp = LegacyAppAuthConnection.instance()
        #    return tmp
        # except Exception:
        #    return None

        # tmp = ConnexionSurTl(
        #     settings.BASEURL2,
        #     self.curr_login,
        #     self.curr_pwd
        # )

        # self._manager.post(
        #    SubmitUserCred(self.ref_mod.curr_login, self.ref_mod.curr_pwd)
        # )
        print('calling go_submit_credentials')
        return

        # TODO persister Mdp que si lutilisateur le demande !
        # TODO remettre la case à cocher permettant de le spécifier
        l_soumis = self.ref_mod.curr_login
        p_soumis = self.ref_mod.curr_pwd

        self.game_serv = GameServer.instance()
        cred_ok, id_av_recu = self.game_serv.legacy_app_auth(
            l_soumis,
            p_soumis
        )

        if not cred_ok:  # vérification en restant dans le mode ecran_login
            print('server: access denied. Check your login, password.')
            self.ref_view.affiche_erreur(True)
            return

        # -- on sait que le login est faisable...
        if not self.ref_mod.get_save_pwd():
            p_soumis = ''
        LoginCtrl.persister_login_mdp(l_soumis, p_soumis)  # ecriture username [, password] sur le disque

        # avatar_id a déjà été enregistré ds les var. globales
        # -- on passe dans le mode Loading
        self._manager.post(
            UnitedEvent(Dingus2EvTypes.CHANGESTATE, state_ident=ST_LOADING)
        )
