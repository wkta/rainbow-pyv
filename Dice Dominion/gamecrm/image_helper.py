import coremon_main.conf_eng as cgmconf


def filename_bg():
    res = 'vbasic_bg.png'
    if cgmconf.runs_in_web():
        pass
    else:
        import os
        res = os.path.join('assets', res)
    return res


def filenames_4borders():
    solo_bordernames = [
        'hexBorder0.PNG', 'hexBorder1.PNG', 'hexBorder2.PNG',
        'hexBorder3.PNG', 'hexBorder4.PNG', 'hexBorder5.PNG'
    ]
    if cgmconf.runs_in_web():
        res = solo_bordernames
    else:
        import os
        tmp_li = list()
        for elt in solo_bordernames:
            tmp_li.append(os.path.join('assets', elt))
        res = tmp_li
    return res


def odd_n_even_img_filenames():
    if not cgmconf.runs_in_web():
        import os
        return os.path.join('assets', 'oddLocator.PNG'), os.path.join('assets', 'evenLocator.PNG')
    else:
        return 'oddLocator.PNG', 'evenLocator.PNG'


def filenames_4tiles():
    solo_tilenames = [
        'g_hexDGruen.PNG', 'g_hexGelb.PNG', 'g_hexHGruen.PNG',
        'g_hexOrange.PNG', 'g_hexRosa.PNG', 'g_hexRot.PNG',
        'g_hexTuerkis.PNG', 'g_hexViolette.PNG', 'g_hexSchwarz.PNG'
    ]
    if cgmconf.runs_in_web():
        res = solo_tilenames
    else:
        import os
        tmp_li = list()
        for elt in solo_tilenames:
            tmp_li.append(os.path.join('assets', elt))
        res = tmp_li
    return res


def get_t_colorkey():
    return 0x80, 0x00, 0x80  # violet
