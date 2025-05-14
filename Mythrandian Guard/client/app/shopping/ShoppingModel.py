import random

import glvars
from game_defs import *
from game_events import MyEvTypes

# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi


class ShoppingModel(kengi.event.CogObj):

    SHOP_SIZE = 5

    def __init__(self):
        super().__init__()
        if glvars.shop_content is None:
            temp_shop = dict()
            cpt = 0
            for _ in range(self.SHOP_SIZE):
                temp_shop[cpt] = random.choice(LackeyCodes.all_codes)
                cpt += 1

            glvars.shop_content = temp_shop

        self._slots = glvars.shop_content

        self._prices = dict()

        for slotnum, code in self._slots.items():
            self._prices[slotnum] = 1+4*lackey_c_to_strength[code]

    def get_price(self, slot_num):
        # returns lackey's price
        return self._prices[slot_num]

    def can_buy_lackey(self, slot_num):
        if glvars.the_avatar.gold < self._prices[slot_num]:
            return False
        if glvars.the_avatar.has_full_team():
            return False
        return True

    def buy_lackey(self, slot):
        cost = self._prices[slot]
        glvars.the_avatar.mod_gold(-cost)
        glvars.the_avatar.add_lackey(self._slots[slot])

        # remplacement
        nouv_code = random.choice(LackeyCodes.all_codes)
        self._slots[slot] = nouv_code
        self._prices[slot] = 1 + 4 * lackey_c_to_strength[nouv_code]
        self.pev(MyEvTypes.LackeySpawn, idx=slot)

        print(glvars.the_avatar.lackeys_desc)

    def __getitem__(self, item):
        return self._slots[item]

    def get_lackeys_for_sale(self):
        """
        :return: dict slot num <> lackey code,
        example
        {
            1: LackeyCodes.Slime, 2: LackeyCodes.Vampire, 3: LackeyCodes.Werewolf, 4: LackeyCodes.Cyclop
        }
        """
        return self._slots
