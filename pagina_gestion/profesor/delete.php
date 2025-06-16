<?php
require '../config/db.php';

$id = $_GET['id'];

try {
    $stmt = $pdo->prepare("DELETE FROM Profesor WHERE id_profesor = :id");
    $stmt->execute(['id' => $id]);

    header("Location: index.php");
} catch (PDOException $e) {
    echo "<h3>No se puede eliminar el profesor. Puede estar relacionado con materias.</h3>";
    echo "<a href='index.php'>Volver</a>";
}
