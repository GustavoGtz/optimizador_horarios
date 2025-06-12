<?php
require '../config/db.php';

$id = $_GET['id'];

try {
    $stmt = $pdo->prepare("DELETE FROM Tipo_Clase WHERE id_tipo_clase = :id");
    $stmt->execute(['id' => $id]);
    header("Location: index.php");
} catch (PDOException $e) {
    echo "<h3>❌ No se puede eliminar el tipo de clase porque está asociado a otros registros.</h3>";
    echo "<p>Primero elimina las dependencias relacionadas antes de intentar eliminar este tipo de clase.</p>";
    echo "<a href='index.php'>Volver</a>";
}
