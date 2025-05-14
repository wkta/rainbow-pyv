"""
import requests

r =requests.get('https://xkcd.com/1906/')

print(r.status_code)
print(r.headers)
print(r.headers['Content-Type'])

print()
print('-'*64)
print(r.text)
"""
import json
from json import JSONDecodeError

import requests
from katagames_sdk.alpha_pyg.Singleton import Singleton


"""
pload2 = {'playerid':'3','func':'gm_infos'}
 # ?playerid=3&func=gm_infos
pload1 = {"json_msg": '{"jsonrpc": "2.0", "method":"math/subtract", "params": {"a":87,"b":22}, "id": 1}'}
url2 = 'http://10.0.0.13/rpc_test/post.php'
url1 = 'http://10.0.0.13/rpc_test/index.php'
r = requests.post(url1, data = pload1)
print(r.text)
#print(r.json())
"""


JSONRPC_ERR_METHOD = -32601
JSONRPC_ERR_PARAMS = -32602


class JsonRpcError(Exception):
    def __init__(self, msg, errtype, added_info=None):

        if errtype == JSONRPC_ERR_PARAMS:
            self.message = msg + ', passed: {} to {}/{}'.format(added_info[2], added_info[0], added_info[1])

        elif errtype == JSONRPC_ERR_METHOD:
            self.methodname = added_info
            self.message = msg + ', tried to call {}/{}'.format(*self.methodname)
        else:
            self.message = 'After calling {}/{}'.format(added_info[0], added_info[1]) + '\n' + msg
        super().__init__(self.message)


@Singleton
class JsonRpcServer:

    def __init__(self):
        self._endpoint = 'http://localhost/'  # default
        self._prefix = 'default'
        self.free_id = 1

    def set_endpoint(self, http_endpoint):
        self._endpoint = http_endpoint

    def set_prefix(self, p):
        self._prefix = p

    def __getattr__(self, name):

        def mimic_method(**kwargs):
            if kwargs:
                tmp_string = json.dumps(kwargs)
                message = '"jsonrpc": "2.0", "method":"{}/{}", "params": '.format(self._prefix, name)
                message += tmp_string
                message += ', "id": {}'.format(self.free_id)
                message = '{' + message + '}'
            else:
                message = '"jsonrpc": "2.0", "method":"{}/{}", "id": {}'.format(self._prefix, name, self.free_id)
                message = '{' + message + '}'
            # print('message is...')
            # print(message)
            pload = {"json_msg": message}
            req = requests.post(self._endpoint, data=pload)
            self.free_id += 1

            # error handling 1/2
            try:
                req.json()
            except JSONDecodeError:
                msg = req.text
                raise JsonRpcError(msg, 0, (self._prefix, name))

            tmp_obj = req.json()

            # error handling 2/2
            if 'error' in tmp_obj:
                err_code = tmp_obj['error']['code']
                if err_code == JSONRPC_ERR_PARAMS:
                    addedi = (self._prefix, name, kwargs)
                    raise JsonRpcError(tmp_obj['error']['message'], err_code, addedi)
                if err_code == JSONRPC_ERR_METHOD:
                    raise JsonRpcError(tmp_obj['error']['message'], err_code, (self._prefix, name))

            return tmp_obj['result']

        return mimic_method


DEV_SERVER = True

if __name__ == '__main__':
    print('--- testing the JsonRpcServer class ---')
    print()

    server = JsonRpcServer.instance()
    if DEV_SERVER:
        server.set_endpoint('http://10.0.0.13/~tom/server/rpc_endpoint.php')
    else:
        server.set_endpoint('http://sc.gaudia-tech.com/tom/bo-server/rpc_endpoint/')

    # - calling various server-side functions
    server.set_prefix('Math')
    print(
        server.subtract(a=877, b=70)
    )
    server.set_prefix('Morgoul')
    print(
        server.changeString(entree='antisocial_yes')
    )
    server.set_prefix('Roger')
    print(
        server.nomfamilial()
    )
