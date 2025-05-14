import time

import katagames_sdk.engine as kataen
from katagames_sdk.ext_gui.Button import ButtonPanel, Button

# in future versions:
# kataen.bootstrap()
pygame = kataen.pygame #kataen.import_pygame()


GAME_TITLE = 'Mythrandian Guard'
MAXFPS = 60
gameover = False
scr = pygame.surface.Surface((0, 0))
clock = pygame.time.Clock()
spr_group = pygame.sprite.Group()
buttons = pygame.sprite.Group()
t_last_update = time.time()
player_spr = None
lizard_spr = None
panel = None


class CustomListener(kataen.EventReceiver):
    def proc_event(self, ev, source):
        global gameover, player_spr, lizard_spr

        if ev.type == kataen.EngineEvTypes.BTCLICK:
            print(ev)

        elif ev.type == pygame.QUIT:
            gameover = True

        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                anim_attack()
            elif ev.key == pygame.K_RETURN:
                anim_defend()
            elif ev.key == pygame.K_BACKSPACE:
                anim_hit()


# -- to be bound to GUI buttons --
def anim_attack():
    global player_spr, lizard_spr
    player_spr.play('attack')
    lizard_spr.play('attack')


def anim_defend():
    global player_spr, lizard_spr
    player_spr.play('defend')
    lizard_spr.play('defend')


def anim_hit():
    global player_spr, lizard_spr
    player_spr.play('getsHit')
    lizard_spr.play('getsHit')


cc = None
manager = None


def init_g():
    global scr, clock, spr_group, player_spr, lizard_spr, panel, cc, manager

    # pygame.init()
    # scr = pygame.display.set_mode((640, 480))
    kataen.init('hd')#kataen.HD_MODE)
    scr = kataen.get_screen()

    pygame.display.set_caption(GAME_TITLE)

    spr = player_spr = kataen.AnimatedSprite('assets/knightye_sheet')
    spr.preload()
    spr.rect.topleft = (256, 0)
    spr2 = lizard_spr = kataen.AnimatedSprite('assets/lizardgr_sheet')
    spr2.preload()
    spr2.rect.topleft = (0, 0)

    spr_group.add(spr, spr2)

    tmp_li = list()
    actions = ['attack(space)', 'defend(return)', 'getsHit(backspc)']
    for k, action in enumerate(actions):
        tmp_li.append(Button(pos=(100 + 228 * k, 256), size=(150, 48), label=action))

    panel = ButtonPanel(
        tmp_li, {
            tmp_li[0].ident: anim_attack,
            tmp_li[1].ident: anim_defend,
            tmp_li[2].ident: anim_hit,
        }
    )
    print('on allume')
    panel.turn_on()  # works only if kataen is init
    cc = CustomListener()
    cc.turn_on()

    buttons.add(
        tmp_li[0], tmp_li[1], tmp_li[2]
    )
    manager = kataen.EventManager.instance()


def update_g():  # infot=None:
    global scr, gameover, clock, spr_group, player_spr, t_last_update, manager

    manager.update()  # event management

    tmp = time.time()
    dt = (tmp - t_last_update)
    t_last_update = tmp
    spr_group.update(dt)

    # draw
    scr.fill('antiquewhite3')
    spr_group.draw(scr)
    buttons.draw(scr)

    # pygame.display.update()
    kataen.display_update()
    clock.tick(MAXFPS)


if __name__ == '__main__':  # local execution entry pt
    # here, we dont use the built-in (engine) game ticker
    # we code the loop manually
    init_g()
    while not gameover:
        update_g()

    kataen.cleanup()
    # pygame.quit()
