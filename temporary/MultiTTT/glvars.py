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
# put here, all the custom code added by the gamedev
# --------
font_obj = None
screen_center = None
jeu_contre_IA = True
#les 2 variables ci-dessous sont utiles dans le cas d'un jeu contre l'ordinateur

game_over = False

    
# constantes du programme
SYM_IA = 'x' # on attribue au joueur IA l'usage des croix
SYM_HUMAIN = 'o'

BLACK = 'black'
BLUE = 'blue'
CASE_NON_VALIDE = (-1,-1)
CIRCLE_RADIUS = 25
CIRCLE_WIDTH = 6
CROSS_OFFSET = 18
CROSS_WIDTH = 6
EVAL_LOOSE = float('-inf')
EVAL_WIN = float('+inf')
EVAL_TIE = 0.0
FANCY_GRAY = '#7a7076'
FANCY_WHITE = '#f9e7e4'
GRID_LINE_WIDTH = 4
RED = 'red'
TAILLE_CASE_PX = 80
TAILLE_FENETRE_PX = (5*TAILLE_CASE_PX, 3*TAILLE_CASE_PX)
