import gamecrm.eventtypes as eventtypes
import random
import pygame
from coremon_main.events import EventReceiver


class NetworkReplacement(EventReceiver):

    def __init__(self):
        super().__init__()

        self.eliza = None  #  N.B. le module eliza a été retiré du projet
        # eliza.eliza()

        # TODO bind
        # self.reg_event_func(eventtypes.CHATMSG, self.on_chatmsg)
        # self.reg_event_func(eventtypes.ELIZATIMER, self.on_timer)

        # TODO fix
        # events.RootEventSource.instance().add_listener(self)
        self.nick = "Therapist: "
        eventtypes.post_chatmsg(self, self.nick + "hi, please speak english to me.")
        self.messages = []

    # redefinition
    def proc_event(self, ev, source):
        pass

    def on_chatmsg(self, event):
        if event.source != self:
            msg = event.msg
            split = msg.split(':')
            msg = msg[len(split[0]):]
            if len(self.messages) == 0:
                self.set_timer()
            self.messages.append(msg)

    def on_timer(self, event):
        if len(self.messages):
            # stop timer
            pygame.time.set_timer(eventtypes.ELIZATIMER, 0)
            msg = self.messages.pop(0)
            resp = self.eliza.respond(msg)
            resp = self.nick + resp
            eventtypes.post_chatmsg(self, resp)
            if len(self.messages) > 0:
                self.set_timer()

    def set_timer(self):
        """
        
        """
        print(self)
        interval = random.randint(1500, 10000)
        print(interval)
        pygame.time.set_timer(eventtypes.ELIZATIMER, interval)

# if __name__=='__main__':
#     import pygame
#     import gui
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     chat = gui.ChatModul("nickname", 10)
#     NetworkReplacement()
#     pygame.key.set_repeat(500, 30)
#     while 1:
#         screen.fill((0,0,0))
#         events.RootEventSource.instance().update()
#         screen.blit(chat.image,(0, 0))
#         pygame.display.flip()
