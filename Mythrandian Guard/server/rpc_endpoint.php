<?php
namespace Datto\API;

require __DIR__ . "/vendor/autoload.php";
// require __DIR__ . "/vendor/datto/json-rpc/src/Server.php";
// require __DIR__ . "/vendor/datto/json-rpc-simple/src/Simple/Evaluator.php";

use Datto\JsonRpc\Server;
use Datto\JsonRpc\Simple;

require 'temp.php';

// This will instantiate an object of the type `Datto\API\Math`,
// // call the `subtract` method, and return a corresponding JSON-RPC response.
//
$server = new Server(new Simple\Evaluator());

//"cho $server->reply('{"jsonrpc": "2.0", "method": "math/subtract", "params": {"a": 3, "b": 2}, "id": 1}');
// echo $server->reply('{"jsonrpc": "2.0", "method": "roger/nomfamilial", "id": 2}');
//

/*
var_dump($_SERVER);
var_dump(getallheaders() );
var_dump($_REQUEST);
var_dump($_GET);
 */
$msg = $_POST['json_msg'];


echo $server->reply( $msg );
//$message);
?>
