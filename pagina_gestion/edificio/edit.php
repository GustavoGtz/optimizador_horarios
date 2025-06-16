<?php
require '../config/db.php';

$id = $_GET['id'];

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = $_POST['nombre'];

    $stmt = $pdo->prepare("UPDATE Edificio SET nombre = :nombre WHERE id_edificio = :id");
    $stmt->execute(['nombre' => $nombre, 'id' => $id]);

    header("Location: index.php");
    exit;
} else {
    $stmt = $pdo->prepare("SELECT * FROM Edificio WHERE id_edificio = :id");
    $stmt->execute(['id' => $id]);
    $edificio = $stmt->fetch(PDO::FETCH_ASSOC);
}
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Editar Edificio</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
<h2>Editar Edificio</h2>
<form method="POST">
    Nombre: <input type="text" name="nombre" value="<?= $edificio['nombre'] ?>" required><br>
    <button type="submit">Actualizar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
