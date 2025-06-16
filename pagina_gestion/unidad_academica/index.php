<?php
require '../config/db.php';

// Obtener todas las unidades académicas
$unidades = $pdo->query("SELECT * FROM Unidad_Academica")->fetchAll();
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Unidades Académicas</title>
    <link rel="stylesheet" href="../style.css"> 
</head>
<body>
<h2>Unidades Académicas</h2>
<a href="create.php">Nueva Unidad Académica</a>
<table border="1">
    <tr>
        <th>ID</th>
        <th>Nombre</th>
        <th>Abreviatura</th>
        <th>Acciones</th>
    </tr>
    <?php foreach ($unidades as $u): ?>
        <tr>
            <td><?= $u['id_unidad_academica'] ?></td>
            <td><?= htmlspecialchars($u['nombre']) ?></td>
            <td><?= htmlspecialchars($u['abreviatura']) ?></td>
            <td>
                <a href="edit.php?id=<?= $u['id_unidad_academica'] ?>">Editar</a> |
                <a href="delete.php?id=<?= $u['id_unidad_academica'] ?>">Eliminar</a>
            </td>
        </tr>
    <?php endforeach; ?>
</table>
<a href="../index.php">Volver</a>
</body>
</html>
