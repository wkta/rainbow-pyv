import json
import math
import random
from . import glvars


pyv = glvars.pyv
pyv.bootstrap_e()
screen = None
r4 = pyv.new_rect_obj(32, 32, 128, 128)
kpressed = set()
labels = [None, None]
big_ft = ft_obj = None
gameserver_host = None
SLUG_CART = 'Wheel Spinner'# TODO need to find how to fetch metadata for the game being executed...I think glvars.netw can have it

# Colors
BLACK = "#2d3047"
WHITE = (255, 255, 255)
RED = "#c8553d"
GREEN = "#588b8b"
BLUE = "#93b7be"
ORANGE = "#f28f3b"
PEACH = "#ffd5c2"
col_names = {
    WHITE: "white",
    RED: "red",
    GREEN: "green",
    BLUE: "blue",
    ORANGE: "orange",
    PEACH: "peach",
}
BG_COL = BLACK
CURSOR_COL = WHITE
# Define the wheel's wedges
NUM_WEDGES = 6
# ATTENTION: grosse astuce!
# comme on recherche l'alignement entre le cuseurs qui se trouve en haut de l'écran (et pas l'angle 0)
# et puis comme on dessine les wedges dans un ordre qui est inversé par rapport à la rotation appliquée
# sur la roue, nous devons à la fois selectionner le 1er element différemment
# ET utiliser l'ordre inverser pour que le calcul de wedge actuel + l'image affichée soit en cohérence
disp_order_WEDGE_COLORS = [RED, GREEN, BLUE, ORANGE, PEACH, WHITE]
WEDGE_COLORS = [WHITE, RED, GREEN, BLUE, ORANGE, PEACH]
WEDGE_COLORS.reverse()
ANGLE_PER_WEDGE = 360 / NUM_WEDGES
WHEEL_RADIUS = 144  # org value:200 before may25
angles_thresholds = [(i * ANGLE_PER_WEDGE - 30, i * ANGLE_PER_WEDGE + 30) for i in range(6)]
wealth = 0
wealth_label = None
label_locked = None
# Wheel rotation
# 0 --> milieu du peach, -30..30 est donc l'intervalle où on est ds peach
current_angle = 0  # degrés & clockwise
spinning = False
speed = 0
deceleration = 0.08  # Constant deceleration
final_target_angle = 0
tmp_disp = None  # label to disp final wedge color
LABEL_POS = (320, 566)
WEALTH_POS = (590, 566)
locked_game = True  # if youre not logged in, the game is locked
curr_spin_count = 0
target_spin1, target_spin2 = None, None


# --------- as of may 2025 this is deprecated ------------
# i still use it, only for this proto, but this is wrong
def fetch_endpoint_gameserver() -> str:
    # read the content from remote file "servers.json", located at katagames.io/servers.json
    # then provide an ad-hoc URL to the game server software
    tmp = glvars.netw.get(  # TODO avoid using hard set URLs, this should be packed in the local "pyconnector_config.json" file!
        'https://katagames.io/', 'servers.json'
    ).to_json()
    
    print('-------servers.json fetched-------------\n', tmp)
    print('reading key...',SLUG_CART)
    game_server_infos = tmp[SLUG_CART]
    target_game_host = game_server_infos['url']
    print('found url:',target_game_host)
    return target_game_host


def refresh_fonts():
    global ft_obj, big_ft
    big_ft = pyv.new_font_obj(None, 48)
    ft_obj = pyv.new_font_obj(None, 22)


def gen_initial_speed():
    return random.uniform(9.25, 15.667)  # the random spin speed, initially applied


def draw_wheel(center_x, center_y, angle):
    for i in range(NUM_WEDGES):
        start_angle = math.radians(angle + i * ANGLE_PER_WEDGE)
        end_angle = math.radians(angle + (i + 1) * ANGLE_PER_WEDGE)
        # Calculate the points for the wedge polygon
        start_x = center_x + WHEEL_RADIUS * math.cos(start_angle)
        start_y = center_y + WHEEL_RADIUS * math.sin(start_angle)
        end_x = center_x + WHEEL_RADIUS * math.cos(end_angle)
        end_y = center_y + WHEEL_RADIUS * math.sin(end_angle)
        # Draw the wedge
        points = [(center_x, center_y), (start_x, start_y), (end_x, end_y)]
        pyv.draw_polygon(screen, disp_order_WEDGE_COLORS[i], points)


