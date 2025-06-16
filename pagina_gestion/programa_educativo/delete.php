<?php
require '../config/db.php';

$id = $_GET['id'];

try {
    $stmt = $pdo->prepare("DELETE FROM Programa_Educativo WHERE id_programa_educativo = :id");
    $stmt->execute(['id' => $id]);
    header("Location: index.php");
} catch (PDOException $e) {
    echo "<h3>❌ No se puede eliminar el programa educativo porque está relacionado con otros registros.</h3>";
    echo "<p>Primero asegúrate de eliminar las dependencias asociadas a este programa.</p>";
    echo "<a href='index.php'>Volver</a>";
}
