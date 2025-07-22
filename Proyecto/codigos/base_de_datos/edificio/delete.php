<?php
require '../config/db.php';

$id = $_GET['id'];

try {
    $stmt = $pdo->prepare("DELETE FROM Edificio WHERE id_edificio = :id");
    $stmt->execute(['id' => $id]);

    header("Location: index.php");
} catch (PDOException $e) {
    echo "<h3>❌ No se puede eliminar el edificio porque está relacionado con alguna aula.</h3>";
    echo "<p>Primero elimina las aulas asociadas a este edificio.</p>";
    echo "<a href='index.php'>Volver</a>";
}
