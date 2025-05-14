import json
import os
import shutil
import sys
from distutils.dir_util import copy_tree
from glob import glob

import requests


if __name__ != '__main__':
    import katagames_sdk.toolset as toolset
    import katagames_sdk.serve_files_HTTP as serve_files_HTTP
    import katagames_sdk.templates as templates_sub_mod
else:
    import toolset
    import serve_files_HTTP
    import templates as templates_sub_mod


index_content = None
splash_data = None
assets_js_ct = "window.assets_folder_p = 'assets/'; \n \
window.asset_keys = {};"
datafavicon = None


def load_scripts_pack(src_dir):
    global index_content, assets_js_ct, datafavicon, splash_data

    try:
        import importlib.resources as pkg_resources
    except ImportError:
        # Try backported to PY<37 `importlib_resources`.
        import importlib_resources as pkg_resources

    ressources_loc = templates_sub_mod
    index_content = pkg_resources.read_text(ressources_loc, 'index')
    try:
        ff = open(src_dir + os.sep + 'assets.json', 'r')
        assets_js_ct = assets_js_ct.format(ff.read())
        ff.close()
    except FileNotFoundError:
        print()
        print('** WARNING: file assets.json -> Not Found, using an empty list instead **')
        assets_js_ct = assets_js_ct.format('[]')
        print()

    datafavicon = pkg_resources.read_binary(ressources_loc, 'favicon')
    splash_data = pkg_resources.read_binary(ressources_loc, 'splash-screen.png')
    print('templates found.')


def basic_copy(a, b):
    with open(a, 'rb') as src:
        with open(b, 'wb') as dest:
            dest.write(src.read())


def copy_all_python_src(folderA, folderB):
    print()
    print('COPYING python source files...')
    result = [y for x in os.walk(folderA) for y in glob(os.path.join(x[0], '*.py'))]
    target_dir_li = list()

    for cp_src in result:
        print(' @ {} '.format(cp_src), )

        base_name = os.path.basename(cp_src)
        folders_chain = os.path.dirname(cp_src)
        folders_li = folders_chain.split(os.sep)
        folders_li[0] = folderB

        dest_folders_chain = os.sep.join(folders_li)
        os.makedirs(dest_folders_chain, exist_ok=True)
        cp_dest = dest_folders_chain + os.sep + base_name

        print('    -> {}'.format(cp_dest))
        basic_copy(cp_src, cp_dest)
    # an alternative solution would be based on:
    # result = list(Path(srcfolder).rglob("*.[pP][yY]"))


class BundleGenerator:
    """
    base class
    """
    BTYPE = 'PROD-READY bundle'

    def __init__(self, src_dir, targ_dir, dev_key):
        self._src_dir = src_dir
        self._targ_dir = targ_dir
        self._req_devk = dev_key

    def source(self):
        return self._src_dir

    @property
    def target(self):
        return self._targ_dir

    @classmethod
    def bundle_type_str(cls):
        return cls.BTYPE

    def run_gen(self) -> bool:
        """
        :returns: true/false: wether generation a success or not
        """
        global index_content, datafavicon, splash_data

        srcfolder = self._src_dir
        targetfolder = self._targ_dir

        print('@_[ {} ]_@'.format(self.bundle_type_str()))
        print(srcfolder + ' --> Copy_And_Bundle --> ', end='')
        print(targetfolder)
        print('-' * 64)

        subf = 'libJS'
        arg = targetfolder + os.sep + subf
        os.makedirs(arg, exist_ok=True)

        r = requests.get('https://kata.games/ludo_app/katasdk/gam_hash.php?dk={}'.format(self._req_devk))

        ret = True
        if 200 == r.status_code:
            res_obj = json.loads(r.text)
            if isinstance(res_obj, int):
                print('**WARNING** could not generate a new gam_hash')
                ret = False
            else:
                gam_hash = res_obj
                load_scripts_pack(srcfolder)

                # step 1: write index.html & assets.js & assets & ico& main.py
                fiptr = open(targetfolder + os.sep + 'index.html', 'w')
                fiptr.write(index_content)
                fiptr.close()
                fiptr = open(targetfolder + os.sep + 'assets.js', 'w')
                fiptr.write(assets_js_ct)
                fiptr.close()

                # assets
                if not os.path.isdir(srcfolder + os.sep + "assets"):
                    print()
                    print('** WARNING: missing folder "assets/" in the source folder, using an empty one for the web bundle **')
                    print()
                    os.makedirs(targetfolder + os.sep + "assets", exist_ok=True)
                
                else:
                    copy_tree(srcfolder + os.sep + "assets", targetfolder + os.sep + "assets")
                # ico
                with open(targetfolder + os.sep + 'favicon.ico', 'wb') as tptr:
                    tptr.write(datafavicon)
                # splash
                with open(targetfolder + os.sep + 'assets' + os.sep + 'splash-screen.png', 'wb') as tptr:
                    tptr.write(splash_data)

                # bring ALL FILES
                copy_all_python_src(srcfolder, targetfolder)

                # step 2: main JS scripts
                basic_scr_li = [
                    "bmegapack.js",
                    "brython_stdlib.js",
                    "howler.js",
                    "hybrid-crypto.min.js",
                    "sound_kappa.js",
                    "canvasprim.js"
                ]
                ressources_loc = templates_sub_mod

                toolset.js_generation.cp_basic_js_scripts(ressources_loc, basic_scr_li, targetfolder)

                # step 3: JS add-on
                # ajoute les deux scripts js plus évolués
                self.step3_gen(targetfolder, gam_hash)

        else:
            print('generation -> failed! Could not run the gam_hash script')
            ret = False
        return ret

    def step3_gen(self, dest_folder, gam_hash):
        targ_sub_folder = dest_folder + os.sep + 'libJS'
        _hash = gam_hash
        toolset.js_generation.gen_procuration_js(os.sep.join((targ_sub_folder, 'procuration')), _hash[:35])
        print(' x x procuration.js added')
        full_fn = os.sep.join((targ_sub_folder, 'loading_mecha'))
        toolset.js_generation.gen_loadmecha_js(full_fn, _hash[-15:])
        print(' x x loading_mecha.js added')

        print('generation -> SUCCESS')


