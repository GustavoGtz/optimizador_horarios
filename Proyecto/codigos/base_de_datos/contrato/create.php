<?php
require '../config/db.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = $_POST['nombre'];
    $horas_min = $_POST['horas_minimas'];
    $horas_max = $_POST['horas_maximas'];

    $stmt = $pdo->prepare("INSERT INTO Contrato (nombre, horas_minimas, horas_maximas) VALUES (:nombre, :min, :max)");
    $stmt->execute([
        'nombre' => $nombre,
        'min' => $horas_min,
        'max' => $horas_max
    ]);

    header("Location: index.php");
    exit;
}
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Nuevo Contrato</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
<h2>Nuevo Contrato</h2>
<form method="POST">
    Nombre: <input type="text" name="nombre" required><br>
    Horas Mínimas: <input type="number" name="horas_minimas" required><br>
    Horas Máximas: <input type="number" name="horas_maximas" required><br>
    <button type="submit">Guardar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
