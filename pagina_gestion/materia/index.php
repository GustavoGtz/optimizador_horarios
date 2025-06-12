<?php
require '../config/db.php';

$materias = $pdo->query("
    SELECT m.*, t.nombre AS tipo_nombre, p.nombre AS programa_nombre
    FROM Materia m
    JOIN Tipo_Clase t ON m.id_tipo_clase = t.id_tipo_clase
    JOIN Programa_Educativo p ON m.id_programa_educativo = p.id_programa_educativo
")->fetchAll();
?>
<!DOCTYPE html>
<html>
<head>
    <title>Materias</title>
</head>
<body>
<h2>Lista de Materias</h2>
<a href="create.php">Nueva Materia</a>
<table border="1">
    <tr>
        <th>ID</th>
        <th>Clave</th>
        <th>Nombre</th>
        <th>Créditos</th>
        <th>Semestre</th>
        <th>Horas/Semana</th>
        <th>Tipo</th>
        <th>Programa</th>
        <th>Acciones</th>
    </tr>
    <?php foreach ($materias as $m): ?>
        <tr>
            <td><?= $m['id_materia'] ?></td>
            <td><?= $m['clave'] ?></td>
            <td><?= $m['nombre'] ?></td>
            <td><?= $m['creditos'] ?></td>
            <td><?= $m['semestre'] ?></td>
            <td><?= $m['horas_por_semana'] ?></td>
            <td><?= $m['tipo_nombre'] ?></td>
            <td><?= $m['programa_nombre'] ?></td>
            <td>
                <a href="edit.php?id=<?= $m['id_materia'] ?>">Editar</a> |
                <a href="delete.php?id=<?= $m['id_materia'] ?>">Eliminar</a>
            </td>
        </tr>
    <?php endforeach; ?>
</table>
<a href="../index.php">Volver al inicio</a>
</body>
</html>