class WebtestBundleGen(BundleGenerator):
    BTYPE = 'WEBTEST bundle'

    def __init__(self, src, target):
        testers_dev_k = '5625db026772e21b3e67f9a77acf5835'  # serv-side defined
        # testers unique Acc => this is a FFA thing but fruits all have a low TTL

        super().__init__(src, target, testers_dev_k)


class EmutestBundleGen(WebtestBundleGen):

    def step3_gen(self, dest_folder, gam_hash):
        js_gen = toolset.js_generation
        targ_sub_folder = dest_folder + os.sep + 'libJS'
        full_fn = os.sep.join((targ_sub_folder, 'loading_mecha.js'))
        # on va sortir le contenu normal censé etre dans loading_mecha.js
        # mais en le simplifiant, et SANS paramétrage par un bout de gam_hash
        with open(full_fn, 'w') as fptr_target:
            fptr_target.write(js_gen.provide_content_loading_mecha_emutest())
            print(' x x {} written'.format(full_fn))

        # procuration.js est inutile en mode emutest, donc on le zappe

        print('generation (emutest) -> SUCCESS')


"""
one function per katasdk command
--------------------------------
"""


def gen_prod_bundle(devkfile, src_folder, targfolder):
    with open(devkfile, 'r') as devk_fptr:
        devk_val = devk_fptr.read()
        print('<DevKey signature> {}'.format(devk_val))
        bg = BundleGenerator(src_folder, targfolder, devk_val)
        return bg.run_gen()


def gen_test_bundle(src_folder, targetdir):
    bg = WebtestBundleGen(src_folder, targetdir)
    ret = bg.run_gen()
    return ret


def gen_emutest_bundle(src_folder, targetdir):
    print('ds gen_emutest_bundle')
    bg = EmutestBundleGen(src_folder, targetdir)
    res = bg.run_gen()
    basic_copy('linker.bat', targetdir+os.sep+'linker.bat')
    return res


def xserve(whatdir):
    import threading
    import webbrowser

    class bOpener(threading.Thread):
        def run(self):
            webbrowser.open('http://127.0.0.1:8000', new=1, autoraise=True)

    guess_path = "C:/Program Files/Mozilla Firefox/firefox.exe"
    if os.path.isfile(guess_path):
        os.environ['BROWSER'] = guess_path

    thr = bOpener()
    thr.start()

    os.chdir(whatdir)
    serve_files_HTTP.do_serve()


def manage_old_bundles(dest_dir):
    if os.path.isdir(dest_dir):
        print()
        print(' /!\\   ')
        print('  destination folder "{}" already exists. '.format(dest_dir))
        prompt_msg = ' Overwrite content in "{}", y/n ?  '.format(dest_dir)
        rep = input(prompt_msg)

        retval = True
        while rep not in ('y', 'Y', 'n', 'N'):
            print('non-valid answer, please re-try')
            rep = input(prompt_msg)
        if rep in ('n', 'N'):
            print()
            print('> > > generation aborted by the user! < < <')
            retval = False

        else:  # overwriting confirmed
            print('replacing: ', end='')
            print('.' + os.sep + dest_dir)
            # force rmdir
            shutil.rmtree('.' + os.sep + dest_dir, ignore_errors=True)
        return retval
    else:
        return True


def main():
    global index_content, assets_js_ct, datafavicon

    if len(sys.argv) < 2:
        print('Error: katasdk requires a parameter (bundle, webtest, serve, emutest...)')

    else:
        usercmd = sys.argv[1]

        if usercmd == 'serve':
            xserve(sys.argv[2])

        elif usercmd == 'bundle':
            print('  ~ command "bundle" received ~  ')

            keyfilename, src_folder = sys.argv[2], sys.argv[3]
            target_d = src_folder.rstrip('\\/') + '(' + keyfilename.split('.')[0] + '-wbundle)'
            can_bundle_now = manage_old_bundles(target_d)

            if can_bundle_now:
                gen_prod_bundle(keyfilename, src_folder, target_d)

        elif usercmd == 'webtest':
            print('  ~ command "webtest" received ~  ')
            source_dir = sys.argv[2]
            target_d = 'site-TEST'

            can_bundle_now = manage_old_bundles(target_d)

            if can_bundle_now:
                # bundle & serve immediately
                bundle_built = gen_test_bundle(source_dir, target_d)
                if bundle_built:
                    input('Press ENTER to continue')
                    xserve(target_d)

        elif usercmd == 'emutest':
            print('  ~ command "emutest" received ~  ')

            source_dir = sys.argv[2]
            target_d = 'emu-TEST'

            # principle= auto-replace files if files already exist
            # so we auto-delete anything old
            if os.path.isdir(target_d):
                shutil.rmtree('.' + os.sep + target_d, ignore_errors=True)

            bundle_built = gen_emutest_bundle(source_dir, target_d)
            if bundle_built:
                print('gen successful')
                input('fix the sys link bro! Then press ENTER')
                xserve(target_d)
        
        # parser = argparse.ArgumentParser()
        # parser.add_argument("--address", help="URL to be checked", required=True)
        # parser.add_argument("--jsonauth", help="JSON Google Authentication file path")
        # parser.add_argument("--verbosity", help="Verbosity", action="store_false")
        # print('yoooo')


if __name__ == '__main__':
    main()
