# ------
# engine-related code, do not modify!
# --------

registry = set()
libname_to_alias_mapping = dict()

def get_alias(origin_lib_name):
    return libname_to_alias_mapping[origin_lib_name]

def has_registered(origin_lib_name):
    return origin_lib_name in libname_to_alias_mapping

def register_lib(alias, libname, value):  # handy for dependency injection
    global registry, libname_to_alias_mapping
    libname_to_alias_mapping[libname] = alias
    if alias in registry:
        raise KeyError(f'Cannot register lib "{alias}" more than once!')
    globals()[alias] = value
    registry.add(alias)


# ------
# custom code the gamedev added
# --------

blocks_pop = None
prev_time_info = None
end_game_label = None  # != None means player cannot move bc he/she lost

scr_width = scr_height = None  # will be set right after the .init in the main program
bgcolor = None  # will be set after engine initialization

# (Size of break-out blocks)
BLOCK_W = 36
BLOCK_H = 16
BLOCK_SPACING = 1
#SCR_WIDTH = 960 SCR_HEIGHT = 720
# LIMIT = SCR_WIDTH / (BLOCK_W + BLOCK_SPACING)
WALL_X, WALL_Y = 3, 41

# physics
PL_WIDTH, PL_HEIGHT = 60, 8
PLAYER_SPEED = 125.0

MAX_SPEED_BALL = 145.0
YSPEED_BALL = 84.333

# ball-related
BALL_SIZE = 8
