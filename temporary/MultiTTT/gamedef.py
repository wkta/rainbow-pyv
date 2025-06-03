from . import glvars
from .glvars import pyv
from .actors import *
from .ttt_specific import *


displaysurface = None
coup_ia = None
mouse_pos = None
niveau_IA = 1
police = None
pressed_keys = set()
last_nb_keys = 0
timer_active = False
img_texte = texte2 = None
win_size = None
blocking=False

# -----
#  declare the 3 main functions (mandatory)
def init(**kwargs):
    global displaysurface, police, win_size
    pyv.init(4)

    displaysurface = pyv.get_surface()  # TODO se rapprocher de glvars.TAILLE_FENETRE_PX
    win_size = displaysurface.get_size()

    # menu rudimentaire pour choix du nombre de joueurs
    jeu_contre_IA = True
    print('*** jeu du tic-tac-toe ***')
    # msg_invite = "1 ou 2 joueur(s) humain(s) ?\n"
    # msg_refus = "saisie non reconnue."
    # input_var = input( msg_invite)
    # while ( input_var!='1' and input_var!='2' ):
        # print( msg_refus)
        # input_var = input( msg_invite)
    # if(int(input_var)==2):
        # jeu_contre_IA = False;

    # menu rudimentaire pour choix de la difficulté IA
    niveau_IA = 0
    # if(jeu_contre_IA):
        # niveau_IA = None
        # msg_invite = "type d'adversaire souhaité ?\n0 joueur aléatoire\n1 IA basique\n2 IA balèze\n"
        # input_var = input( msg_invite)
        # while ( input_var!='0' and input_var!='1' and input_var!='2' ):
            # print( msg_refus)
            # input_var = input( msg_invite)
        # niveau_IA = int(input_var)
    
    # declare your custom events here
    pyv.actors.declare_evs(
        'new_nb_pressed_keys', 'timer_start', 'timer_stop', 'color_change'
    )
    print('-' * 32)
    print('press one or two key (any key) to see something cool')
    font_size = 48
    glvars.font_obj = pyv.new_font_obj(None, font_size)  # None -> the defaut font
    new_solid_background()
    glvars.screen_center = (
        pyv.get_surface().get_width()//2,
        pyv.get_surface().get_height()//2
    )
    new_movable_rect(glvars.screen_center)
    new_entities_viewer()
    new_color_viewer()

    print('----- try to press 1, 2 or 3 keys at the same time! ---------')
    print('you can also drag and drop the purple square, for fun. This will play a sound')
    police = pyv.new_font_obj(None, 50)


