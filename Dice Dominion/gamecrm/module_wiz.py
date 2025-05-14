import sys

sys.path.insert(0, "../vendor/")
from cgm_engine.util import underscore_format
import os


MSG = "name of the new module, using CamelCase? (or just hit Enter to cancel)\n> "

TEMPLATE = "\
from cgm_engine import BaseGameState\n\
\n\
\n\
class {}(BaseGameState):\n\
    def __init__(self, gs_id, name):\n\
        super().__init__(gs_id, name)\n\
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
    saisie = input(MSG)
    if len(saisie) == 0:
        print('canceled.')
    
    else:
        directory = 'app'
        ensure_dir(directory)
        tmp = underscore_format(saisie)
        directory = os.path.join(directory, tmp)
        ensure_dir(directory)
        
        chemin_py = 'app.{}.state'.format(tmp)
        print('creating ' + chemin_py)
        nom_cl = saisie + 'State'
        
        print('adding stub files :')

        # crea fichiers vides
        li_fi = ('__init__.py', 'model.py', 'ctrl.py', 'view.py')
        for nomfi in li_fi:
            contenu = ' '
            filepath = os.path.join(directory, nomfi)
            
            ptr = open(filepath, 'w')
            ptr.write(contenu)
            ptr.close()
            print('created empty file {}...'.format(filepath))
        
        # crea state.py
        nomfi = 'state.py'
        contenu = TEMPLATE.format(nom_cl)
        filepath = os.path.join(directory, nomfi)
        
        ptr = open(filepath, 'w')
        ptr.write(contenu)
        ptr.close()
        print('created class {} in {}...'.format(nom_cl, filepath))

        print("\nDONE.")
