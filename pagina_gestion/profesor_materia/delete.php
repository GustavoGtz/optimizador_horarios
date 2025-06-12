<?php
require '../config/db.php';

$id_profesor = $_GET['id_profesor'];
$id_materia = $_GET['id_materia'];

try {
    $stmt = $pdo->prepare("DELETE FROM Profesor_Materia WHERE id_profesor = :id_profesor AND id_materia = :id_materia");
    $stmt->execute([
        'id_profesor' => $id_profesor,
        'id_materia' => $id_materia
    ]);
    header("Location: index.php");
    exit;
} catch (PDOException $e) {
    echo "<h3>❌ No se puede eliminar la asignación porque tiene dependencias asociadas.</h3>";
    echo "<p>Primero asegúrate de que esta relación no esté siendo usada en otra parte del sistema.</p>";
    echo "<a href='index.php'>Volver</a>";
}
?>
