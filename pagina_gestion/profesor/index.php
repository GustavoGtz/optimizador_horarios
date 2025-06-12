<?php
require '../config/db.php';

$profesores = $pdo->query("
    SELECT p.*, c.nombre AS contrato_nombre
    FROM Profesor p
    JOIN Contrato c ON p.id_contrato = c.id_contrato
")->fetchAll();
?>
<!DOCTYPE html>
<html>
<head>
    <title>Profesores</title>
</head>
<body>
<h2>Lista de Profesores</h2>
<a href="create.php">Nuevo Profesor</a>
<table border="1">
    <tr>
        <th>ID Profesor</th>
        <th>Nombre</th>
        <th>Contrato</th>
        <th>Acciones</th>
    </tr>
    <?php foreach ($profesores as $profesor): ?>
        <tr>
            <td><?= $profesor['id_profesor'] ?></td>
            <td><?= htmlspecialchars($profesor['nombre']) ?></td>
            <td><?= htmlspecialchars($profesor['contrato_nombre']) ?></td>
            <td>
                <a href="edit.php?id=<?= $profesor['id_profesor'] ?>">Editar</a> |
                <a href="delete.php?id=<?= $profesor['id_profesor'] ?>" onclick="return confirm('¿Seguro que deseas eliminar?')">Eliminar</a>
            </td>
        </tr>
    <?php endforeach; ?>
</table>
<a href="../index.php">Volver al inicio</a>
</body>
</html>
