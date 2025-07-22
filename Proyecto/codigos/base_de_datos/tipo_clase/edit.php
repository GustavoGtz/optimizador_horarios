<?php
require '../config/db.php';

$id = $_GET['id'];

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = $_POST['nombre'];

    $stmt = $pdo->prepare("UPDATE Tipo_Clase SET nombre = :nombre WHERE id_tipo_clase = :id");
    $stmt->execute([
        'nombre' => $nombre,
        'id' => $id
    ]);

    header("Location: index.php");
    exit;
} else {
    $stmt = $pdo->prepare("SELECT * FROM Tipo_Clase WHERE id_tipo_clase = :id");
    $stmt->execute(['id' => $id]);
    $tipo_clase = $stmt->fetch(PDO::FETCH_ASSOC);
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Editar Tipo de Clase</title>
    <link rel="stylesheet" href="../style.css"> 
</head>
<body>
<h2>Editar Tipo de Clase</h2>
<form method="POST">
    Nombre: <input type="text" name="nombre" value="<?= htmlspecialchars($tipo_clase['nombre']) ?>" required><br><br>
    <button type="submit">Actualizar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
