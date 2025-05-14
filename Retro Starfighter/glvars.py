import katagames_sdk.engine as kataen

pygame = kataen.import_pygame()


class JoystickHandler:
    def __init__(self, ident):
        self.id = ident
        self.joy = pygame.joystick.Joystick(ident)
        self.name = self.joy.get_name()
        self.joy.init()
        self.numaxes = self.joy.get_numaxes()
        self.numballs = self.joy.get_numballs()
        self.numbuttons = self.joy.get_numbuttons()
        self.numhats = self.joy.get_numhats()

        self.axis = []
        for i in range(self.numaxes):
            self.axis.append(self.joy.get_axis(i))

        self.ball = []
        for i in range(self.numballs):
            self.ball.append(self.joy.get_ball(i))

        self.button = []
        for i in range(self.numbuttons):
            self.button.append(self.joy.get_button(i))

        self.hat = []
        for i in range(self.numhats):
            self.hat.append(self.joy.get_hat(i))


jhandler = [
    JoystickHandler(0),  # pygame.joystick.get_count() ,  identifiant joystick!
    None,
    None,
    None
]

title_scene = None