def get_wcolor_under_cursor(curr_angle):
    global WEDGE_COLORS
    # Center of the wheel
    # center_x, center_y = WIDTH // 2, HEIGHT // 2
    # The angle where the cursor is pointing (upwards is 90 degrees)
    # cursor_angle = 90  # 90 degrees is the upward direction
    # Adjust the angle to see which wedge the cursor points to
    adjusted_angle = curr_angle % 360
    # Determine the wedge under the cursor
    res = 0  # because numbers below 0.0 arent supported by the for loop below, the default wedge rank is the 0th
    for rank in range(0, 6):
        intv = angles_thresholds[rank]
        if intv[0] < adjusted_angle <= intv[1]:
            res = rank
            break
    return res, WEDGE_COLORS[res]


def paint_game(scr):
    # Draw the wheel
    global current_angle, spinning, speed, tmp_disp
    WIDTH, HEIGHT = scr.get_size()
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    draw_wheel(center_x, center_y, current_angle)
    # Draw the cursor
    yinf = 11
    cursor_spike_factor = 25
    pyv.draw_polygon(screen, CURSOR_COL, [(center_x - 10, yinf), (center_x + 10, yinf), (center_x, yinf+cursor_spike_factor)])
    if tmp_disp:
        screen.blit(tmp_disp, LABEL_POS)
    if wealth_label:
        screen.blit(wealth_label, WEALTH_POS)


def test_luck_remote_call() -> tuple:
    """
    :return: a pair of integer values. The second one can be None
    """
    global gameserver_host
    print('call test my luck ------..........')
    # we have to use .text on the result bc we wish to pass a raw Serial to the model class
    netw_reply = glvars.netw.get('', gameserver_host, data={'jwt': glvars.stored_jwt})
    try:  # stop if error, stop right now as it will be easier to debug
        json_obj = json.loads(netw_reply.text)
        a, b = json_obj["serverNumber1"], json_obj["serverNumber2"]
        print(json_obj['message'])
        print()
        return int(a)-1, int(b)-1
    except json.JSONDecodeError:
        print(' --Warning-- : cant decode the JSON reply, after game server script has been called!')
        return None, None


def peek_future_match(selected_speed, goal_wedge):
    """
    le but de cette fonction est de simuler le lancement de roue mais sans jouer l'animation client-side,
    la fct aide à selectionner 'par brute-force' la speed qui va bien pour tomber sur le wedge qu'on est censé voir
    apparaitre post-spin
    :param selected_speed: float
    :param goal_wedge: int, le rang du triangle, dans l'intervalle 0..5
    :return:
    """
    global current_angle, speed
    cp_angle = current_angle
    speed = selected_speed

    # simulation per se
    simu_done = False
    while not simu_done:
        cp_angle -= speed
        speed -= deceleration
        if speed < 0.0001:
            simu_done = True
            wedge_rank, wedge_color = get_wcolor_under_cursor(cp_angle)
            wedge_name = col_names[wedge_color]

            if goal_wedge == wedge_rank:
                print('simu success-> speed ok found!', selected_speed)
                print()
                return True
            # - big debug
            # print('...simu avec arret:', wedge_name)
    return False


def post_play_refresh_cr():
    # called after each "play", to refresh the amount of CR
    global wealth, wealth_label
    infos = glvars.netw.get_user_infos(glvars.stored_pid)
    wealth = infos['balance']
    wealth_label = ft_obj.render('{} CR'.format(wealth), False, WHITE)


def init(vmst=None):
    global screen, gameserver_host, wealth, locked_game, label_locked

    pyv.init(engine_mode_id=4)  #wcaption='Untitled pyved-based Game')
    refresh_fonts()

    glvars.stored_jwt = glvars.netw.get_jwt()
    glvars.stored_username = glvars.netw.get_username()
    glvars.stored_pid = glvars.netw.get_user_id()
    screen = pyv.get_surface()
    print("jwt:", glvars.stored_jwt)
    print("username:", glvars.netw.get_username())
    print('pid:', glvars.stored_pid)
    gameserver_host = fetch_endpoint_gameserver()
    locked_game = (glvars.stored_jwt is None)

    if not locked_game:
        post_play_refresh_cr()
    else:
        label_locked = ft_obj.render('Please login with credentials, then re-launch game', False, WHITE)


