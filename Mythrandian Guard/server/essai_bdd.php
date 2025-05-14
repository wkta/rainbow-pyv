<?php
require 'propenable.php';

use datab\Player;

echo 'basic insertion';

$k = new Player();
$k->setPid(666);
$k->setName('thomas');
$k->setPwdHash('xyxyxy');
$k->setTsAuth('88');

$k->save();

echo PHP_EOL.'<br> -> done!';
?>
