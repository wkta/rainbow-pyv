# --- constantes pr faire marcher AffichageCred
import pygame
# from core.gui.BaseGuiDecorator import BaseGuiDecorator
# from core.util.atoms.Trigger import Trigger
# from core.util.SharedData import SharedData
# from basis.triggers import TRIG_FOCUS_MAIL, TRIG_FOCUS_PWD, TRIG_CHECKBOX_MEM_MDP
# from core.EventManager import EventManager
# from core.pgu import gui  # framework pour GUI
# from trad_tmp import var_lang
# from gettext import translation
# en = translation('login', localedir='locale', languages=var_lang)
# en.install()

#from prim_gui.Trigger import Trigger


# TODO fix it
class Trigger:
    def __init__(self, fonte, pos, taille):
        pass

    def set_visible(self, bool_val):
        pass


TRIG_FOCUS_MAIL, TRIG_FOCUS_PWD, TRIG_CHECKBOX_MEM_MDP = range(3)

POS_CADRE1 = (180, 274)
POS_CADRE2 = (180, 309)
POS_CADRE3 = (37, 360)
TCADRE = (285, 34)
COORDS_TRIG_SAVING_PWD = (135, 343)
SIZE_TRIG_SAVING_PWD = (20, 20)
ERRCO = "Login et/ou mot de passe incorrect"
SAVEPWD = "Memoriser le mot de passe"
#
#
# class ColorDialog(gui.Dialog):
#     def __init__(self, value, **params):
#         self.value = list(gui.parse_color(value))
#
#         title = gui.Label("Color Picker")
#
#         main = gui.Table()
#
#         main.tr()
#
#         self.color = gui.Color(self.value, width=64, height=64)
#         main.td(self.color, rowspan=3, colspan=1)
#
#         # The sliders CHANGE events are connected to the adjust method.  The
#         # adjust method updates the proper color component based on the value
#         # passed to the method.
#         # ::
#         main.td(gui.Label(' Red: '), 1, 0)
#         e = gui.HSlider(value=self.value[0], min=0, max=255, size=32, width=128, height=16)
#         e.connect(gui.CHANGE, self.adjust, (0, e))
#         main.td(e, 2, 0)
#         ##
#
#         main.td(gui.Label(' Green: '), 1, 1)
#         e = gui.HSlider(value=self.value[1], min=0, max=255, size=32, width=128, height=16)
#         e.connect(gui.CHANGE, self.adjust, (1, e))
#         main.td(e, 2, 1)
#
#         main.td(gui.Label(' Blue: '), 1, 2)
#         e = gui.HSlider(value=self.value[2], min=0, max=255, size=32, width=128, height=16)
#         e.connect(gui.CHANGE, self.adjust, (2, e))
#         main.td(e, 2, 2)
#
#         gui.Dialog.__init__(self, title, main)
#
#     # The custom adjust handler.
#     # ::
#     def adjust(self, value):
#         (num, slider) = value
#         self.value[num] = slider.value
#         self.color.repaint()
#         self.send(gui.CHANGE)
#
#
# class StarControl(gui.Table):
#     def __init__(self, **params):
#         self.evt_m = EventManager.instance()
#
#         gui.Table.__init__(self, **params)
#
#         # def fullscreen_changed(btn):
#         # pygame.display.toggle_fullscreen()
#         #    print("TOGGLE FULLSCREEN")
#
#         def stars_changed(slider):
#             print('SLIDER ACTIVE')
#             # n = slider.value - len(stars)
#             # if n < 0:
#             #     for i in range(n,0):
#             #         stars.pop()
#             # else:
#             #     for i in range(0,n):
#             #         stars.append([random.randrange(-WIDTH*span,WIDTH*span),
#             #                       random.randrange(-HEIGHT*span,HEIGHT*span),
#             #                       random.randrange(1,dist)])
#
#         fg = (255, 255, 255)
#
#         self.tr()
#         self.td(gui.Label("Essai freestyle pgu mini-framework", color=fg), colspan=2)
#
#         self.tr()
#         self.td(gui.Label("Speed: ", color=fg), align=1)
#         e = gui.HSlider(100, -500, 500, size=20, width=100, height=16, name='speed')
#         self.td(e)
#
#         self.tr()
#         self.td(gui.Label("Size: ", color=fg), align=1)
#         e = gui.HSlider(2, 1, 5, size=20, width=100, height=16, name='size')
#         self.td(e)
#
#         self.tr()
#         self.td(gui.Label("Quantity: ", color=fg), align=1)
#         e = gui.HSlider(100, 1, 1000, size=20, width=100, height=16, name='quantity')
#         e.connect(gui.CHANGE, stars_changed, e)
#         self.td(e)
#
#         self.tr()
#         self.td(gui.Label("Color: ", color=fg), align=1)
#
#         default = "#ffffff"
#         color = gui.Color(default, width=64, height=10, name='color')
#         color_d = ColorDialog(default)
#
#         color.connect(gui.CLICK, color_d.open, None)
#         self.td(color)
#
#         def update_col():
#             color.value = color_d.value
#
#         color_d.connect(gui.CHANGE, update_col)
#
#         btn = gui.Switch(value=False, name='fullscreen')
#         # -- pr faire des essais
#         # btn.connect(gui.CHANGE, self.traite_fullscreen, btn)
#
#         self.tr()
#         self.td(gui.Label("Full Screen: ", color=fg), align=1)
#         self.td(btn)
#
#         self.tr()
#         self.td(gui.Label("Warp Speed: ", color=fg), align=1)
#         self.td(gui.Switch(value=False, name='warp'))
#
#     # def traite_fullscreen(self, widget):
#     #     self.evt_m.post(
#     #         TriggerFired(TRIG_FOCUS_PWD)
#     #     )
#     #     print(str(widget))
#
#
# ##Using App instead of Desktop removes the GUI background.  Note the call to app.init()
# ##::
# form = gui.Form()


