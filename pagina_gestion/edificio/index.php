<?php
require '../config/db.php';

$edificios = $pdo->query("SELECT * FROM Edificio")->fetchAll();
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Edificios</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
<h2>Lista de Edificios</h2>
<a href="create.php">Nuevo Edificio</a>
<table border="1">
    <tr>
        <th>ID</th>
        <th>Nombre</th>
        <th>Acciones</th>
    </tr>
    <?php foreach ($edificios as $e): ?>
        <tr>
            <td><?= $e['id_edificio'] ?></td>
            <td><?= $e['nombre'] ?></td>
            <td>
                <a href="edit.php?id=<?= $e['id_edificio'] ?>">Editar</a> |
                <a href="delete.php?id=<?= $e['id_edificio'] ?>">Eliminar</a>
            </td>
        </tr>
    <?php endforeach; ?>
</table>
<a href="../index.php">Volver</a>
</body>
</html>
