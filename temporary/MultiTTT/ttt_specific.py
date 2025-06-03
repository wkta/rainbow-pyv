import random
from . import glvars
from .glvars import TAILLE_CASE_PX, CROSS_OFFSET, CROSS_WIDTH, RED, BLUE, CIRCLE_RADIUS, CIRCLE_WIDTH


_grille ='''\
...\
...\
...\
'''
_joueur_courant = random.choice( ('x','o') ) # choix aléatoire du joueur qui commence

pyv = glvars.pyv


# ---------------------
# fonctions utilitaires
# ---------------------
def get_curr_state():
    return _grille


def adversaire(joueur_x):
    if('o'==joueur_x):
        return 'x'
    return 'o'

def case_vers_pixel(case):
    i,j = case
    i += 1; j += 1 #on incrémente i et j
    x = i * TAILLE_CASE_PX +(TAILLE_CASE_PX//2)
    y = j * TAILLE_CASE_PX +(TAILLE_CASE_PX//2)
    return (x,y)


def est_ia_active():
    return glvars.SYM_IA==_joueur_courant


def maj_jeu(coup_joue):
    global _grille, _joueur_courant
    _grille = joue_coup(_grille, coup_joue, _joueur_courant)
    if est__grille_pleine(_grille) or est_joueur_vainqueur(_grille,_joueur_courant): # le coup joué met-il fin à la partie?
        glvars.game_over = True
        return
    # on passe la main
    _joueur_courant = adversaire(_joueur_courant)
    print('nouv joueur:', _joueur_courant)


def pixel_vers_case(pixel):
    x,y = pixel
    tempi = x//TAILLE_CASE_PX
    tempj = y//TAILLE_CASE_PX
    if(tempi <1 or tempi >3 or tempj <1 or tempj >3):
        return glvars.CASE_NON_VALIDE
    i = tempi -1
    j = tempj -1
    return (i,j)


# --- fonctions au service de l'IA
# --------------------------------
def decision_joueur_alea(position):
    possib = det_liste_possib(position)
    return random.choice( possib)

def decision_IA_moyenne(position):
    # on va calculer les coups adverses qui nous feraient perdre
    menaces = list()
    possib_ia = det_liste_possib(position)
    for coup_ia_envisage in possib_ia: #pour chaque coup que pourrait jouer l'IA
        position1 = joue_coup(position, coup_ia_envisage, glvars.SYM_IA)
        possib_humain = det_liste_possib(position1)
        for coup_h_envisage in possib_humain: #pour chaque coup que pourrait jouer l'humain
            position2 = joue_coup(position1, coup_h_envisage, glvars.SYM_HUMAIN)
            if est_joueur_vainqueur(position2, glvars.SYM_HUMAIN): # si l'humain gagne...
                menaces.append( coup_h_envisage)
    
    if(len(menaces)>0):
        return random.choice(menaces) #en jouant soi-même sur la case où se trouve une menace, on joue défensivement
    
    #si aucune menace repérée, on se contente d'un choix aléatoire
    return decision_joueur_alea(position)

def decision_IA_forte(position):
    # on peut déduire (en faisant des tests avec minimax) que jouer dans les coins
    # est un coup initial qui offre un maximum de possibilités de victoire.
    # Par conséquent, autant toujours commencer la partie de cette façon.
    if( '.........'==position ): # si _grille vide
        l_coins = [ (0,0),(2,0),(2,2),(0,2) ]
        return random.choice( l_coins)

    #on se trouve au niveau 0 de l'arbre, la racine, du point de vue minimax, c'est un niveau max
    coups_jouables = det_liste_possib(position)
    max_score= None
    meilleur_coup = None
    for c in coups_jouables:
        psimulee = joue_coup(position, c, glvars.SYM_IA)
        tmp_score = feval(psimulee, 1)
        print(c,tmp_score)
        if(meilleur_coup==None or tmp_score>max_score):
            max_score=tmp_score
            meilleur_coup = c
    print('meilleur coup: '+str(meilleur_coup) )
    return meilleur_coup

def feval(position , profondeur ): #fonction récursive évaluation + minimax
    if (profondeur%2)==1:
        niveau_mini = True
    else:
        niveau_mini = False
        
    #conditions d'arrêt pour la récursion
    if(est_joueur_vainqueur(position, glvars.SYM_HUMAIN)):
        return EVAL_LOOSE
    if(est_joueur_vainqueur(position, glvars.SYM_IA)):
        return EVAL_WIN
    if(est__grille_pleine(position)):
        return EVAL_TIE
    
    #si les tests ci-dessus n'ont rien donné, il faut explorer les nœuds plus en profondeur
    # --- implémentation de la méthode minimax
    coups_jouables = det_liste_possib(position)
    
    if(niveau_mini): #l'humain joue, il cherche à minimiser l'évaluation
        min_score = None
        for c in coups_jouables:
            psimulee = joue_coup(position, c, glvars.SYM_HUMAIN)
            tmp_score = feval(psimulee, profondeur+1)
            if( None==min_score or tmp_score<min_score ):
                min_score = tmp_score
        return min_score
    
    #l'ordi joue, il cherche à maximiser l'évaluation
    max_score = None
    for c in coups_jouables:
        psimulee = joue_coup(position, c, glvars.SYM_IA)
        tmp_score = feval(psimulee, profondeur+1)
        if( None==max_score or tmp_score>max_score):
            max_score=tmp_score
    return max_score


# --- définition de fonctions gérant la position de jeu
# -----------------------------------------------------
def det_liste_possib(position ):
    """retourne la liste de coups possible (taille entre 1 à 8), un coup étant un couple (i,j)"""
    candidats = []
    for i in range(3):
        for j in range(3):
            if est_coup_jouable(position,(i,j)):
                candidats.append( (i,j))
    print('candidats:', candidats)
    return candidats

def est_coup_jouable(position, case_envisagee):
    i,j= case_envisagee
    index_cible = 3*j+ i
    return ('.'==position[index_cible]) #si la case envisagée est libre alors le coup est jouable

def est__grille_pleine(position):
    """retourne vrai ou faux"""
    for ind in range(len(position)):
        if('.'==position[ind]):
            return False
    return True

def est_joueur_vainqueur(position, j_considere):
    config_qui_gagnent = [
        [0,1,2], [3,4,5], [6,7,8], #victoire suivant une ligne
        [0,3,6], [1,4,7], [2,5,8], #victoire suivant une colonne
        [0,4,8], [2,4,6] ] #victoire suivant une diagonale
    for conf in config_qui_gagnent:
        i,j,k = conf
        if(j_considere==position[i] and j_considere==position[j] and j_considere==position[k]):
            return True
    return False

def joue_coup(position, case, signe):
    """étant donnée une position du jeu (c-à-d une _grille sous forme de chaîne de caractères),
    on retourne une nouvelle position où le signe 'o' / 'x' a été ajouté dans une certaine case"""
    i,j= case
    index_cible = 3*j+ i
    tmp = list(position)
    tmp[index_cible] = signe
    return ''.join(tmp)


# --- Définition de fonctions gérant l'affichage
# ----------------------------------------------
def affiche_croix(surface,case):
    #dessin en utilisant pygame.draw.line(Surface, color, start_pos, end_pos, width=1) -> Rect
    x,y = case_vers_pixel(case)
    coin_hg = (x - CROSS_OFFSET, y - CROSS_OFFSET)
    coin_hd = (x + CROSS_OFFSET, y - CROSS_OFFSET)
    coin_bg = (x - CROSS_OFFSET, y + CROSS_OFFSET)
    coin_bd = (x + CROSS_OFFSET, y + CROSS_OFFSET)
    pyv.draw_line(surface, RED, coin_hg, coin_bd, CROSS_WIDTH)
    pyv.draw_line(surface, RED, coin_bg, coin_hd, CROSS_WIDTH)

def affiche_rond(surface, case):
    #dessin en utilisant pygame.draw.circle(Surface, color, pos, radius, width=0) -> Rect
    pyv.draw_circle(surface, BLUE, case_vers_pixel(case), CIRCLE_RADIUS, CIRCLE_WIDTH)

def dessine_cadre(surface):
    """dessine deux colonnes, deux lignes qui se croisent"""
    org_col1 = (  2*TAILLE_CASE_PX, 1*TAILLE_CASE_PX )
    fin_col1 = (  2*TAILLE_CASE_PX, 4*TAILLE_CASE_PX )
    org_col2 = (  3*TAILLE_CASE_PX, 1*TAILLE_CASE_PX )
    fin_col2 = (  3*TAILLE_CASE_PX, 4*TAILLE_CASE_PX )
    pyv.draw_line(surface, glvars.FANCY_GRAY, org_col1, fin_col1, glvars.GRID_LINE_WIDTH)
    pyv.draw_line(surface, glvars.FANCY_GRAY, org_col2, fin_col2, glvars.GRID_LINE_WIDTH)

    org_ligne1 = (  1*TAILLE_CASE_PX, 2*TAILLE_CASE_PX )
    fin_ligne1 = (  4*TAILLE_CASE_PX, 2*TAILLE_CASE_PX )
    org_ligne2 = (  1*TAILLE_CASE_PX, 3*TAILLE_CASE_PX )
    fin_ligne2 = (  4*TAILLE_CASE_PX, 3*TAILLE_CASE_PX )
    pyv.draw_line(surface, glvars.FANCY_GRAY, org_ligne1, fin_ligne1, glvars.GRID_LINE_WIDTH)
    pyv.draw_line(surface, glvars.FANCY_GRAY, org_ligne2, fin_ligne2, glvars.GRID_LINE_WIDTH)    

def dessine_jeu(surface):
    global _grille
    position = _grille
    for i in range(3):
        for j in range(3):
            index_cible = 3*j+ i
            if('o'==_grille[index_cible]):
                affiche_rond(surface,(i,j))
            elif('x'==_grille[index_cible]):
                affiche_croix(surface,(i,j))
