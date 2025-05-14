import pygame


# from gettext import translation
# en = translation('login', localedir='locale', languages=var_lang)
# en.install()

# --- constantes pr faire marcher AffichageBoiteLogin (qui affiche limage de boite de login)
# from SharedData import SharedData
# from prim_gui.GfxManager import GfxManager, dessin_txt_contraint
# from prim_gui.Trigger import Trigger

from defs import glvars


# TODO fix it
class Trigger:
    def __init__(self, fonte, pos, taille):
        pass

    def set_visible(self, bool_val):
        pass

POS_BOITE_LOGIN = (13, 160)
T_BOUTON_A = (285, 36)
T_BOUTON_B = (140, 34)
POS_BOUTON1 = (180, 398)
POS_BOUTON2 = (330, 398)
POS_BOUTON3 = (182, 475)
HEAD_LOGIN = 'I already have an account'
INFO_LOGIN = 'Press tab to go from one field to another, Enter to validate'
FOOT_LOGIN = 'I want to join the game'
PSEUDO = 'LOGIN-'
MDP = 'PASSWORD-'
VALIDER = 'Login'
ANNULER = 'Cancel'
INSCRIPTION = 'Sign up via internet'


class AffichageBoiteLogin:  #(BaseGuiDecorator):
    GFX_IDENT = 'BOITE_LOGIN'

    def __init__(self, vue_decoree):
        # super().__init__(vue_decoree)

        drawing_font = glvars.fonts['pxled_med_font']

        title_font = glvars.fonts['pxled_med_font_big']
        self.ecriture = drawing_font
        self.ecriture_titre = title_font

        self.couleur = glvars.colors['deep_purple']
        self.couleur_sombre = glvars.colors['noir']

        # TODO fix chargement images...
        # self.gfxm = GfxManager.instance()
        # if not self.gfxm.isLoaded(self.__class__.GFX_IDENT):
        #     self.gfxm.loadOne(self.__class__.GFX_IDENT, 'vignette_login.png')

        # -- création triggers
        triggers_visible = False
        self.bouton_valider = Trigger(drawing_font, POS_BOUTON1, T_BOUTON_B)
        self.bouton_valider.set_visible(triggers_visible)

        self.bouton_reset = Trigger(drawing_font, POS_BOUTON2, T_BOUTON_B)
        self.bouton_reset.set_visible(triggers_visible)

        self.bouton_inscript = Trigger(drawing_font, POS_BOUTON3, T_BOUTON_A)
        self.bouton_inscript.set_visible(triggers_visible)

        self.surface_text = pygame.Surface((469, 400), pygame.SRCALPHA)
        self.surface_text.fill((255, 255, 255, 0))

        # création étiquettes
        self.renderHeadLogin()
        self.renderFootLogin()
        self.renderPseudo()
        self.renderMdp()
        self.renderValider()
        self.renderAnnuler()
        self.renderInscrire()

    @classmethod
    def __paste_over_trigger(cls, screen, ref_trig, img):
        img_size = img.get_size()
        trig_size = ref_trig.getSize()

        cool_pos = list(ref_trig.getPos())
        # calcul mileu
        cool_pos[0] += trig_size[0] // 2
        cool_pos[1] += trig_size[1] // 2
        # calcul pt haut gauche pr cibler le meme milieu
        # cool_pos[0] += 80
        cool_pos[0] -= img_size[0] // 2
        cool_pos[1] -= img_size[1] // 2
        screen.blit(img, cool_pos)

    def draw_specific(self, screen):
        self.gfxm.pasteGfxTo(self.__class__.GFX_IDENT, POS_BOITE_LOGIN, screen)

        tmp_pos = (60, 180)
        screen.blit(self.img_head_login, tmp_pos)

        # TODO fix dessin
        # screen.blit(dessin_txt_contraint(self.surface_text,
        #                                  INFO_LOGIN,
        #                                  self.ecriture,
        #                                  (10, 10),
        #                                  self.couleur),
        #             (POS_BOITE_LOGIN[0], POS_BOITE_LOGIN[1] + 50))

        tmp_pos = (60, 445)
        screen.blit(self.img_foot_login, tmp_pos)
        screen.blit(self.img_pseudo, (POS_BOITE_LOGIN[0] + 10, 280))
        screen.blit(self.img_mdp, (POS_BOITE_LOGIN[0] + 10, 315))

        # labels sur boutons
        self.__paste_over_trigger(screen, self.bouton_valider, self.img_valider)
        self.__paste_over_trigger(screen, self.bouton_reset, self.img_annuler)
        self.__paste_over_trigger(screen, self.bouton_inscript, self.img_inscrire)

        # screen.blit(self.img_valider, POS_BOUTON1)
        # screen.blit(self.img_annuler, POS_BOUTON2)
        # screen.blit(self.img_inscrire, POS_BOUTON3)

        self.bouton_valider.draw(screen)
        self.bouton_reset.draw(screen)
        self.bouton_inscript.draw(screen)

    def lookup_ft_specific(self, mouse_button, clickpos):
        if mouse_button == 1:  # clic gauche
            # -- on utilise triggers pour clic sur boutons !
            if self.bouton_valider.contains(clickpos):
                return 0
                #return LOGIN_VALIDATION
            if self.bouton_reset.contains(clickpos):
                return 1
                #return LOGIN_RESET
            if self.bouton_inscript.contains(clickpos):
                return 2
                #return LOGIN_INSCRIPTION

    def renderHeadLogin(self):
        self.img_head_login = self.ecriture.render_txt(
            HEAD_LOGIN,
            True,
            self.couleur
        )

    def renderFootLogin(self):
        self.img_foot_login = self.ecriture.render_txt(
            FOOT_LOGIN,
            True,
            self.couleur
        )

    def renderPseudo(self):
        self.img_pseudo = self.ecriture_titre.render_txt(
            PSEUDO,
            True,
            self.couleur
        )

    def renderMdp(self):
        self.img_mdp = self.ecriture_titre.render_txt(
            MDP,
            True,
            self.couleur
        )

    def renderValider(self):
        self.img_valider = self.ecriture.render_txt(
            VALIDER,
            True,
            self.couleur_sombre
        )

    def renderAnnuler(self):
        self.img_annuler = self.ecriture.render_txt(
            ANNULER,
            True,
            self.couleur_sombre
        )

    def renderInscrire(self):
        self.img_inscrire = self.ecriture.render_txt(
            INSCRIPTION,
            True,
            self.couleur_sombre
        )
