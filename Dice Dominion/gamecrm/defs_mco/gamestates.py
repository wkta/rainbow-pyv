from coremon_main.util import enum_starting_from_zero


GameStates = enum_starting_from_zero(
    'Login',
    'MenuSolo',
    'Conquest'
)
