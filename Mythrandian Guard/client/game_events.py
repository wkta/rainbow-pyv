# - use katasdk, only if needed
# import katagames_sdk.katagames_engine as kengi
# kengi = katasdk.kengi
import katagames_engine as kengi


MyEvTypes = kengi.struct.enum(
    'ChallengeStarts',  # is it useful in this project?

    'LackeySpawn',  # contains idx:int -> indication faut changer gfx

    'PlayerBuysItem',
    'WannaBuySkin',  # deprec
    'EquipOwnedSkin',  # deprec

    'FightStarts',

    'MissionStarts',  # contains t, idx
    'MissionEnds',  # contains idx

    'MissionFree',  # only for the view, contains idx

    'AvatarUpdate',  # only here to force view refresh itself
    'NotifyAutoloot'  # contains is_gold, amount
)
