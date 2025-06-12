<?php
require '../config/db.php';

$relaciones = $pdo->query("
    SELECT 
        pm.id_profesor,
        pm.id_materia,
        p.nombre AS nombre_profesor,
        m.nombre AS nombre_materia
    FROM Profesor_Materia pm
    JOIN Profesor p ON pm.id_profesor = p.id_profesor
    JOIN Materia m ON pm.id_materia = m.id_materia
")->fetchAll();
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Asignación Profesor-Materia</title>
    <link rel="stylesheet" href="../style.css"> 
</head>
<body>
<h2>Relaciones Profesor - Materia</h2>
<a href="create.php">Nueva Asignación</a>

<table border="1">
    <tr>
        <th>Profesor</th>
        <th>Materia</th>
        <th>Acciones</th>
    </tr>
    <?php foreach ($relaciones as $r): ?>
        <tr>
            <td><?= htmlspecialchars($r['nombre_profesor']) ?></td>
            <td><?= htmlspecialchars($r['nombre_materia']) ?></td>
            <td>
                <a href="edit.php?id_profesor=<?= $r['id_profesor'] ?>&id_materia=<?= $r['id_materia'] ?>">Editar</a> |
                <a href="delete.php?id_profesor=<?= $r['id_profesor'] ?>&id_materia=<?= $r['id_materia'] ?>">Eliminar</a>
            </td>
        </tr>
    <?php endforeach; ?>
</table>
<a href="../index.php">Volver</a>
</body>
</html>
