<?php
require '../config/db.php';

$id = $_GET['id'];

try {
    $stmt = $pdo->prepare("DELETE FROM Unidad_Academica WHERE id_unidad_academica = :id");
    $stmt->execute(['id' => $id]);
    header("Location: index.php");
} catch (PDOException $e) {
    echo "<h3>❌ No se puede eliminar la unidad académica porque está relacionada con otros registros.</h3>";
    echo "<p>Primero elimina o reubica los programas educativos o elementos asociados a esta unidad académica.</p>";
    echo "<a href='index.php'>Volver</a>";
}
