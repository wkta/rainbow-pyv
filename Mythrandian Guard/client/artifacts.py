# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi


"""
Definition file for artifacts only
IMPORTANT REMARK:
    this file is not meant to be imported directly, preferably use -> import game_defs
"""


ArtifactCodes = kengi.struct.enum(
    'KingsPlate',
    'Relics',
    'StaffNin',
)

ArtifactNames = {
    ArtifactCodes.KingsPlate: {
        0: 'Luriel\'s Outfit',  # 0 -> artifact's name, always
        # list of reagents
        1: 'Antique Breastplate',
        2: 'Antique spaulders',
        3: 'Antique Sallet',
        4: 'Silver Scepter',
    },
    ArtifactCodes.Relics: {
        0: 'Relics of Matangi',

        1: 'Loincloth',
        2: 'Club',
        3: 'Shield',
        4: 'Necklace'
    },
    ArtifactCodes.StaffNin: {
        0: 'Antique Staff of Nin',

        1: 'The head',
        2: 'Ash wood stick'
    }
}
