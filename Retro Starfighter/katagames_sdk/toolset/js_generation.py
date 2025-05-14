import os

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

lines_jscode_loading_mecha = [
    '"use strict";',
    'window.retrv_cached = retrv_cached;',
    'window.catalog = {};',
    'function retrv_cached(nom_img){return window.catalog[nom_img];}',
    'function preload_images(){',
    'let asset_pairs = window.asset_keys.map(elt => {return [elt, window.assets_folder_p + elt];});',
    'asset_pairs.forEach(elt => {',
    'let img = new Image();',
    'img.onload = function(){',
    'window.catalog[elt[0]] = [img, img.naturalWidth, img.naturalHeight]; };',
    'img.src = elt[1];',
    '}); }',
    'function py_WhenRdy() {',
    "window.console.log('KataSDK wbundle: LOADING...');",
    "let nb_elt_charges = Object.keys(window.catalog).length;",
    "if (window.obj_scripts != null && window.asset_keys.length == nb_elt_charges) {",  # idx 15
    "window.console.log(window.asset_keys, nb_elt_charges, 'OK');",
    "window.console.log(' B-package injection');",
    "__BRYTHON__.use_VFS = true;",
    "__BRYTHON__.update_VFS(window.obj_scripts);",
    "window.console.log('Transpiling Python...');",
    "brython();",
    "} else {setTimeout(py_WhenRdy, 500);} }",
    'function splash(){',
    'var canvas = document.getElementById("pygame-canvas");',
    'var ctx = canvas.getContext("2d");',
    'var image = document.getElementById("splash-scr-source");',
    'ctx.drawImage(image, 0, 0); }',
    'function gameInit(bleedin_e=0) {',
    'window.obj_scripts = null;',
    'splash();',
    "procur(bleedin_e,'%s');",  # idx 31
    'preload_images();',
    'py_WhenRdy(); }'
]


def provide_templ_loading_mecha():
    global lines_jscode_loading_mecha
    return ''.join(lines_jscode_loading_mecha)


def provide_content_loading_mecha_emutest():
    global lines_jscode_loading_mecha
    tmp = list(lines_jscode_loading_mecha)  # copie
    tmp[15] = "if (window.asset_keys.length == nb_elt_charges) {"
    tmp[17] = tmp[18] = tmp[19] = ''
    tmp[31] = ''
    return "\n".join(tmp)


