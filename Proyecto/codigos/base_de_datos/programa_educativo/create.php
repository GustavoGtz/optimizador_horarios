<?php
require '../config/db.php';

// Obtener todas las unidades académicas para el selector
$unidades = $pdo->query("SELECT id_unidad_academica, nombre FROM Unidad_Academica")->fetchAll();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = $_POST['nombre'];
    $abreviatura = $_POST['abreviatura'];
    $id_unidad = $_POST['id_unidad_academica'];

    $stmt = $pdo->prepare("
        INSERT INTO Programa_Educativo (nombre, abreviatura, id_unidad_academica)
        VALUES (:nombre, :abreviatura, :id_unidad)
    ");
    $stmt->execute([
        'nombre' => $nombre,
        'abreviatura' => $abreviatura,
        'id_unidad' => $id_unidad
    ]);

    header("Location: index.php");
    exit;
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Nuevo Programa Educativo</title>
    <link rel="stylesheet" href="../style.css"> 
</head>
<body>
<h2>Nuevo Programa Educativo</h2>
<form method="POST">
    Nombre: <input type="text" name="nombre" required><br><br>
    Abreviatura: <input type="text" name="abreviatura" maxlength="5" required><br><br>

    Unidad Académica:
    <select name="id_unidad_academica" required>
        <option value="">Seleccione una unidad académica</option>
        <?php foreach ($unidades as $u): ?>
            <option value="<?= $u['id_unidad_academica'] ?>">
                <?= htmlspecialchars($u['nombre']) ?>
            </option>
        <?php endforeach; ?>
    </select><br><br>

    <button type="submit">Guardar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
