# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi
from katagames_engine.Singleton import Singleton
from game_defs import ArtifactNames


@Singleton
class ArtifactStorage:
    """
    Aims at easing a specific info. storage
    (info. about the artifact parts collection)
    internally it uses an obj whose precise format is
        {
            ArtifactCodes.KingsPlate: {
                1: 0,  # part 1 -> Breastplate
                2: 0,  # part 2... etc
                3: 0,
                4: 0,
                5: 0,
            },
            ...
        }
    """

    def __init__(self):
        self._irepr = dict()
        for code in ArtifactNames.keys():
            self._irepr[code] = dict()
            for idx in ArtifactNames[code].keys():
                if idx:
                    self._irepr[code][idx] = 0

    def collect(self, art_code, element, quant=1):
        self._irepr[art_code][element] += quant

    def get_quant(self, code, elt_no):
        return self._irepr[code][elt_no]
