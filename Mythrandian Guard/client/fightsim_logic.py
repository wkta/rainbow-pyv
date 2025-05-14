"""
fight simulator (Game Logic)
this will be used both in mission & PvP (raids).

ONE RULE: keep it simple!
this rule is very important since the game logic will be coded a second time
on the server (PHP lang.)

So the following file works just like a complex MATH function with many parameters.
-> input= Two sets of fighters
<- output= history of the fight so you can "re-play" it and compute the winner
"""
import pygame
from app.battle.bmodel import Battle, Team, GenFighter
from fightsim_view import draw_fighters


def run_simu():
    # model debug test valeurs extremes
    for lvl in (1, 59):
        for en in (1, 10):
            tf = GenFighter(lvl, 1, en)
            print(tf)

    print()
    print('----------- * * * -')

    # init pygame, init real model
    w = pygame.display.set_mode((960, 540))

    b = Battle.sample_example()

    # game loop
    gameover = False
    turn = 1
    can_update = False
    while not gameover:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                gameover = True
            elif ev.type == pygame.KEYDOWN and pygame.K_SPACE == ev.key:
                can_update = True

        # logic update
        if can_update:
            can_update = False
            if not b.is_over():
                b.increm_fight(turn)
                if b.is_over():
                    print('battle has ended at turn {} !!!'.format(turn))
                else:
                    turn += 1

        # refresh screen
        w.fill('darkblue')
        draw_fighters(w, True, 'pink', b)
        draw_fighters(w, False, 'orange', b)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    run_simu()
    pygame.quit()