procuration_templ = """
// pr but denregistrer les scripts bython dans un obj, référencé par window.obj_scripts 
function procur(bleedin_e,sfdevk){
  window.obj_scripts = null;

function cryptagetruc(xxx){
	// prepa operations chiffrement
	// const pr_key = forge.pki.privateKeyFromPem('
	// -----BEGIN RSA PRIVATE KEY-----
	// MIIEpAIBAAKCAQEA0qATHNjfM3upWwOgVA9V/zHAVQ9/FCfGbu7h4i2VV6OgudEg
	// HfVsifeKi869wO9MNtwNBJmJQst6Jmu6rd3qknUKHKtaq2cd52fdIegt7wDVusM/
	// CyuC6rp+elsHdV/I3ttWbuR1+0TTyXUFuVelXPiy9cLTn/+gyiIzm4dDJWyuGXnQ
	// l8Az5wgaaSOwbqWgp7MYc2b7ZkVdTj+GMtv1lxZz/Lgr5duJpl6J5nF2EXJs1hCE
	// 1LIGunIOfon52ZdlLC9xAn79Uf7oFVqG9TGoD4AirTjZ8NYr89mFVnYgbM8DcZ2j
	// IAYYt19IbVc8h1/QQAPmNlDBOwjxYfodt0pLDQIDAQABAoIBABrppUeMVojHhk5A
	// 2l2jUAO5oa+8uSokIvDNyUMTO//kwoa7t/TcBTBj1uoiUpCygvSHjYpG7AkC4urB
	// 3SqWLoDkP5SGOKGqHWISHWlVt3jQjH6+r/GHb8T6a2rK8tsGkC4ZrKOiwYiHtOAK
	// +d5C2rhUdtl8OXo6OZtaX2nCEMxZKSwrojTheLszWeNlNxl35zIrFu4UY4rkft5m
	// YK6JOWg4z9aHIRGvOF/9zyXTJKHC2Ais6KCZYaouikze7MhZf/VNLpyqZbFJWtUU
	// UvSmQg3g8siQ1WpNeIsZQtP97ct9ycC1/pgAa8cCJmn33Mu3RJ6k1QkNR1wxDOe1
	// MyZ6HqkCgYEA+iy5It/WbX/nBrx0/8uf+9DxecQwZMKhqy9sneipbIDMhaIa7pfb
	// kxfg7bA1yyL3XjVR6CJ/hhxiNKaz7lKUMf7gdQs3B08mF/RHrYyHVRMd/5wq6ugt
	// hOjcvedtHx+zxVzeQvT/GjwqRZ4yhB+J1xDKa+dqDiKUtO7GmpxfL2cCgYEA14eZ
	// iVLLdet/kYrWWxQqIAl+wiwGLQIpyWNTVTdeYDNDYxfwtco7FdL2smrd/BmaAEY5
	// 5RpSOhLGZ7WufzrCn/wN/ktCQ4xiMdH7blHx1p6fYXIott7+h9fhBeHWBPzHcMCQ
	// MhFBc8Szl4CBwSlohQSgJPVCCFfYaeqL5Y2UzWsCgYEAzsKvsBb3DUCsG3Ed8VrF
	// OkWRjWWL6XrCSszDJC7p93brkXZMc+yl2IffqhH8I4sejonay9PXOWuz7nfoNYui
	// Vz+jGpjOPgg4H4wQwWpnXvSR0nOrNMH2/OXHqlveX96/oNoEB6qcO36GIUuBzJiU
	// P17tLQjxKgWCiZbeJWIfePkCgYAhvDXKCs2R7YSQMV0P8H4Peaz/k4h77wS/Yu6e
	// PgZlpGB92DdzHO5Woii/EH8igJdcR6G0PIR2Vo37mbJwc7AW/orqLLl4fTa5eZaT
	// U/w4jaeAxy+cQBczCBVOqGSpby+AdIOdcpn+FuHNau3kYCjd+TVf04u8ZpOXMIEp
	// MxoBdQKBgQDD+M/UXcvJ18UUSbbwSZ2AJbivH/9t9u9Zeh3pM8K0I2CpYN2Z8PYX
	// 5YBugoVjjkbdJU2+VEjfNsN2nrDCOm6H9BEq8vSxpLEwxGJwa57nYvQftro6gVmD
	// Be7j37eO1hQbNT/wIbYsx4z3oneB6CXlfHuxQc5f2t+mzAU0GICz2g==
	// -----END RSA PRIVATE KEY-----' );
	// console.log('priv key PEM:', pr_key);
	// const pu = forge.pki.setRsaPublicKey(pr_key.n, pr_key.e)
	// console.log('pub key PEM:', pu);

	// 1) av+ec FORGE
	// ------------------------
	//const transmi = pu.encrypt(xxx);
	//console.log('encrypted: ', forge.util.encode64(transmi));
	//const y = pr_key.decrypt(transmi);
	// encrypt  (enc/dec with Obj Pub and PEM Priv)
	//console.log('[Enc by Obj/Dec by PEM]');
	//const encrypted = pub.encrypt('Hello World!');
	//console.log('encrypted(by Obj):', forge.util.encode64(encrypted));
	//const decrypted = priv2.decrypt(encrypted);
	//console.log('decrypted(by PEM):', decrypted);
	// je dois affecter dans :
	
	// 2) avec hybrid
	var rsa = new RSA();
	var crypt = new Crypt();
	var br_tbl_scripts = null;

	function aller_retour(pu, pr){
		// Encryption with one public RSA key
		var encrypted = crypt.encrypt(pu, xxx);
		// console.log(encrypted);
		// Decrypt encryped message with private RSA key
		var decrypted = crypt.decrypt(pr, encrypted);
		var serial_json = decrypted.message;

		window.obj_scripts = JSON.parse(serial_json);  // saving essential info.
		
	}
	function cb_func(keyPair){
		aller_retour(keyPair.publicKey,keyPair.privateKey);
	}
	rsa.generateKeyPair(cb_func);  // uses a callback
}
cibl = (bleedin_e==0 ? 'https://games.gaudia-tech.com/ludo_app/katasdk/' :
 'https://games.gaudia-tech.com/ludo_app/katasdk_dev/' );
cibl += '?gk=%s'+sfdevk;
var request = new XMLHttpRequest();
request.open('GET', cibl, true);
request.onload = function() {
  if (request.status >= 200 && request.status < 400) {  // success
    var rep = request.responseText;
	function hex_to_ascii(str1)
	{
        if (null==str1){
             return null;
        }else{
            var hex  = str1.toString();
            var str = '';
            for (var n = 0; n < hex.length; n += 2) {
            str += String.fromCharCode(parseInt(hex.substr(n, 2), 16));
            }
            return str;
        }
	}
	var tmp = hex_to_ascii(JSON.parse(rep));
        if (null == tmp){
            throw new Error('-FATAL- Game access has been revoked (by Kata.games) if you think this is unexpected, please contact support or re-bundle your game using the ad-hoc DevKey');
            return;
        }else{		
	    cryptagetruc(tmp);
	}
  } else {
    // We reached our target server, but it returned an error
	console.log('ERR ajax to retrieve katasdk');
  }
};
request.onerror = function() { // There was a connection error of some sort
};
request.send();
}
"""


def cp_basic_js_scripts(ress_loc, fname_li, dir_bundle):
    """
    copie les 5 scripts JS qui ne contiennent pas dinfo variable
    """
    for fname in fname_li:
        cont = pkg_resources.read_binary(ress_loc, fname)
        with open(dir_bundle + os.sep + 'libJS' + os.sep + fname, 'wb') as targetfptr:
            targetfptr.write(cont)
        print(' x x {} added'.format(fname))


##    destdir = dir_bundle+os.sep+'libJS'
##    cpt = 0
##    for fn, hexcont in dico.items():
##        print(fn)
##        fp = open(destdir+os.sep+fn, 'wb')
##        fp.write(bytes.fromhex(hexcont))
##        fp.close()
##        cpt += 1
##    print('gen done, {} scripts expanded'.format(cpt))


def gen_procuration_js(targ_fn, pfdk):
    with open(targ_fn + '.js', 'w') as targf:
        targf.write(procuration_templ % pfdk)


def gen_loadmecha_js(targ_fn, sfdk):
    with open(targ_fn + '.js', 'w') as targf:
        targf.write(provide_templ_loading_mecha() % sfdk)
