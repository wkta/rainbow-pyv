import random
import game_defs
from app.magery.ArtifactStorage import ArtifactStorage
from game_defs import LackeyCodes, MAX_MANA_PTS, BASE_LIMIT_LACKEYS, INIT_ENERGY_LVL


class BelongingsMod:
    """
    Models all resources collected + avatar's belongings
    this incudes lackeys

    - gold pieces
    - rep points
    - mana

    - equipment

    - artifacts (collectibles)
    - lackeys
    """

    def __init__(self, gp, rep, mana, energy=None, lackey_list=None):
        self.gold = gp
        self.rep = rep
        self.mana = mana if mana < MAX_MANA_PTS else MAX_MANA_PTS  # capped quantity
        if energy:
            self.energy = energy
        else:
            self.energy = INIT_ENERGY_LVL

        self._eq_items = {
            'head': None, 'hands': None, 'torso': None, 'legs': None
        }

        self.artifact_parts = ArtifactStorage.instance()
        self.whole_artifacts = dict()

        for ac in game_defs.ArtifactCodes.all_codes:
            self.whole_artifacts[ac] = 0  # quantities

        if lackey_list:
            self.lackeys = lackey_list
        else:  # starting with 0 lackey
            self.lackeys = [None for _ in range(BASE_LIMIT_LACKEYS)]

    def debug_give_random_lackeys(self):
        self.lackeys[0] = LackeyCodes.SmallOrc
        if random.random() < 0.6:
            self.lackeys[1] = LackeyCodes.FriendlySpider
            if random.random() < 0.6:
                self.lackeys[2] = LackeyCodes.Slime
                if random.random() < 0.5:
                    self.lackeys[3] = LackeyCodes.MountainTroll

    def describe_lackeys(self):
        res = ''
        cpt = 0
        for t in self.lackeys:
            if t:
                cpt += 1
        res += '{} lackeys'.format(cpt)
        if cpt:
            res += ':\n'
        for ii in range(cpt):
            # lackey code, to str
            res += ' - {}'.format(LackeyCodes.inv_map[self.lackeys[ii]])
            if ii != cpt-1:
                res += '\n'
        return res
