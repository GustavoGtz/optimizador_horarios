<?php
require '../config/db.php';

$id = $_GET['id'];

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = $_POST['nombre'];
    $abreviatura = $_POST['abreviatura'];

    $stmt = $pdo->prepare("UPDATE Unidad_Academica SET nombre = :nombre, abreviatura = :abreviatura WHERE id_unidad_academica = :id");
    $stmt->execute([
        'nombre' => $nombre,
        'abreviatura' => $abreviatura,
        'id' => $id
    ]);

    header("Location: index.php");
    exit;
} else {
    $stmt = $pdo->prepare("SELECT * FROM Unidad_Academica WHERE id_unidad_academica = :id");
    $stmt->execute(['id' => $id]);
    $unidad = $stmt->fetch(PDO::FETCH_ASSOC);
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Editar Unidad Académica</title>
    <link rel="stylesheet" href="../style.css"> 
</head>
<body>
<h2>Editar Unidad Académica</h2>
<form method="POST">
    Nombre: <input type="text" name="nombre" value="<?= htmlspecialchars($unidad['nombre']) ?>" required><br><br>
    Abreviatura: <input type="text" name="abreviatura" maxlength="5" value="<?= htmlspecialchars($unidad['abreviatura']) ?>" required><br><br>
    <button type="submit">Actualizar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
