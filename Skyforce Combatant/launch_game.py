"""
REMARK: the current file is automatically generated by PYV /pyved-engine.
*DO NOT EDIT THAT FILE* (unless you really know what you're doing)
"launch_game.py" is part of the game engine layout. It's the standard
launcher script tied to the "pyved-engine game bundle" format.
The following code helps in booting up a wrapped game cartridge
(->PyvGAMCART format) | To know more, please visit:
https://github.com/pyved-solution | Contact author: thomas.iw@kata.games
"""
import importlib.util
import json
import os

bundle_name, link_to_glvars, pyved_engine_alias = None, None, 'pyved_engine'


def prep_libs(cb_func, rel_import_flag, plugins_list):
    global pyved_engine_alias
    for alias, plugin_name in plugins_list:
        if plugin_name == 'pyved_engine':
            import pyved_engine
            plugin_module = pyved_engine
            pyved_engine_alias = alias
            getattr(pyved_engine, '_hub').bundle_name = bundle_name
        elif rel_import_flag:
            module_name = f".lib.{plugin_name}"
            plugin_module = importlib.import_module(module_name, __package__)
        else:
            module_name = f"lib.{plugin_name}"
            plugin_module = importlib.import_module(module_name)
        cb_func(alias, plugin_name, plugin_module)


def game_execution(metadata, gdef_module):
    global link_to_glvars, pyved_engine_alias

    def find_folder(givenfolder, start_path):
        for root, dirs, files in os.walk(start_path):
            if givenfolder in dirs:
                return True

    current_folder = os.getcwd()
    if find_folder(metadata['slug'], current_folder):
        adhoc_folder = os.path.join('.', metadata['slug'], 'cartridge')
    elif find_folder('cartridge', current_folder):
        adhoc_folder = os.path.join('.', 'cartridge')
    else:
        raise FileNotFoundError("ERR: Asset dir for pre-loading assets cannot be found!")
    pyv = getattr(link_to_glvars, pyved_engine_alias)
    pyv.preload_assets(
        metadata,
        prefix_asset_folder=adhoc_folder + os.sep + metadata['asset_base_folder'] + os.sep,
        prefix_sound_folder=adhoc_folder + os.sep + metadata['sound_base_folder'] + os.sep,
        debug_mode=True
    )
    for anchor_nam, std_name in {  # standardized mapping
        'beginfunc_ref': 'init', 'updatefunc_ref': 'update', 'endfunc_ref': 'close'
    } .items():
        setattr(pyv.vars, anchor_nam, getattr(gdef_module, std_name))
    pyv.run_game()


def bootgame(metadata):
    global bundle_name, link_to_glvars
    try:
        from cartridge import glvars as c_glvars
        rel_imports = False
    except ModuleNotFoundError:
        from .cartridge import glvars as c_glvars
        rel_imports = True
    link_to_glvars = c_glvars  # glvars becomes available elsewhere
    lib_list = list()
    for lib_id in metadata['dependencies'].keys():
        if len(metadata['dependencies'][lib_id]) > 1:
            alias = metadata['dependencies'][lib_id][1]
            lib_list.append((alias, lib_id))
        else:
            lib_list.append((lib_id, lib_id))
    bundle_name = metadata['slug']
    prep_libs(c_glvars.register_lib, rel_imports, lib_list)
    if c_glvars.has_registered('network'):  # manually fix the network lib (retro-compat)
        getattr(c_glvars, c_glvars.get_alias('network')).slugname = metadata['slug']
    if not rel_imports:
        from cartridge import gamedef
    else:
        from .cartridge import gamedef
    game_execution(metadata, gamedef)


if __name__ == '__main__':  # for  a"pyv-cli less" execution
    with open('cartridge/metadat.json', 'r') as fp:
        bootgame(json.load(fp))
