import os

import game_defs
# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi

from app.shopping.ShoppingModel import ShoppingModel
from game_defs import lackey_c_to_name, AvLooks, SUPPORTED_LOOKS, ASSETS_DIR, LackeyCodes, ASSOC_IDPORTRAIT_FILENAME
from game_events import MyEvTypes


pygame = kengi.pygame
EngineEvTypes = kengi.event.EngineEvTypes
EventReceiver = kengi.event.EventReceiver


class MiniDispPortraits:
    # recyclage du DispShop écrit par Paul...

    TRIG_SIZE = (85, 20)
    NB_ITEM_PER_LINE = 7
    POS_INIT = (44, 200)
    POS_RAPPEL_PESOS = (25, 120)
    POS_MESSAGE = (420, 635)
    OFFSET_Y_PORTRAITS = 40
    OFFSET_Y_ITEMS = 10
    DECAL_Y_2E_LIGNE = 100

    temp_lcode2asset = dict()

    def __init__(self, ref_shop_model, id_portrait_actuel):

        if len(self.temp_lcode2asset) == 0:  # one-time init
            tmptmp = list()
            for skin_code in SUPPORTED_LOOKS:
                kengi.gui.WidgetBo.link_resource(  # bind gfx id. to a surface u can retrieve via .getSurface()
                    self._to_gfxid(skin_code), os.sep.join((ASSETS_DIR, ASSOC_IDPORTRAIT_FILENAME[skin_code]))
                )
                tmptmp.append(self._to_gfxid(skin_code))
            # bind lackeycode to gfxid
            cpt = 1
            n_const = len(tmptmp)
            for lc in LackeyCodes.all_codes:
                self.temp_lcode2asset[lc] = tmptmp[cpt]
                cpt = (cpt + 1) % n_const

        # - reste du constructeur -
        self.pos_legende = [32, 128]
        self.pos_legende[1] += self.DECAL_Y_2E_LIGNE
        self._ref_mod = ref_shop_model

        # fonts
        self.big_font = pygame.font.Font(None, 30)
        self.desc_font = pygame.font.Font(None, 22)

        # --- Gestion du portrait actuel
        self.id_portrait_actuel = id_portrait_actuel

        # --- Items et portraits proposés
        self.li_prix_items = None
        self.li_triggers = self.li_icons = self.li_label_prices = None

        self.assoc_trigger_slotnum = dict()
        self.li_icons = list()
        self.li_label_prices = list()
        self.li_label_names = list()
        self.li_triggers = list()
        self.refresh_disp_offers()  # peuple les 3 listes ci-dessus

        self.message = self.big_font.render("", True, 'BLACK')
        self.wanna_buy_thing_id = None  # Récupéré par ctrl, pour éviter de déclarer 2 * 7 triggers
        self.label_legende_1er_ligne = self.big_font.render(
            'achat ?',
            True,
            'BLACK'
        )

    def refresh_disp_offers(self):
        """
        Génère les widgets, labels, et triggers de l'affichage
        Normalement appelée uniquement dans le constructeur
        :return:
        """
        # purge
        self.assoc_trigger_slotnum.clear()
        del self.li_icons[:]
        del self.li_label_prices[:]
        del self.li_label_names[:]
        del self.li_triggers[:]

        # re-fill
        for cpt in range(ShoppingModel.SHOP_SIZE):
            x, y = self.pos_case_vers_pos_ecran(cpt)
            curr_lackey_code = self._ref_mod[cpt]

            # widget -
            img = kengi.gui.WidgetBo(
                self.temp_lcode2asset[curr_lackey_code],
                (x, y - 50)
            )  # comme une image facile a manipuler, maybe cliquable

            # labels: cout, nom
            cout = self._ref_mod.get_price(cpt)
            texte_adhoc = MiniDispPortraits._formatte_cout(cout)
            lbl = self.desc_font.render(texte_adhoc, True, 'DARKRED')
            tmp_pos_lbl = (x - 15, y + 68)

            lbl_lackey_name = self.desc_font.render(
                lackey_c_to_name[curr_lackey_code], True, 'DARKRED'
            )
            tmp_pos2 = (x - 15, y + 44)

            # "bouton"/trigger
            buy_trig = kengi.gui.Trigger((x, y + 100), self.TRIG_SIZE)
            buy_trig.setLabel('Buy')

            # - cest ce bloc qui est essentiel -
            self.li_icons.append(img)
            self.li_label_prices.append((lbl, tmp_pos_lbl))
            self.li_label_names.append((lbl_lackey_name, tmp_pos2))
            self.li_triggers.append(buy_trig)
            self.assoc_trigger_slotnum[buy_trig] = cpt

    @classmethod
    def _to_gfxid(cls, skin_code):
        return 'skin_portrait{}x2'.format(skin_code)

    def informe_achat_item(self, skin_code):
        skin_name = AvLooks.inv_map[skin_code]
        txt = "Achat du skin {} >> OK".format(skin_name)
        self.message = self.big_font.render(txt, True, 'BLACK')
        self.wanna_buy_thing_id = None
        self.refresh_disp_offers()
        # trig_a_changer = self.assoc_iditem_trigger[skin_code]
        # trig_a_changer.setLabel('Activate')

    def feedback_achat_portrait(self):
        txt = "Achat du portrait OK"
        self.message = self.big_font.render(txt, True, 'BLACK')
        self.wanna_buy_thing_id = None

    def feedback_trop_cher(self):
        txt = "Pas assez de ressources! ($ ou MOBI)"
        self.message = self.big_font.render(txt, True, (255, 0, 0))

    def feedback_inventaire_plein(self):
        txt = "L'inventaire est plein"
        self.message = self.big_font.render(txt, True, (255, 0, 0))

    def feedback_portrait_possede(self):
        txt = "Vous possédez déjà ce portrait"
        self.message = self.big_font.render(txt, True, (255, 0, 0))

    @staticmethod
    def _formatte_cout(cout_infos):
        assert cout_infos is not None
        return '{} $'.format(cout_infos)

    def pos_case_vers_pos_ecran(self, num_case):
        """
        :param num_case: Numéro de la case dans la liste d'items à acheter dans le shop
        :return: Un couple x,y indiquant la position du coin supérieur gauche de l'image de l'item/portrait sur la map
        """
        linerank = num_case % self.NB_ITEM_PER_LINE
        x, y = self.POS_INIT
        y += self.DECAL_Y_2E_LIGNE
        x += 192 * linerank
        return x, y

    def is_slot_clicked(self, clickpos):
        for trigger_obj, num_slot in self.assoc_trigger_slotnum.items():
            if trigger_obj.contains(clickpos):
                return num_slot

    def get_wanna_buy_thing_id(self):
        return self.wanna_buy_thing_id

    def do_paint(self, scr):
        for widg in self.li_icons:
            widg.draw(scr)

        for lbl in self.li_label_prices:
            text, pos = lbl
            scr.blit(text, pos)
        for lbl in self.li_label_names:
            text, pos = lbl
            scr.blit(text, pos)

        for trig in self.li_triggers:
            trig.draw(scr, 'DARKRED')

        scr.blit(self.label_legende_1er_ligne, self.pos_legende)
        scr.blit(self.message, self.POS_MESSAGE)


class ShoppingView(EventReceiver):

    def __init__(self, ref_mod2, id_portrait_actuel):
        super().__init__()
        self.ref_mod2 = ref_mod2
        self.disp2 = MiniDispPortraits(self.ref_mod2, id_portrait_actuel)  # TODO simplification!

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            scr = ev.screen

            scr.fill(game_defs.BG_COLOR)
            self.disp2.do_paint(scr)

        elif ev.type == pygame.MOUSEBUTTONUP:
            tmp = self.disp2.is_slot_clicked(ev.pos)

            if tmp is not None:
                if self.ref_mod2.can_buy_lackey(tmp):
                    print('passe ordre achat')
                    self.ref_mod2.buy_lackey(tmp)

                    # TODO effet graphique

        elif ev.type == MyEvTypes.LackeySpawn:
            self.disp2.refresh_disp_offers()

    def signale_achat_ok(self, skin_code):
        self.disp2.informe_achat_item(skin_code)

    def signale_trop_cher(self):
        self.disp2.feedback_trop_cher()

    def signale_portrait_possede(self):
        self.disp2.feedback_portrait_possede()
