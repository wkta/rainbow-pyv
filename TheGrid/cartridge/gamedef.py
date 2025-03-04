from . import glvars


pyv = glvars.pyv
pyv.bootstrap_e()  # not done in lanch_game.py ??

from .GameClientPlusGUI import GameClientPlusGUI


# - constants
USER_COMMANDS = {
    pyv.keycodes.K_UP: (0, -1),
    pyv.keycodes.K_DOWN: (0, 1),
    pyv.keycodes.K_LEFT: (-1, 0),
    pyv.keycodes.K_RIGHT: (1, 0)
}
# if sys.argv[1] == 'p1':
    # local_pl, remote_pl = 'p1', 'p2'
# else:
    # local_pl, remote_pl = 'p2', 'p1'
local_pl, remote_pl =  'p1','p2'
GS_HOST = 'localhost'
GS_PORT = 60111

ref_cc = None

def init(vmst=None):
    global ref_cc
    pyv.init(4, wcaption='Roguelike actor-based')
    glvars.screen = pyv.get_surface()
    
    # init network comms, create a model, and force sync it
    netlayer = pyv.neotech.Objectifier(**pyv.neotech.build_net_layer('socket', 'client'))
    netlayer.start_comms(GS_HOST, GS_PORT)

    mediator = pyv.neotech.UMediator()

    mediator.set_network_layer(netlayer)
    pyv.use_mediator(mediator)
    glvars.mediator = mediator

    # demarre GUI+sync réseau (=1er ping)
    ref_cc = GameClientPlusGUI(local_pl)
    ref_cc.force_sync()  # faut penser à sync au démarrage en demandant l'etat
    ref_cc.mediator.update()


def update(curr_t=None):
    """
    you need to use the mediator(umediator)

    while not glvars.game_over:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                glvars.game_over = True
            elif ev.type == pygame.KEYDOWN:
                if ev.key in USER_COMMANDS:
                    p = cc.player_location
                    dx, dy = USER_COMMANDS[ev.key]
                    targetcell = (p[0] + dx, p[1] + dy)
                    cc.request_move(targetcell)
        glvars.mediator.post('paint', '', False)
        # update games_events queue, then refresh the gfx buffer
        cc.mediator.update()
        pygame.display.flip()
    """

    for ev in pyv.event_get():
        if ev.type == pyv.EngineEvTypes.Quit:
            pyv.set_gameover()
        elif ev.type == pyv.EngineEvTypes.Keydown:
            if ev.key == pyv.keycodes.K_ESCAPE:
                pyv.set_gameover()
                continue
            if ev.key in USER_COMMANDS:
                p = ref_cc.player_location
                dx, dy = USER_COMMANDS[ev.key]
                targetcell = (p[0] + dx, p[1] + dy)
                ref_cc.request_move(targetcell)

    #pyv.post_ev('update', info_t=curr_t)
    #pyv.post_ev('paint', '', False)
    # pyv.process_evq()
    ref_cc.mediator.post('update', '', False)
    ref_cc.mediator.post('paint', '', False)
    ref_cc.mediator.update()

    pyv.flip()


def close(vmst=None):
    glvars.mediator.network_layer.shutdown_comms()  # gentle network exit
    pyv.close_game()
    print('TheGrid tech demo: over')
