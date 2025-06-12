<?php
require '../config/db.php';

$id_aula = $_GET['id_aula'];
$id_edificio = $_GET['id_edificio'];

try {
    $stmt = $pdo->prepare("DELETE FROM Aula WHERE id_aula = :id_aula AND id_edificio = :id_edificio");
    $stmt->execute(['id_aula' => $id_aula, 'id_edificio' => $id_edificio]);
    header("Location: index.php");
} catch (PDOException $e) {
    echo "<h3>❌ No se puede eliminar el aula porque tiene registros asociados.</h3>";
    echo "<a href='index.php'>Volver</a>";
}
?>