def update(time_info=None):
    global labels, spinning, tmp_disp, speed, curr_spin_count, current_angle, target_spin1, target_spin2

    wanna_spin = False
    
    # the right way to do stuff is:
    for ev in pyv.event_get():
        if ev.type == pyv.EngineEvTypes.Quit:
            pyv.vars.gameover = True
        elif ev.type == pyv.EngineEvTypes.Keydown:
            if ev.key == pyv.K_ESCAPE:
                pyv.vars.gameover = True
            elif ev.key == pyv.K_SPACE:
                wanna_spin = True
        elif ev.type == pyv.EngineEvTypes.Mousedown:
            wanna_spin = True  # manage mouse clicking
    
    # --- old and bad:
    # for ev in pyv.event_get():
        # if ev.type == pyv.event.QUIT:
            # pyv.vars.gameover = True  # manage game exit
        # elif ev.type == pyv.KEYDOWN:
            # if ev.key == pyv.K_ESCAPE:
                # pyv.vars.gameover = True
            # elif ev.key == pyv.K_SPACE:
                # wanna_spin = True
        # elif ev.type == pyv.MOUSEBUTTONDOWN:
            # wanna_spin = True  # manage mouse clicking

    if locked_game:
        wanna_spin = False

    # ---------------
    #  logic update
    # ---------------
    if wanna_spin:  # only the "start spin" part
        if not spinning:
            if curr_spin_count == 0:  # init speed 1st spin
                # we use the precomputed server-side number
                target_spin1, target_spin2 = test_luck_remote_call()
                print(target_spin1, target_spin2)
                target_wcol = [ WEDGE_COLORS[target_spin1], WEDGE_COLORS[target_spin2]]
                print('server gave:', col_names[target_wcol[0]], col_names[target_wcol[1]])

                # so we need a speed print('rez:', spin_result)

                # - selecting the adhoc speed
                try_speed = gen_initial_speed()
                while not peek_future_match(try_speed, target_spin1):
                    try_speed = gen_initial_speed()

                speed = try_speed
                # Start the spinning
                spinning = True
                tmp_disp = None

                # Random target angle (1-3 full spins)
                # final_target_angle = initial_angle + random.uniform(360, 1080)

                # TODO ensure that server side you cant win CR on the 2nd spin if the 1st spin was lost
                if target_spin1 == 5:  # there is no sense to spin again if first color isnt white
                    curr_spin_count += 1

            elif curr_spin_count == 1:  # init speed 2nd spin

                # - selecting the adhoc speed
                try_speed = gen_initial_speed()
                while not peek_future_match(try_speed, target_spin2):
                    try_speed = gen_initial_speed()
                speed = try_speed
                # Start the spinning
                spinning = True
                tmp_disp = None
                curr_spin_count = 0

            else:
                raise ValueError('warning curr_spin_count value non consistent')

    # update the wheel position
    if spinning:
        current_angle -= speed
        speed -= deceleration
        if speed < 0.0001:
            spinning = False
            speed = 0
            _, wedge_color = get_wcolor_under_cursor(current_angle)
            wedge_name = col_names[wedge_color]
            # print(f"The wheel stopped at {wedge_name.capitalize()}!")
            tmp_disp = ft_obj.render(wedge_name.capitalize(), True, wedge_color,
                                     "#ffffff" if wedge_color != WHITE else "#000000")
            if curr_spin_count == 0:
                post_play_refresh_cr()

    # graphical update
    screen.fill(BG_COL)
    if locked_game:
        scr_size = screen.get_size()
        label_size = label_locked.get_size()
        mid_pt = [
            (scr_size[0] - label_size[0]) // 2,
            (scr_size[1] - label_size[1]) // 2
        ]
        screen.blit(label_locked, mid_pt)
    else:
        paint_game(pyv.get_surface())
    pyv.flip()


def close(vmst=None):
    print('clean exit.')
    pyv.close_game()