##You can include your own run loop.
##::
##reset()
##clock = pygame.time.Clock()
##done = False
##while not done:
##    for e in pygame.event.get():
##        if e.type is QUIT: 
##            done = True
##        elif e.type is KEYDOWN and e.key == K_ESCAPE: 
##            done = True
##        else:
##            app.event(e)
##
##    # Clear the screen and render the stars
##    dt = clock.tick(FPS)/1000.0
##    screen.fill((0,0,0))
##    render(dt)
##    
##    pygame.display.flip()
##
##pygame.quit()


from defs import glvars


class DispCredentials:  #(BaseGuiDecorator):
    def __init__(self, vue_fondement, bool_focus_login, login_str, pwd_str):
        drawing_font = glvars.fonts['courier_font']
        #drawing_font = SharedData.instance().fonts['pxled_med_font']
        #p = SharedData.instance()

        #super().__init__(vue_fondement)

        self.CADRE_WIDTH = 2
        self.ecriture = drawing_font
        self.couleur = glvars.colors['deep_purple']
        self.coul_rouge = glvars.colors['rouge']
        self.checkbox_color = glvars.colors['orange']

        self.pos_cadre = None
        self.possib_position_cadre = [
            POS_CADRE1,
            POS_CADRE2,
            POS_CADRE3
        ]

        paddingx = 3
        paddingy = 6
        self.positions_txt = {
            'login': (POS_CADRE1[0] + paddingx, POS_CADRE1[1] + paddingy),
            'pwd': (POS_CADRE2[0] + paddingx, POS_CADRE2[1] + paddingy),
            'errLog': (POS_CADRE3[0] + paddingx, POS_CADRE3[1] + paddingy),
            'savePwd': (COORDS_TRIG_SAVING_PWD[0] + SIZE_TRIG_SAVING_PWD[0] + 10,
                        COORDS_TRIG_SAVING_PWD[1])
        }
        self.deplaceCadreFocus(bool_focus_login)

        self.trig_login = Trigger(self.ecriture, POS_CADRE1, TCADRE)
        self.trig_login.set_visible(False)
        self.trig_pwd = Trigger(self.ecriture, POS_CADRE2, TCADRE)
        self.trig_pwd.set_visible(False)
        self.trig_saving_pwd = Trigger(self.ecriture, COORDS_TRIG_SAVING_PWD, SIZE_TRIG_SAVING_PWD)

        self.img_login = None
        self.img_pwd = None
        self.img_savepwd = None
        self.img_Err_login = None

        self.renderLogin(login_str)
        self.renderPwd(pwd_str)
        self.renderErrorLogin()
        self.renderSavePwd()
        self._erreur_login = False
        self._save_pwd = False

        # self.gfxm = GfxManager.instance()
        # self.gfxm.loadMany(
        #     {
        #         'french_flag': 'french_flag.png',
        #         'us_flag': 'us_flag.png'
        #      }
        #
        # )
        # self.french_but = Widget('french_flag', (0, 0))
        # self.english_but = Widget('us_flag', (150, 0))
        #
        # self.french_but.set_active(True)
        # self.english_but.set_active((True))

        # -- test de GUI "moderne"
        # self.app = gui.App()
        # star_panel = StarControl()  # pr retour GUI
        #
        # c = gui.Container(align=-1, valign=-1)
        # c.add(star_panel, 0, 0)
        #
        # self.app.init(c)

        self.trig_actu = None

    def draw_specific(self, surface):
        # dessin du cadre (focus)

        pygame.draw.rect(
            surface,
            self.couleur,
            (self.pos_cadre[0], self.pos_cadre[1], TCADRE[0], TCADRE[1]),
            self.CADRE_WIDTH
        )

        # dessin des textes
        tmp_pos = self.positions_txt['login']
        surface.blit(self.img_login, tmp_pos)
        tmp_pos = self.positions_txt['pwd']
        surface.blit(self.img_pwd, tmp_pos)
        tmp_pos = self.positions_txt['savePwd']
        surface.blit(self.img_savepwd, tmp_pos)
        if self._erreur_login:
            tmp_pos = self.positions_txt['errLog']
            surface.blit(self.img_Err_login, tmp_pos)

        # dessin des triggers
        self.trig_login.draw(surface)
        self.trig_pwd.draw(surface)
        self.fillSavePwd(surface)
        self.trig_saving_pwd.draw(surface, self.checkbox_color)

        # self.french_but.draw(surface)
        # self.english_but.draw(surface)

        # self.app.paint()

    # hack
    def input_pygame_evt(self, pygame_evt):
        pass
        # self.app.event(pygame_evt)

    def lookup_ft_specific(self, mouse_buttons, clickpos):

        if self.trig_actu is not None:
            tmp = self.trig_actu
            self.trig_actu = None
            print(' ******** retour trigid 999')
            return tmp

        # self.app.event(
        #     pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos':clickpos, 'button':(True,False,False)})
        # )

        if self.trig_login.contains(clickpos):
            return TRIG_FOCUS_MAIL
        elif self.trig_pwd.contains(clickpos):
            return TRIG_FOCUS_PWD
        elif self.trig_saving_pwd.contains((clickpos)):
            return TRIG_CHECKBOX_MEM_MDP

        # if self.french_but.contains(clickpos):
        #     return ID_TRIG_CLICK_FRENCH
        # if self.english_but.contains(clickpos):
        #     return ID_TRIG_CLICK_ENGLISH

        # for ev in ev_list:
        #     if ev.type == MOUSEBUTTONDOWN:
        #         mp = pygame.mouse.get_pos()
        #         if self.bouton_valider.contains(mp):
        #             return CLIC_VALIDATION
        #         if self.bouton_inscript.contains(mp):
        #             return CLIC_INSCRIPTION
        #         if self.bouton_reset.contains(mp):
        #             return CLIC_RESET
        return None

    def renderLogin(self, txt):
        self.img_login = self.ecriture.render_txt(
            txt,
            True,
            self.couleur
        )

    def renderPwd(self, txt):
        self.img_pwd = self.ecriture.render_txt(
            txt,
            True,
            self.couleur
        )

    def renderErrorLogin(self):
        self.img_Err_login = self.ecriture.render_txt(
            ERRCO,
            True,
            self.coul_rouge
        )

    def renderSavePwd(self):
        self.img_savepwd = self.ecriture.render_txt(
            SAVEPWD,
            True,
            self.couleur
        )

    def fillSavePwd(self, surface):
        if self._save_pwd:
            tmp_rect = list()
            tmp_rect.extend(COORDS_TRIG_SAVING_PWD)
            tmp_rect.extend(SIZE_TRIG_SAVING_PWD)
            neg_offset = -2
            tmp_rect[0] -= neg_offset
            tmp_rect[1] -= neg_offset
            tmp_rect[2] += 2 * neg_offset
            tmp_rect[3] += 2 * neg_offset
            pygame.draw.rect(surface, self.checkbox_color, tmp_rect)

    def deplaceCadreFocus(self, focus_login_flag):
        if focus_login_flag:
            self.pos_cadre = self.possib_position_cadre[0]
            return
        self.pos_cadre = self.possib_position_cadre[1]

    def setErreurLogin(self, affiche):
        self._erreur_login = affiche

    def setSavePwd(self, save):
        self._save_pwd = save



