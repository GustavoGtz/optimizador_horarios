<?php
require '../config/db.php';

$id = $_GET['id'];

// Obtener todas las unidades académicas para el menú desplegable
$unidades = $pdo->query("SELECT id_unidad_academica, nombre FROM Unidad_Academica")->fetchAll();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = $_POST['nombre'];
    $abreviatura = $_POST['abreviatura'];
    $id_unidad = $_POST['id_unidad_academica'];

    $stmt = $pdo->prepare("
        UPDATE Programa_Educativo 
        SET nombre = :nombre, abreviatura = :abreviatura, id_unidad_academica = :id_unidad
        WHERE id_programa_educativo = :id
    ");
    $stmt->execute([
        'nombre' => $nombre,
        'abreviatura' => $abreviatura,
        'id_unidad' => $id_unidad,
        'id' => $id
    ]);

    header("Location: index.php");
    exit;
} else {
    $stmt = $pdo->prepare("SELECT * FROM Programa_Educativo WHERE id_programa_educativo = :id");
    $stmt->execute(['id' => $id]);
    $programa = $stmt->fetch(PDO::FETCH_ASSOC);
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Editar Programa Educativo</title>
    <link rel="stylesheet" href="../style.css"> 
</head>
<body>
<h2>Editar Programa Educativo</h2>
<form method="POST">
    Nombre: <input type="text" name="nombre" value="<?= htmlspecialchars($programa['nombre']) ?>" required><br><br>
    Abreviatura: <input type="text" name="abreviatura" maxlength="5" value="<?= htmlspecialchars($programa['abreviatura']) ?>" required><br><br>

    Unidad Académica:
    <select name="id_unidad_academica" required>
        <?php foreach ($unidades as $u): ?>
            <option value="<?= $u['id_unidad_academica'] ?>" <?= $u['id_unidad_academica'] == $programa['id_unidad_academica'] ? 'selected' : '' ?>>
                <?= htmlspecialchars($u['nombre']) ?>
            </option>
        <?php endforeach; ?>
    </select><br><br>

    <button type="submit">Actualizar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
