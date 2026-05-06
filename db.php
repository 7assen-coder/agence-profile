<?php
$host    = 'localhost';
$db      = 'transport_reservation';
$user    = 'root';
$pass    = '';
$charset = 'utf8mb4'; 

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";

$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

try {
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (PDOException $e) {
    // En production, évitez d'afficher le message d'erreur brut aux utilisateurs
    die("Erreur de connexion : " . $e->getMessage());
}
?>