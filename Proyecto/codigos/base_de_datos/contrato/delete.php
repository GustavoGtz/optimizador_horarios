<?php
require '../config/db.php';

$id = $_GET['id'];

try {
    $stmt = $pdo->prepare("DELETE FROM Contrato WHERE id_contrato = :id");
    $stmt->execute(['id' => $id]);
    header("Location: index.php");
} catch (PDOException $e) {
    echo "<h3>❌ No se puede eliminar el contrato porque está relacionado con profesores.</h3>";
    echo "<p>Primero reubica o elimina los profesores con este contrato.</p>";
    echo "<a href='index.php'>Volver</a>";
}
