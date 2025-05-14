from gamecrm.shared.LocalStorage import LocalStorage


class LoginModel:
    """
    classe utilisée pr stocker temporairement login / pwd
    durant le processus de login. Le pwd est gardé secret (pas d'affichage) mais on compte et
    on affiche correctement le nb de car
    """

    def __init__(self):
        data_cote_cli = LocalStorage.instance()
        self.curr_login = data_cote_cli.get_val('stored_username')
        self.curr_pwd = data_cote_cli.get_val('stored_pwd')
        self.save_pwd = len(self.curr_pwd) > 0

        self.focus_sur_login = True  # valeur initiale pr : ou se trouve la boite de focus

    def ajoute_lettre(self, c):
        self.ajouteCar(c)
        return

        if self.focus_sur_login:
            self._manager.post(
                CredentialsChangedEvent(self.curr_login, None)
            )
        else:
            self._manager.post(
                CredentialsChangedEvent(None, self.getPwdStr())
            )

    def suppr_lettre(self):
        return

        if self.focus_sur_login:
            if len(self.curr_login) > 0:
                self.curr_login = self.curr_login[:-1]
                self._manager.post(
                    CredentialsChangedEvent(self.curr_login, None)
                )
            return

        # le focus est sur le mdp
        if len(self.curr_pwd) > 0:
            self.curr_pwd = self.curr_pwd[:-1]
            self._manager.post(
                CredentialsChangedEvent(None, self.getPwdStr())
            )

    # ----------------
    #  MÉTIER
    # ----------------
    def toggleFocus(self):  # gestion focus
        if not self.focus_sur_login:
            self.focus_sur_login = True
        else:
            # focus_sur_login est vrai, actuellement
            self.focus_sur_login = False
        # propager changement
        self._manager.post(FocusChangedEvent(self.focus_sur_login))  # propagation nouvelle valeur

    def ajouteCar(self, c):
        if self.focus_sur_login:
            self.curr_login += c
        else:
            self.curr_pwd += c

    # méthodes pr la remise à zéro
    def resetPwdOnly(self):
        if len(self.curr_pwd) > 0:
            self.curr_pwd = ''
            tag_pwd = self.getPwdStr()
            self._manager.post(
                CredentialsChangedEvent(None, tag_pwd)
            )

    def resetAll(self):
        tag_login = tag_pwd = None

        if len(self.curr_login) > 0:
            self.curr_login = ''
            tag_login = self.curr_login

        if len(self.curr_pwd) > 0:
            self.curr_pwd = ''
            tag_pwd = self.getPwdStr()

        ev = CredentialsChangedEvent(tag_login, tag_pwd)
        if (tag_login is None) and (tag_pwd is None):
            return
        self._manager.post(
            CredentialsChangedEvent(tag_login, tag_pwd)
        )

    # méthodes utiles pour initialiser la vue, mais aussi pr masquer le mot de passe dans laffichage graphique
    def isFocusingLogin(self):
        return self.focus_sur_login

    def getLoginStr(self):
        return self.curr_login

    def getPwdStr(self):
        k = len(self.curr_pwd)
        li_etoiles = '*' * k
        return ''.join(li_etoiles)

    def change_pwd_save(self):
        self.save_pwd = not self.save_pwd
        return self.save_pwd

    def get_save_pwd(self):
        return self.save_pwd
