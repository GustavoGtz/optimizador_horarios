<?php
require '../config/db.php';

$id_profesor = $_GET['id_profesor'];
$id_materia = $_GET['id_materia'];

try {
    $stmt = $pdo->prepare("DELETE FROM Profesor_Materia WHERE id_profesor = :idp AND id_materia = :idm");
    $stmt->execute(['idp' => $id_profesor, 'idm' => $id_materia]);
    header("Location: index.php");
} catch (PDOException $e) {
    echo "<h3>❌ No se pudo eliminar la relación.</h3>";
    echo "<p>Puede estar siendo usada en otra parte del sistema.</p>";
    echo "<a href='index.php'>Volver</a>";
}
