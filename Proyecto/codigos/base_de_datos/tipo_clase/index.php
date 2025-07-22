<?php
require '../config/db.php';

// Obtener todos los tipos de clase
$tipos = $pdo->query("SELECT * FROM Tipo_Clase")->fetchAll();
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Tipos de Clase</title>
    <link rel="stylesheet" href="../style.css"> 
</head>
<body>
<h2>Tipos de Clase</h2>
<a href="create.php">Nuevo Tipo de Clase</a>
<table border="1">
    <tr>
        <th>ID</th>
        <th>Nombre</th>
        <th>Acciones</th>
    </tr>
    <?php foreach ($tipos as $t): ?>
        <tr>
            <td><?= $t['id_tipo_clase'] ?></td>
            <td><?= htmlspecialchars($t['nombre']) ?></td>
            <td>
                <a href="edit.php?id=<?= $t['id_tipo_clase'] ?>">Editar</a> |
                <a href="delete.php?id=<?= $t['id_tipo_clase'] ?>">Eliminar</a>
            </td>
        </tr>
    <?php endforeach; ?>
</table>
<a href="../index.php">Volver</a>
</body>
</html>
