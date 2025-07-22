<?php
require '../config/db.php';

$programas = $pdo->query("
    SELECT 
        p.id_programa_educativo, 
        p.nombre AS nombre_programa, 
        p.abreviatura, 
        u.nombre AS nombre_unidad
    FROM Programa_Educativo p
    JOIN Unidad_Academica u ON p.id_unidad_academica = u.id_unidad_academica
")->fetchAll();
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Programas Educativos</title>
    <link rel="stylesheet" href="../style.css"> 
</head>
<body>
<h2>Programas Educativos</h2>
<a href="create.php">Nuevo Programa</a>
<table border="1">
    <tr>
        <th>ID</th>
        <th>Nombre</th>
        <th>Abreviatura</th>
        <th>Unidad Académica</th>
        <th>Acciones</th>
    </tr>
    <?php foreach ($programas as $p): ?>
        <tr>
            <td><?= $p['id_programa_educativo'] ?></td>
            <td><?= htmlspecialchars($p['nombre_programa']) ?></td>
            <td><?= htmlspecialchars($p['abreviatura']) ?></td>
            <td><?= htmlspecialchars($p['nombre_unidad']) ?></td>
            <td>
                <a href="edit.php?id=<?= $p['id_programa_educativo'] ?>">Editar</a> |
                <a href="delete.php?id=<?= $p['id_programa_educativo'] ?>">Eliminar</a>
            </td>
        </tr>
    <?php endforeach; ?>
</table>
<a href="../index.php">Volver</a>
</body>
</html>
