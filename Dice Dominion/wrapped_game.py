
if not is_web_context:
import sys
sys.path.append('../../scripts/Lib/site-packages/')
# warning: test that pygame folder is not here, when testing app in the local context


import coremon_main.conf_eng as cgmconf
is_web_context=False
cgmconf.renseigne(is_web_context)


# - in this game wrapper, the line below should be the only
# app-specific line
import gamecrm.slender_mconquest as mygame

import coremon_main.engine as coremon


coremon.init('hd')
mygame.run()

if not cgmconf.runs_in_web():
    coremon.cleanup()
