"""
Definition file for lackeys only
IMPORTANT REMARK:
    this file is not meant to be imported directly, preferably use -> import game_defs
"""

# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi

LackeyCodes = kengi.struct.enum(
    'CaveTroll',
    'Chimera', 'Cyclop', 'FriendlySpider', 'Gargoyle', 'Goblin',
    'Imp', 'Mercenary', 'MountainTroll', 'Slime',
    'SmallOrc', 'Vampire', 'Werewolf', 'Zombie'
)

lackey_c_to_name = LackeyCodes.inv_map

lackey_c_to_strength = {
    LackeyCodes.CaveTroll: 8,
    LackeyCodes.Chimera: 4,
    LackeyCodes.Cyclop: 7,
    LackeyCodes.FriendlySpider: 3, LackeyCodes.Gargoyle: 5, LackeyCodes.Goblin: 4,
    LackeyCodes.Imp: 2, LackeyCodes.Mercenary: 7, LackeyCodes.MountainTroll: 9,
    LackeyCodes.Slime: 1,
    LackeyCodes.SmallOrc: 3, LackeyCodes.Vampire: 8, LackeyCodes.Werewolf: 5,
    LackeyCodes.Zombie: 6
}
