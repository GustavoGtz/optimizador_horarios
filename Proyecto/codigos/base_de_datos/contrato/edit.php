<?php
require '../config/db.php';

$id = $_GET['id'];

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = $_POST['nombre'];
    $horas_min = $_POST['horas_minimas'];
    $horas_max = $_POST['horas_maximas'];

    $stmt = $pdo->prepare("UPDATE Contrato SET nombre = :nombre, horas_minimas = :min, horas_maximas = :max WHERE id_contrato = :id");
    $stmt->execute([
        'nombre' => $nombre,
        'min' => $horas_min,
        'max' => $horas_max,
        'id' => $id
    ]);
    header("Location: index.php");
    exit;
} else {
    $stmt = $pdo->prepare("SELECT * FROM Contrato WHERE id_contrato = :id");
    $stmt->execute(['id' => $id]);
    $contrato = $stmt->fetch(PDO::FETCH_ASSOC);
}
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Editar Contrato</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
<h2>Editar Contrato</h2>
<form method="POST">
    Nombre: <input type="text" name="nombre" value="<?= $contrato['nombre'] ?>" required><br>
    Horas Mínimas: <input type="number" name="horas_minimas" value="<?= $contrato['horas_minimas'] ?>" required><br>
    Horas Máximas: <input type="number" name="horas_maximas" value="<?= $contrato['horas_maximas'] ?>" required><br>
    <button type="submit">Actualizar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
