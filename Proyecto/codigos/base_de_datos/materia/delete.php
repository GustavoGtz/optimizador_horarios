<?php
require '../config/db.php';

$id = $_GET['id'];

try {
    $stmt = $pdo->prepare("DELETE FROM Materia WHERE id_materia = :id");
    $stmt->execute(['id' => $id]);

    header("Location: index.php");
} catch (PDOException $e) {
    echo "<h3>No se puede eliminar la materia. Puede estar relacionada con profesores.</h3>";
    echo "<a href='index.php'>Volver</a>";
}
