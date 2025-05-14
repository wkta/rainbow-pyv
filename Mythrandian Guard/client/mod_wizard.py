# those two lines are useful if running without PyCharm /proper "Content Root" settings...
# import sys
# sys.path.append('../vendor')
import os

from katagames_sdk.alpha_pyg.util import underscore_format


MSG_INVITE = "how to name the new module? *** plz use CamelCase *** (or hit Enter to cancel)\n> "

TEMPLATE = "\
from katagames_sdk.engine import BaseGameState, EngineEvTypes, EventReceiver, import_pygame\n\
\n\
\n\
pygame = import_pygame()\n\
\n\
\n\
class {}(BaseGameState):\n\
    def __init__(self, gs_id, name):\n\
        super().__init__(gs_id, name)\n\
        self.m = self.v = self.c = None\n\
\n\
    def enter(self):\n\
        pass\n\
\n\
    def release(self):\n\
        pass\n"


def ensure_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)
    # fin ensure_dir


if __name__ == '__main__':
    saisie = input(MSG_INVITE)
    if len(saisie) == 0:
        print('canceled.')

    else:
        directory = 'app'
        ensure_dir(directory)
        tmp = underscore_format(saisie) + '_state.py'
        #directory = os.path.join(directory, tmp)
        #ensure_dir(directory)

        chemin_py = tmp  # 'app.{}.state'.format(tmp)
        print('creating ' + chemin_py)
        nom_cl = saisie + 'State'
        # print('adding stub files :')

        # crea fichiers vides
        # li_fi = ('__init__.py', 'model.py', 'ctrl.py', 'view.py')
        # for nomfi in li_fi:
        #     contenu = ' '
        #     filepath = os.path.join(directory, nomfi)
        #
        #     ptr = open(filepath, 'w')
        #     ptr.write(contenu)
        #     ptr.close()
        #     print('created empty file {}...'.format(filepath))

        # crea state.py
        nomfi = tmp  #'state.py'
        contenu = TEMPLATE.format(nom_cl)
        filepath = os.path.join(directory, nomfi)

        ptr = open(filepath, 'w')
        ptr.write(contenu)
        ptr.close()
        print('created class {} in {}...'.format(nom_cl, filepath))

        print("\nDONE.")