def update(time_info=None):
    global pressed_keys, last_nb_keys, timer_active, mouse_pos, blocking
    # <>
    # handle events, many operations here are mere forwarding
    for ev in pyv.event_get():
        # forwarding low_level events to events that exist in the mediator
        # a regular game dev should never see this kind of stuff...
        # if ev.type == pyv.EngineEvTypes.Quit:
            # pyv.vars.gameover = True
        # elif ev.type == pyv.EngineEvTypes.Mousedown:
            # pyv.post_ev('mousedown', pos=ev.pos, button=ev.button)  # forward event (low level->game level)
        # elif ev.type == pyv.EngineEvTypes.Mouseup:
            # pyv.post_ev('mouseup', pos=ev.pos, button=ev.button)  # forward event
        # elif ev.type == pyv.EngineEvTypes.Mousemotion:
            # pyv.post_ev('mousemotion', pos=ev.pos, rel=ev.rel)  # forward event
        # elif ev.type == pyv.EngineEvTypes.Keydown and ev.key == pyv.keycodes.K_RETURN:
            # if not timer_active:
                # pyv.post_ev('timer_start')
                # timer_active = True
            # else:
                # pyv.post_ev('timer_stop')
                # timer_active = False
        # elif ev.type == pyv.EngineEvTypes.Keydown and ev.key == pyv.keycodes.K_SPACE:
            # pyv.post_ev('color_change')
        # other not important keys...
        # elif ev.type == pyv.EngineEvTypes.Keydown:
            # pressed_keys.add(ev.key)
        # elif ev.type == pyv.EngineEvTypes.Keyup:
            # if ev.key not in (pyv.keycodes.K_RETURN, pyv.keycodes.K_SPACE):
                # pressed_keys.remove(ev.key)
        if ev.type == pyv.EngineEvTypes.Quit:
            pyv.vars.gameover = True
        elif ev.type == pyv.EngineEvTypes.Mousedown:
            if blocking:
                pyv.vars.gameover = True  # leave the program
            else:
                mouse_pos = ev.pos

    # <>
    # logic update (Sandobox tech demo:)
    # if last_nb_keys is None or len(pressed_keys) != last_nb_keys:  # only if smth changed
        # new_nb = len(pressed_keys)
        # pyv.post_ev('new_nb_pressed_keys', nb=new_nb)  # we forward how many keys are pressed now
        # last_nb_keys = new_nb
    # pyv.post_ev('update', curr_t=time_info)

    # 2- mise à jour de la logique du jeu ("logique de jeu" ou "modèle")
    if glvars.jeu_contre_IA:
        if not glvars.game_over:
            if est_ia_active():
                # à l'ordinateur de jouer...
                if(0==niveau_IA):
                    coup_ia = decision_joueur_alea(get_curr_state())
                elif(1==niveau_IA):
                    coup_ia = decision_IA_moyenne(get_curr_state())
                elif(2==niveau_IA):
                    coup_ia = decision_IA_forte(get_curr_state())
                maj_jeu(coup_ia)
            elif mouse_pos is not None:
                # un humain joue...
                coup_joueur = pixel_vers_case(mouse_pos)
                if(coup_joueur != glvars.CASE_NON_VALIDE): # un clic en dehors de la grille est ignoré
                    if(est_coup_jouable(get_curr_state(), coup_joueur)): # si le coup respecte les règles du tic-tac-toe on va l'appliquer...
                        maj_jeu(coup_joueur)
                mouse_pos = None
        if glvars.game_over:
            gr = get_curr_state()
            #affichage du résultat de la partie, et du message "cliquez pour quitter."
            if est_joueur_vainqueur(gr, 'x'):
                texte_a = 'victoire du joueur "croix"'
            elif est_joueur_vainqueur(gr, 'o'):
                texte_a = 'victoire du joueur "ronds"'
            else:
                texte_a = 'match nul'

            img_texte = police.render(texte_a,True,glvars.BLACK,glvars.FANCY_WHITE)
            posx_a = (win_size[0]-img_texte.get_width())//2
            posy_a = (win_size[1]-img_texte.get_height())//2

            texte_b = 'cliquez pour quitter.'
            posx_b = posx_a
            posy_b = posy_a + img_texte.get_height()
            texte2 = police.render(texte_b,True,glvars.BLACK,glvars.FANCY_WHITE)
            posx = int( win_size[0]/2 - texte2.get_width()/2) #centrer le txt cliquer pr quitter, aussi

    else:
        raise NotImplementedError
    # <>
    # screen/visual update(Sandbox tech demo:)
    # pyv.post_ev('draw', screen=pyv.vars.screen)  # ref. to the screen can also be fetched through:
    # pyv.process_evq()  # process all events that are in stand-by
    
    displaysurface.fill(glvars.FANCY_WHITE)
    dessine_cadre(displaysurface)
    dessine_jeu(displaysurface)
    if glvars.game_over:
        displaysurface.blit(img_texte,(posx_a,posy_a) )
        displaysurface.blit(texte2,(posx_b,posy_b) )
        blocking = True  # once the end msg has been shown, we're ready to quit game for good
        
    pyv.flip()  # always call .flip() at the end of the update function


def close(vmst=None):
    pyv.close_game()
    print('TTT proto has exit properly')
