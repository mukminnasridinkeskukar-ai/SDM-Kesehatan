<?php
/**
 * Visitor Counter API
 * Menyimpan data pengunjung secara terpusat menggunakan file JSON.
 * Semua pengunjung website tercatat di sini.
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

$dataFile = __DIR__ . '/visitors_data.json';

defaultData();

function defaultData() {
    global $dataFile;
    if (!file_exists($dataFile)) {
        $initial = [
            'totalCount' => 0,
            'todayCount' => 0,
            'todayDate'  => date('Y-m-d'),
            'monthCount' => 0,
            'monthDate'  => date('Y-m'),
            'countries'  => [],
            'recentVisitors' => []
        ];
        file_put_contents($dataFile, json_encode($initial, JSON_PRETTY_PRINT));
    }
}

function readData() {
    global $dataFile;
    $fp = fopen($dataFile, 'r');
    if (!$fp) return null;
    flock($fp, LOCK_SH);
    $content = stream_get_contents($fp);
    flock($fp, LOCK_UN);
    fclose($fp);
    return json_decode($content, true);
}

function writeData($data) {
    global $dataFile;
    $fp = fopen($dataFile, 'c');
    if (!$fp) return false;
    flock($fp, LOCK_EX);
    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, json_encode($data, JSON_PRETTY_PRINT));
    flock($fp, LOCK_UN);
    fclose($fp);
    return true;
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $data = readData();
    if ($data === null) {
        echo json_encode(['error' => 'Gagal membaca data']);
        exit;
    }

    $today = date('Y-m-d');
    $month = date('Y-m');
    $changed = false;

    if ($data['todayDate'] !== $today) {
        $data['todayCount'] = 0;
        $data['todayDate'] = $today;
        $changed = true;
    }
    if ($data['monthDate'] !== $month) {
        $data['monthCount'] = 0;
        $data['monthDate'] = $month;
        $changed = true;
    }

    $now = time();
    $cutoff = $now - 300;
    $data['recentVisitors'] = array_values(array_filter(
        $data['recentVisitors'],
        function ($v) use ($cutoff) { return $v['ts'] > $cutoff; }
    ));
    $onlineCount = count($data['recentVisitors']);

    if ($changed) writeData($data);

    echo json_encode([
        'success'       => true,
        'totalCount'    => $data['totalCount'],
        'todayCount'    => $data['todayCount'],
        'monthCount'    => $data['monthCount'],
        'onlineCount'   => $onlineCount,
        'countries'     => $data['countries'],
        'todayDate'     => $data['todayDate'],
        'monthDate'     => $data['monthDate']
    ]);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    if (!$input) $input = [];

    $fp = fopen($dataFile, 'c');
    if (!$fp) {
        echo json_encode(['error' => 'Gagal membuka file data']);
        exit;
    }

    flock($fp, LOCK_EX);
    $content = stream_get_contents($fp);
    $data = json_decode($content, true);
    if (!$data) $data = [];

    $today = date('Y-m-d');
    $month = date('Y-m');

    if (!isset($data['todayDate']) || $data['todayDate'] !== $today) {
        $data['todayCount'] = 0;
        $data['todayDate'] = $today;
    }
    if (!isset($data['monthDate']) || $data['monthDate'] !== $month) {
        $data['monthCount'] = 0;
        $data['monthDate'] = $month;
    }

    $data['totalCount'] = ($data['totalCount'] ?? 0) + 1;
    $data['todayCount'] = ($data['todayCount'] ?? 0) + 1;
    $data['monthCount'] = ($data['monthCount'] ?? 0) + 1;

    $countryCode = isset($input['countryCode']) ? strtolower($input['countryCode']) : 'id';
    if (!isset($data['countries'])) $data['countries'] = [];
    if (!isset($data['countries'][$countryCode])) $data['countries'][$countryCode] = 0;
    $data['countries'][$countryCode]++;

    $sessionId = isset($input['sessionId']) ? $input['sessionId'] : session_id();
    $now = time();
    $cutoff = $now - 300;

    if (!isset($data['recentVisitors'])) $data['recentVisitors'] = [];

    $data['recentVisitors'] = array_values(array_filter(
        $data['recentVisitors'],
        function ($v) use ($cutoff, $sessionId) { return $v['ts'] > $cutoff && $v['sid'] !== $sessionId; }
    ));

    $data['recentVisitors'][] = ['sid' => $sessionId, 'ts' => $now];
    $onlineCount = count($data['recentVisitors']);

    ftruncate($fp, 0);
    rewind($fp);
    fwrite($fp, json_encode($data, JSON_PRETTY_PRINT));
    flock($fp, LOCK_UN);
    fclose($fp);

    echo json_encode([
        'success'     => true,
        'totalCount'  => $data['totalCount'],
        'todayCount'  => $data['todayCount'],
        'monthCount'  => $data['monthCount'],
        'onlineCount' => $onlineCount,
        'countries'   => $data['countries'],
        'todayDate'   => $data['todayDate'],
        'monthDate'   => $data['monthDate']
    ]);
    exit;
}

echo json_encode(['error' => 'Method not allowed']);
