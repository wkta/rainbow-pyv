import random

from coremon_main.Singleton import Singleton
from coremon_main.events import CgmEvent, EventManager
from gamecrm.defs_mco.ev_types import MyEvTypes


@Singleton
class GlobOwnershipLands:
    """
    useful to record who owns what land
    """

    def __init__(self):
        self._nb_players = None
        self._land_ownership = dict()
        self._manager = EventManager.instance()

    @property
    def total(self):
        return len(self._land_ownership)

    def transfer(self, landid, new_owner_code):
        if landid not in self._land_ownership:
            raise ValueError('cannot find landid')
        if new_owner_code is None or (not isinstance(new_owner_code, int)):
            print(new_owner_code)
            raise ValueError('invalid new_owner_code!')

        self._land_ownership[landid] = new_owner_code

    def rand_giveaway(self, li_land_ids, nb_players=2):
        # random allocation
        self._nb_players = nb_players
        self._land_ownership.clear()
        print('ids to affect: '+str(len(li_land_ids)))

        nb_lands = len(li_land_ids)
        base_num = nb_lands // nb_players
        remainder = nb_lands % nb_players
        random.shuffle(li_land_ids)

        for plcode in range(nb_players):
            for _ in range(base_num):
                self._land_ownership[li_land_ids.pop()] = plcode
        for _ in range(remainder):
            self._land_ownership[li_land_ids.pop()] = random.randint(0, nb_players-1)

        print('unaffected ids: '+str(len(li_land_ids)))
        print('exiting rand_giveaway')

    def calc_score(self, plcode):
        cpt = 0
        for landid, owner in self._land_ownership.items():
            if owner == plcode:
                cpt += 1
        return cpt

    def list_land_ids(self, plcode):
        newlist = list()
        for landid, owner in self._land_ownership.items():
            if owner == plcode:
                newlist.append(landid)
        return newlist

    def serialize(self):
        res_serial = '{'

        nb_elt = len(self._land_ownership)
        for lid, plcode in self._land_ownership.items():
            if nb_elt == 1:
                formatadhoc = '"{}":{}'
            else:
                formatadhoc = '"{}":{}, '
            nb_elt -= 1
            res_serial += formatadhoc.format(lid, plcode)

        res_serial += '}'
        return res_serial

    def inject_state(self, dict_state):
        self._land_ownership.clear()
        unique_codes = set()

        for landid, plcode in dict_state.items():
            unique_codes.add(plcode)
            self._land_ownership[int(landid)] = plcode

        self._nb_players = len(unique_codes)

    def __str__(self):
        res = ''
        for k in range(self._nb_players):
            res += "** owner {} **\n".format(k)
            for landid, owner in self._land_ownership.items():
                if owner == k:
                    res += f"   %d \n" % landid
            res += "\n"
        return res

    def __getitem__(self, landid) -> int:
        """
        given a landid, tells what player owns it!
        """
        return self._land_ownership[landid]


def test_ownership():
    own = GlobOwnershipLands.instance()
    nbpl = 3
    own.rand_giveaway(list(range(10, 18)) + [99, 111], nbpl)
    print(own)
    for testval in (111, 10, 17):
        print('who has land {}? Its player {}'.format(testval, own[testval]))
    print('who has 4+ lands?')
    for plcode in range(nbpl):
        if own.calc_score(plcode) >= 4:
            print('player {} does!'.format(plcode))
    print(' * * * SERIAL * * *')
    print(own.serialize())


if __name__ == "__main__":
    test_ownership()
