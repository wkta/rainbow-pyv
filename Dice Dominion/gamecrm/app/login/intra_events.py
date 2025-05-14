

# --- evènements liés au changement de focus / à la saisie clavier
#from engine.UnitedEvent import UnitedEvent


# TODO check if deprecated
class UnitedEvent:
    def __init__(self, name):
        pass


class DoChangeFocus(UnitedEvent):
    def __init__(self):
        super().__init__('do change focus event')
        self._v2 = False


class FocusChangedEvent(UnitedEvent):
    def __init__(self, focusing_login):
        super().__init__('focus changed event')
        self.focusing_login = focusing_login
        self._v2 = False


class AddCharInField(UnitedEvent):
    def __init__(self, char):
        super().__init__('add char in field event')
        self.char = char
        self._v2 = False


class RemoveCharInField(UnitedEvent):
    def __init__(self):
        super().__init__('remove char in field event')
        self._v2 = False


# --- pour mettre à jour la vue
class CredentialsChangedEvent(UnitedEvent):
    def __init__(self, l_actu, p_actu):
        super().__init__('credentials changed event')
        self.l_actu = l_actu
        self.p_actu = p_actu
        self._v2 = False
