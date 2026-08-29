<?php
/**
 * Visitor Counter API
 * Menggunakan GET request saja (tidak ada POST/CORS preflight).
 * Semua pengunjung website tercatat di sini.
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

$dataFile = __DIR__ . '/visitors_data.json';

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

$fp = fopen($dataFile, 'c');
if (!$fp) {
    echo json_encode(['success' => false, 'error' => 'Gagal membuka file data']);
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

// Jika ada parameter ?visit=1, catat kunjungan baru
if (isset($_GET['visit'])) {
    $data['totalCount'] = ($data['totalCount'] ?? 0) + 1;
    $data['todayCount'] = ($data['todayCount'] ?? 0) + 1;
    $data['monthCount'] = ($data['monthCount'] ?? 0) + 1;

    $countryCode = isset($_GET['c']) ? preg_replace('/[^a-z]/', '', strtolower($_GET['c'])) : 'id';
    if (!isset($data['countries'])) $data['countries'] = [];
    if (!isset($data['countries'][$countryCode])) $data['countries'][$countryCode] = 0;
    $data['countries'][$countryCode]++;

    $sid = isset($_GET['s']) ? preg_replace('/[^a-z0-9]/', '', $_GET['s']) : '';
    if ($sid === '') $sid = md5($_SERVER['REMOTE_ADDR'] . microtime());

    $now = time();
    $cutoff = $now - 300;
    if (!isset($data['recentVisitors'])) $data['recentVisitors'] = [];

    $data['recentVisitors'] = array_values(array_filter(
        $data['recentVisitors'],
        function ($v) use ($cutoff, $sid) { return $v['ts'] > $cutoff && $v['sid'] !== $sid; }
    ));

    $data['recentVisitors'][] = ['sid' => $sid, 'ts' => $now];
}

// Hitung online (pengunjung dalam 5 menit terakhir)
$now = time();
$cutoff = $now - 300;
$data['recentVisitors'] = array_values(array_filter(
    $data['recentVisitors'],
    function ($v) use ($cutoff) { return $v['ts'] > $cutoff; }
));
$onlineCount = count($data['recentVisitors']);

// Simpan
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
