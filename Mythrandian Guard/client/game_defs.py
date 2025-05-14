from artifacts import *
from lackeys import *
# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi


# all global constants
BASE_LIMIT_LACKEYS = 14
INIT_ENERGY_LVL = 5
MAX_MANA_PTS = 8
BG_COLOR = 'antiquewhite3'

# listing of gamestates
GameStates = kengi.struct.enum(
    'MainScreen',
    'Battle',
    'Shopping',
    'Magery'  # collection of artifacts etc.
)

EnchantmentCodes = kengi.struct.enum(
    'Archmage',  # incr. mana regen
    'Blacksmith',  # (temp) lower price on the next armor
    'GoldenTouch',  # incr. gold loot
    'Rooted',  # incr. hp regen
    'SwiftLearner',  # incr. xp
    'Warlord'  # +1 mission slot
)

# - 4 defs here maybe deprecated? Was imported from old codebase
ASSETS_DIR = 'assets'

AvLooks = kengi.struct.enum(
    'OldMan',
    'no4',
    'RiceFarmer',
    'no6',
    'no7',
    'no8',
    'no9',
    'no10',
    'no11',
    'no12',
    'Smith',
    'no14',
    'no15',
    'GrandPa',
    'Amazon',
    'no18',
    'no19',
    'GoldenKnight',
    'no21',
    'no22',
    'Skeleton'
)

SUPPORTED_LOOKS = (
    AvLooks.OldMan,
    AvLooks.RiceFarmer,
    AvLooks.Smith,
    AvLooks.GrandPa,
    AvLooks.Amazon,
    AvLooks.Skeleton,
    AvLooks.GoldenKnight
)

ASSOC_IDPORTRAIT_FILENAME = {
    0: 'portrait3.png',
    2: 'portrait5.png',
    10: 'portrait13.png',
    13: 'portrait16.png',
    14: 'portrait17.png',
    17: 'portrait20.png',
    20: 'portrait23.png'
}
