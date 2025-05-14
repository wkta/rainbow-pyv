import random
import time
import glvars
# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi

from app.main_screen.models import Artifact
from game_events import MyEvTypes


class MissionLoot:
    """
    After completing a mission,
    sometimes the player can choose between 2-3 rewards,
    sometimes he just gets extra gold.

    When you're choosing you can select:
    bonus xp
    bonus gold
    potion of mana (small, sometimes LARGE)
    or an artifact (when this occurs other bonuses are doubled)
    """

    def __init__(self, extra_xp, extra_gold, extra_mana, artifact):
        self._xp = extra_xp
        self._gold = extra_gold
        self._mana = extra_mana
        self._artifact = artifact

    def is_choice_less(self):
        """
        if there's only / gold in the loot, therefore there is no choice
        """
        if self._xp is not None:
            if self._gold or self._mana or self._artifact:
                return False
        if self._gold is not None:
            if self._xp or self._mana or self._artifact:
                return False
        return True

    def has_gold(self):
        return self._gold is not None

    @property
    def gold(self):
        return self._gold

    @property
    def xp(self):
        return self.xp

    def claim(self):
        if self._gold:
            glvars.the_avatar.mod_gold(self._gold)
        if self._xp:
            glvars.the_avatar.add_xp(self._xp)
        if self._artifact:
            glvars.the_avatar.add_artifact(self._artifact)
        # TODO mana

    @classmethod
    def gen_random(cls, mission_diff):
        """
        PROBA. TABLE

        0.033: artifact
        0.13: mana

        (things that stack)
        0.75: regular gold amount
        complement: regular xp amount
        """
        ptable = {
            0: 0.025,
            1: 0.10,
            2: 0.87
        }
        rem_loot_elt = 4
        # variables(4)
        # qui contiennent ensemble la future carte(comme une menu) des loot
        arti, mana, gold, xp = None, 0, 0, 0

        # limites de difficulte basees sur progression 2, 3, 5, 8, 13, 21
        nb_lancers = 4
        if mission_diff > 21:
            nb_lancers -= 3
        elif mission_diff > 13:
            nb_lancers -= 2
        elif mission_diff > 8:
            nb_lancers -= 1
        for _ in range(nb_lancers):
            if random.random() < ptable[0]:
                arti = Artifact.gen_random()
                rem_loot_elt -= 1
                break

        if mission_diff > 13 and random.random() < ptable[1]:
            mana += 1
            rem_loot_elt -= 1
        if mission_diff > 21 and random.random() < ptable[1]:
            mana += 1
            rem_loot_elt -= 1

        while rem_loot_elt > 0:
            if random.random() < ptable[2]:
                gold += random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
            else:
                xp += int(3 * mission_diff**2)
            rem_loot_elt -= 1

        gold = int(gold * mission_diff)

        # special case: artifact => double other rewards, mana+2
        if arti is not None:
            if mana:
                mana += 2
            if gold:
                gold *= 2
            if xp:
                xp *= 2

        if mana and (gold > 0):
            gold += int(mana * mission_diff)
        if xp > 0:
            gold = int(gold*0.85)

        # None instead of 0
        mana = mana if mana else None
        gold = gold if gold else None
        xp = xp if xp else None
        return cls(xp, gold, mana, arti)

    def __str__(self):
        res = 'LOOT rewards:\n'
        if self._xp:
            res += 'xp: {}\n'.format(self._xp)
        if self._gold:
            res += 'gold: {}\n'.format(self._gold)
        if self._mana:
            res += 'mana: {}\n'.format(self._mana)
        if self._artifact:
            res += str(self._artifact) + '\n'
        return res


class MissionSetModel(kengi.event.CogObj):  # it holds the state of missions
    """
    3 missions at the same time
    """

    def __init__(self):
        super().__init__()
        self._ongoing_missions = {
            1: 0,
            2: 0,
            3: 0
        }
        self._difficulties = {
            1: 1.1,
            2: 1.5,
            3: 2.25
        }
        self._temp_loots = dict()

    def start_mission(self, index):
        print('mission {} starts!'.format(index))
        self._ongoing_missions[index] = 1
        self.pev(MyEvTypes.MissionStarts, t=time.time(), idx=index)

    def flag_mission_done(self, index):
        print('mission {} done!'.format(index))
        self._ongoing_missions[index] = -1

        self._temp_loots[index] = obj_loot = MissionLoot.gen_random(self._difficulties[index])
        self._difficulties[index] *= 1.07

        if obj_loot.is_choice_less():
            if obj_loot.has_gold():
                self.pev(MyEvTypes.NotifyAutoloot, is_gold=True, amount=obj_loot.gold)
            else:
                self.pev(MyEvTypes.NotifyAutoloot, is_gold=False, amount=obj_loot.xp)
            self.claim_reward(index)
        else:
            self.pev(MyEvTypes.MissionEnds, idx=index)

    def is_m_open(self, index):
        return 0 == self._ongoing_missions[index]

    def is_m_locked(self, index):
        return 1 == self._ongoing_missions[index]

    def is_m_over(self, index):
        return -1 == self._ongoing_missions[index]

    def _reset_m_state(self, idx):
        if not self.is_m_over(idx):
            raise Exception
        self._ongoing_missions[idx] = 0  # reset state
        del self._temp_loots[idx]

    def claim_reward(self, index):
        print(self._temp_loots[index])
        self._temp_loots[index].claim()

        self._reset_m_state(index)
        self.pev(MyEvTypes.MissionFree, idx=index)
