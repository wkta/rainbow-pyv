import webbrowser

from atoms.Trigger import Trigger
from proc import netw
import time
import pygame
import pygame.locals as pl
from atoms.GfxElementManager import GfxElementManager
from core.GameState import GameState
from gamecrm.app import CredentialsMod
from models.avatar.AvatarPersiste import AvatarPersiste
from util.ColorPalette import ColorPalette
from util.FontPalette import FontPalette
from util.UserSpec import UserSpec
from views.misc.CenteredImgView import CenteredImgView
from views.misc.CredentialsView import CredentialsView, CLIC_VALIDATION, CLIC_INSCRIPTION, CLIC_RESET
from views.misc.SingleColoredView import SingleColoredView


COORDS_TRIG_SAVING_PWD = (215, 345)
SIZE_TRIG_SAVING_PWD = (20, 20)


class SimpleLogin(GameState):  # TODO amélioration: implémenter visibilité du curseur
    def __init__(self):
        super().__init__()
        self.registration_url = None
        self.cred = None

        # --- membres utiles pr gérer la logique de ce gamestate
        self.key_pressed = None
        self.sending_cred = None

        # --- membres corresp. aux contrôles
        self.bouton_inscript = None
        self.bouton_valider = None
        self.boites_saisie = None

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = 400  # ms
        self.keyrepeat_interval_ms = 110  # ms

        self.input_string = None
        self.font_object = None

        self.date_lim_popup_refus = None
        self.label_refus = None

        self.is_saving_pwd = None
        self.trig_saving_pwd = None
        self.checkbox_color = None
        self.img_txt_memoriser = None

    def enter(self, engine):
        cp = ColorPalette.instance()
        self.checkbox_color = cp.get('orange')
        self.trig_saving_pwd = Trigger(COORDS_TRIG_SAVING_PWD, SIZE_TRIG_SAVING_PWD)

        fp = FontPalette.instance()
        font_px = fp.get('pxled_med_font')
        self.img_txt_memoriser = font_px.render_txt('save password', False, self.checkbox_color)

        self.registration_url = engine.getGlVar('newplayer_url')

        user_spec = UserSpec.instance()
        self.is_saving_pwd = user_spec.isSavingPwd()
        temp_login = user_spec.getSavedLogin()
        if user_spec.isSavingPwd():
            temp_pwd = user_spec.getSavedPwd()
        else:
            temp_pwd = ''

        # --- init. modèle & vue pr les info. joueur
        self.cred = CredentialsMod(temp_login, temp_pwd)
        self.input_string = self.cred.curr_login  # reférence

        # --- pour gérer la logique des contrôles
        self.key_pressed = False
        self.sending_cred = False  # indique si oui ou non l'utilisateur à terminé la saisie

        self.cursor_position = 0  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

        couleur_rouge = ColorPalette.instance().retrieve('rouge')
        fonte = FontPalette.instance().retrieve('default_small_font')
        self.label_refus = fonte.render_txt('identifiants non valides, re-essayez', False, couleur_rouge)

    def initViews(self, screen_size):
        code_couleur_fond = '#b0b1a1'
        self.addView(SingleColoredView(code_couleur_fond))

        fond_ecran = CenteredImgView('bg_login.png', True, screen_size)
        self.addView(fond_ecran)

        self.addView(CenteredImgView('vignette_login.png', False, screen_size, 250, -1))

        self.boites_saisie = CredentialsView(self.cred)
        self.addView(self.boites_saisie)

    def release(self):
        del self.boites_saisie
        del self.cred
        super().release()
        GfxElementManager.memRelease()

    def handleEvents(self, ev_list, engine):
        code_gui = self.boites_saisie.calculeRetourGUI(ev_list)
        if code_gui == CLIC_VALIDATION:
            self.sending_cred = True
            return

        if code_gui == CLIC_INSCRIPTION:
            webbrowser.open(self.registration_url)
            return

        if code_gui == CLIC_RESET:
            self.cred.hardReset()
            return

        # --- gestion CLAVIER
        for event in ev_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mp = pygame.mouse.get_pos()
                if self.trig_saving_pwd.contains(mp):
                    uspec = UserSpec.instance()
                    if self.is_saving_pwd:
                        self.is_saving_pwd = False
                        uspec.doNotSavePwd()
                    else:
                        self.is_saving_pwd = True
                        uspec.doSavePwd()

            elif event.type == pygame.KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if not event.key in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pl.K_BACKSPACE:  # FIXME: Delete at beginning of line?
                    # self.input_string = self.input_string[:max(self.cursor_position - 1, 0)] + \
                    #                    self.input_string[self.cursor_position:]
                    self.cred.execBackspace()

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pl.K_DELETE:
                    self.input_string = self.input_string[:self.cursor_position] + \
                                        self.input_string[self.cursor_position + 1:]

                elif event.key == pl.K_RETURN:
                    self.sending_cred = True

                elif event.key == pl.K_TAB:
                    self.cred.toggleFocus()
                    if self.cred.isFocusingLogin():
                        self.input_string = self.cred.curr_login
                    else:
                        self.input_string = self.cred.curr_pwd

                elif event.key == pl.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == pl.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pl.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pl.K_HOME:
                    self.cursor_position = 0

                else:
                    # If no special key is pressed, add unicode of key to input_string
                    # self.input_string = self.input_string[:self.cursor_position] + \
                    #                    event.unicode + \
                    #                    self.input_string[self.cursor_position:]
                    self.cred.execAddChar(event.unicode)

                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == pl.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

    def update(self, engine):
        # --- répétition des touches
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock
            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = self.keyrepeat_intial_interval_ms - \
                                                  self.keyrepeat_interval_ms

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(
                    pygame.event.Event(pl.KEYDOWN, {'key': event_key, 'unicode': event_unicode})
                )
        self.clock.tick()

        if self.date_lim_popup_refus is not None:
            if time.time() > self.date_lim_popup_refus:
                self.date_lim_popup_refus = None

        if not self.sending_cred:
            return
        self.sending_cred = False  # le login & mdp saisi seront testés une fois, une seule

        ret_serveur = self.cred.tryAuth()
        if ret_serveur is None:  # identifiants refusés, affichons un message graphique
            self.date_lim_popup_refus = time.time() + 2.5  # t plus 2.5 sec
            self.cred.softReset()
            return

        # +------------------------------+
        #       IDENTIFIANTS ACCEPTÉS
        # +------------------------------+
        user_spec = UserSpec.instance()
        user_spec.saveLogin(self.cred.curr_login)
        if user_spec.isSavingPwd():
            user_spec.savePwd(self.cred.curr_pwd)

        # cas particulier : c'est la toute 1ère connexion
        if netw.test_first_time_login(self.cred.curr_login):
            print('****** 1st time login ********')

            proto_id, proto_name = netw.trigger_av_creation(
                self.cred.curr_login,
                'serial_fake'
            )
            print(str(proto_id), str(proto_name))
            ret_serveur.chooseAvatar((proto_id, proto_name))  # sécurise l'objet ret_serveur, inst. de ConnexionSurTl

            av_identity = AvatarPersiste.create_ex_nihilo(proto_name)
            av_identity.bindToServer(int(proto_id))
            av_identity.saveToServer(ret_serveur)  # le vrai serial est enregistré, grâce à la connexion sécurisée

        else:  # le compte possède déjà un avatar
            les_avatars = ret_serveur.getTabAvatars()
            selected_couple = les_avatars[0]
            id_avatar, full_av_name = selected_couple
            ret_serveur.chooseAvatar(selected_couple)
            superserial = netw.retrieve_av_serial(id_avatar)  # récup info. avatar existantes
            av_identity = AvatarPersiste.deserialize(superserial)
            av_identity.bindToServer(id_avatar)

        # --- passage au mode menu directement
        engine.setGlVar("avatar_identity", av_identity)
        engine.setGlVar('connexion', ret_serveur)

        if engine.hasGlVar('mode_online'):
            if engine.getGlVar('mode_online') == '1':
                engine.changeState('explo_online')
                return

        # enregistrement info. en var gloables pr que le mode multi puisse aussi log sur la web app
        engine.setGlVar('curr_login', self.cred.curr_login)
        engine.setGlVar('curr_pwd', self.cred.curr_pwd)

        # mode initial après login = multi_pur (aka. promenade)
        engine.changeState('multi_pur')

    # ajout manuel p/r aux vues existantes
    def drawContent(self, surf):
        super().drawContent(surf)

        # case à cocher pr sauvegarde identifiants
        if self.is_saving_pwd:
            tmp_rect = list()
            tmp_rect.extend(COORDS_TRIG_SAVING_PWD)
            tmp_rect.extend(SIZE_TRIG_SAVING_PWD)
            neg_offset = -2
            tmp_rect[0] -= neg_offset
            tmp_rect[1] -= neg_offset
            tmp_rect[2] += 2 * neg_offset
            tmp_rect[3] += 2 * neg_offset
            pygame.draw.rect(surf, self.checkbox_color, tmp_rect)
        self.trig_saving_pwd.draw(surf, self.checkbox_color)

        # texte mémoriser pwd
        surf.blit(self.img_txt_memoriser, (COORDS_TRIG_SAVING_PWD[0] + 30, COORDS_TRIG_SAVING_PWD[1] - 2))

        # txt temporaire pr signaler identifiants refusés
        if self.date_lim_popup_refus is not None:
            surf.blit(self.label_refus, (110, 370))
