<?php

error_reporting(0);
#ini_set('display_errors', 1);
#ini_set('display_startup_errors', 1);

$db_file = "db/safari.sqlite";

$error = false;
$messages = array();
$code = "";
$user = "";

if (!empty($_GET)) {
    if (isset($_GET['code'])) {
        $code = strtoupper($_GET['code']);
        if (!preg_match("/^OC[0-9A-F]+$/", $code)) {
            $error = true;
            $code = "";
            array_push($messages, "ERROR: bad cache code.");
        }
    } elseif (isset($_GET['user'])) {
        $user = strtoupper($_GET['user']);
        if ($user == "") {
            $error = true;
            array_push($messages, "ERROR: empty user.");
        }
    } else {
        $error = true;
        array_push($messages, "ERROR: no 'code=OC...', no 'user=...' parameter.");
    }
} else {
    $error = true;
    array_push($messages, "ERROR: no 'code=OC...', no 'user=...' parameter.");
}

if ($code != "") {
    $db = new PDO('sqlite:' . $db_file);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $sql = "SELECT * FROM caches WHERE code = :code";
    $stmt = $db->prepare($sql);
    $stmt->bindParam(':code', $code, PDO::PARAM_STR);
    $stmt->execute();
    $cache = $stmt->fetchObject();
    if ($cache) {
        $sql = "SELECT * FROM logs WHERE cache_code = :code";
        $stmt = $db->prepare($sql);
        $stmt->bindParam(':code', $code, PDO::PARAM_STR);
        $stmt->execute();
        $logs = $stmt->fetchAll();
        $logs2 = array();
        foreach ($logs as $log) {
            $sql = 'SELECT * FROM logimages WHERE log_uuid = :log_uuid';
            $stmt = $db->prepare($sql);
            $stmt->bindParam(':log_uuid', $log['uuid'], PDO::PARAM_STR);
            $stmt->execute();
            $log['images'] = $stmt->fetchAll();
            array_push($logs2, $log);
        }
        header('Content-Type: application/json');
        http_response_code(200);
        echo json_encode(array('cache' => $cache, 'logs' => $logs2));
    } else {
        $error = true;
        array_push($messages, "ERROR: cannot find requested cache in DB.");
    }
} elseif ($user != "") {
    $db = new PDO('sqlite:' . $db_file);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $sql = "SELECT caches.code FROM caches, logs WHERE caches.code = logs.cache_code AND UPPER(logs.user) = :user AND logs.type = 'Found it'";
    $stmt = $db->prepare($sql);
    $stmt->bindParam(':user', $user, PDO::PARAM_STR);
    $stmt->execute();
    $codes = array();
    foreach ($stmt->fetchAll() as $cache) {
        array_push($codes, $cache['code']);
    }
    header('Content-Type: application/json');
    http_response_code(200);
    echo json_encode(array('user' => $user, 'caches' => $codes));
} elseif (!$error) {
    $error = true;
    array_push($messages, "ERROR: no 'code=OC...', no 'user=...' parameter.");
}

if ($error) {
    header('Content-Type: application/json');
    http_response_code(400);
    echo json_encode(array('messages' => $messages));
}

?>
