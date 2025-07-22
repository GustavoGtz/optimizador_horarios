<?php
require '../config/db.php';

$contratos = $pdo->query("SELECT * FROM Contrato")->fetchAll();
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Contratos</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
<h2>Contratos</h2>
<a href="create.php">Nuevo Contrato</a>
<table border="1">
    <tr>
        <th>ID</th>
        <th>Nombre</th>
        <th>Horas Mínimas</th>
        <th>Horas Máximas</th>
        <th>Acciones</th>
    </tr>
    <?php foreach ($contratos as $c): ?>
        <tr>
            <td><?= $c['id_contrato'] ?></td>
            <td><?= $c['nombre'] ?></td>
            <td><?= $c['horas_minimas'] ?></td>
            <td><?= $c['horas_maximas'] ?></td>
            <td>
                <a href="edit.php?id=<?= $c['id_contrato'] ?>">Editar</a> |
                <a href="delete.php?id=<?= $c['id_contrato'] ?>">Eliminar</a>
            </td>
        </tr>
    <?php endforeach; ?>
</table>
<a href="../index.php">Volver</a>
</body>
</html>
