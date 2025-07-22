<?php
require '../config/db.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = $_POST['nombre'];
    $abreviatura = $_POST['abreviatura'];

    $stmt = $pdo->prepare("INSERT INTO Unidad_Academica (nombre, abreviatura) VALUES (:nombre, :abreviatura)");
    $stmt->execute([
        'nombre' => $nombre,
        'abreviatura' => $abreviatura
    ]);

    header("Location: index.php");
    exit;
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Nueva Unidad Académica</title>
    <link rel="stylesheet" href="../style.css"> 
</head>
<body>
<h2>Nueva Unidad Académica</h2>
<form method="POST">
    Nombre: <input type="text" name="nombre" required><br><br>
    Abreviatura: <input type="text" name="abreviatura" maxlength="5" required><br><br>

    <button type="submit">Guardar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
