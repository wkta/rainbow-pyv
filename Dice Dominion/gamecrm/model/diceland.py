from gamecrm.model.Land import Land
from gamecrm.model.Dice6 import Dice6


class DiceLand(Land):
    """
    Specialist version of the Land. It can hold a number of Dices and provides
    a method to roll them.
    """
    def __init__(self, world, given_landid=None):  # pouvoir spec id pour la déserialisation -> important
        """
        Same as for Land.
        """
        # print('building diceland with id {}'.format(land_id))
        super().__init__(world, given_landid)
        self._dices = []    # list of dice object on this land
        
    def _get_num_dices(self):
        """
        Returns the number of dices.
        """
        return len(self._dices)
    num_dice = property(_get_num_dices, doc="number of dices, read only")
    
    def roll_dice(self):
        """
        rollDice() -> (pips1, pips2, ...,), sumOfPips
        Returns a list of all Results of the dices and at the end the Sum of 
        all pips.
        """
        pips_sum = 0
        res = []
        for mdice in self._dices:
            pips = mdice.roll()
            pips_sum += pips
            res.append(pips)
        return res, pips_sum
        
    def _add_dice(self):
        """
        Adds a Dice to this Land.
        """
        obj = Dice6()
        self._dices.append(obj)
    
    def set_num_dice(self, num=1):
        del self._dices[:]  # the _dices list gets a reset
        for k in range(num):
            self._add_dice()
        return len(self._dices)

    # def remove_dice(self):
    #     Removes a Dice from this Land.
    #     Returns the number of left dices.
    #     try:
    #         self._dices.pop()
    #     except:
    #         pass
    #     return len(self._dices)
