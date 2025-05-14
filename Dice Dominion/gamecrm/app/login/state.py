from gamecrm.app.login.LoginCtrl import LoginCtrl
from gamecrm.app.login.LoginView import LoginView
from gamecrm.app.login.model import LoginModel
from coremon_main.structures import BaseGameState


class LoginState(BaseGameState):

    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)
        self.m = self.v = self.c = None

    def enter(self):
        self.m = LoginModel()
        self.v = LoginView(self.m)
        self.c = LoginCtrl(self.m, self.v)
        self.resume()

    def release(self):
        self.pause()
        self.m = self.v = self.c = None

    def pause(self):
        self.c.turn_off()
        self.v.turn_off()

    def resume(self):
        self.v.turn_on()
        self.c.turn_on()
