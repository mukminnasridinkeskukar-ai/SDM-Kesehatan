<?php
error_reporting(0);
ini_set('display_errors', '0');
ob_start();
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

function fetchUrl($url) {
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 5);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 3);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_USERAGENT, 'VisitorCounter/1.0');
        $result = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        return ($httpCode >= 200 && $httpCode < 300) ? $result : false;
    }
    if (ini_get('allow_url_fopen')) {
        $ctx = stream_context_create(['http' => ['timeout' => 5, 'header' => "User-Agent: VisitorCounter/1.0\r\n"]]);
        $result = @file_get_contents($url, false, $ctx);
        return ($result !== false) ? $result : false;
    }
    return false;
}

function getVisitorIP() {
    if (!empty($_SERVER['HTTP_CF_CONNECTING_IP'])) return $_SERVER['HTTP_CF_CONNECTING_IP'];
    if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) { $ips = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']); return trim($ips[0]); }
    return $_SERVER['REMOTE_ADDR'];
}

function geoLookup($ip) {
    $json = fetchUrl('http://ip-api.com/json/' . $ip . '?fields=status,countryCode,country,city,regionName');
    if ($json) { $d = json_decode($json, true); if (isset($d['status']) && $d['status'] === 'success') return ['code' => strtolower($d['countryCode']), 'name' => $d['country'], 'city' => $d['city'] ?? '', 'region' => $d['regionName'] ?? '']; }
    $json2 = fetchUrl('https://ipwho.is/' . $ip);
    if ($json2) { $d2 = json_decode($json2, true); if (isset($d2['country_code'])) return ['code' => strtolower($d2['country_code']), 'name' => $d2['country'] ?? 'Unknown', 'city' => $d2['city'] ?? '', 'region' => $d2['region'] ?? '']; }
    $json3 = fetchUrl('https://ipapi.co/' . $ip . '/json/');
    if ($json3) { $d3 = json_decode($json3, true); if (isset($d3['country_code']) && !isset($d3['error'])) return ['code' => strtolower($d3['country_code']), 'name' => $d3['country_name'] ?? 'Unknown', 'city' => $d3['city'] ?? '', 'region' => $d3['region'] ?? '']; }
    return null;
}

try {
    $dataFile = __DIR__ . '/visitors_data.json';
    if (!file_exists($dataFile)) { $initial = ['totalCount' => 0, 'todayCount' => 0, 'todayDate' => date('Y-m-d'), 'monthCount' => 0, 'monthDate' => date('Y-m'), 'countries' => [], 'recentVisitors' => [], 'ipCache' => []]; @file_put_contents($dataFile, json_encode($initial, JSON_PRETTY_PRINT), LOCK_EX); }
    $fp = @fopen($dataFile, 'c');
    if (!$fp) { ob_end_clean(); echo json_encode(['success' => false, 'error' => 'Cannot open data file']); exit; }
    flock($fp, LOCK_EX);
    $content = stream_get_contents($fp);
    $data = json_decode($content, true);
    if (!$data) $data = [];
    $today = date('Y-m-d'); $month = date('Y-m');
    if (!isset($data['todayDate']) || $data['todayDate'] !== $today) { $data['todayCount'] = 0; $data['todayDate'] = $today; }
    if (!isset($data['monthDate']) || $data['monthDate'] !== $month) { $data['monthCount'] = 0; $data['monthDate'] = $month; }
    $visitorGeo = null; $countryCode = 'id';

    if (isset($_GET['visit'])) {
        $ip = getVisitorIP();
        $sid = isset($_GET['s']) ? preg_replace('/[^a-z0-9]/', '', $_GET['s']) : '';
        if ($sid === '') $sid = md5($ip . microtime());
        if (!isset($data['ipCache'])) $data['ipCache'] = [];
        if (isset($data['ipCache'][$ip]) && (time() - $data['ipCache'][$ip]['t']) < 86400) { $visitorGeo = $data['ipCache'][$ip]['geo']; } else { $visitorGeo = geoLookup($ip); if ($visitorGeo) $data['ipCache'][$ip] = ['geo' => $visitorGeo, 't' => time()]; }
        if (count($data['ipCache']) > 300) { uasort($data['ipCache'], function($a, $b) { return $b['t'] - $a['t']; }); $data['ipCache'] = array_slice($data['ipCache'], 0, 300, true); }
        if ($visitorGeo && isset($visitorGeo['code'])) $countryCode = $visitorGeo['code'];
        $data['totalCount'] = ($data['totalCount'] ?? 0) + 1;
        $data['todayCount'] = ($data['todayCount'] ?? 0) + 1;
        $data['monthCount'] = ($data['monthCount'] ?? 0) + 1;
        if (!isset($data['countries'])) $data['countries'] = [];
        if (!isset($data['countries'][$countryCode])) $data['countries'][$countryCode] = 0;
        $data['countries'][$countryCode]++;
        $now = time(); $cutoff = $now - 300;
        if (!isset($data['recentVisitors'])) $data['recentVisitors'] = [];
        $data['recentVisitors'] = array_values(array_filter($data['recentVisitors'], function ($v) use ($cutoff, $sid) { return $v['ts'] > $cutoff && $v['sid'] !== $sid; }));
        $data['recentVisitors'][] = ['sid' => $sid, 'ts' => $now];
    } else {
        if (isset($_GET['s'])) {
            $sid = preg_replace('/[^a-z0-9]/', '', $_GET['s']); $now = time(); $cutoff = $now - 300;
            if (!isset($data['recentVisitors'])) $data['recentVisitors'] = [];
            $found = false;
            foreach ($data['recentVisitors'] as &$v) { if ($v['sid'] === $sid) { $v['ts'] = $now; $found = true; break; } }
            unset($v);
            if (!$found) $data['recentVisitors'][] = ['sid' => $sid, 'ts' => $now];
            $data['recentVisitors'] = array_values(array_filter($data['recentVisitors'], function ($v) use ($cutoff) { return $v['ts'] > $cutoff; }));
        }
    }
    $now = time(); $cutoff = $now - 300;
    if (isset($data['recentVisitors'])) $data['recentVisitors'] = array_values(array_filter($data['recentVisitors'], function ($v) use ($cutoff) { return $v['ts'] > $cutoff; }));
    $onlineCount = count($data['recentVisitors'] ?? []);
    ftruncate($fp, 0); rewind($fp);
    fwrite($fp, json_encode($data, JSON_PRETTY_PRINT));
    flock($fp, LOCK_UN); fclose($fp);
    ob_end_clean();
    echo json_encode(['success' => true, 'totalCount' => $data['totalCount'] ?? 0, 'todayCount' => $data['todayCount'] ?? 0, 'monthCount' => $data['monthCount'] ?? 0, 'onlineCount' => $onlineCount, 'countries' => $data['countries'] ?? [], 'todayDate' => $data['todayDate'] ?? $today, 'monthDate' => $data['monthDate'] ?? $month, 'visitorGeo' => $visitorGeo]);
} catch (Exception $e) { ob_end_clean(); echo json_encode(['success' => false, 'error' => $e->getMessage()]); }
