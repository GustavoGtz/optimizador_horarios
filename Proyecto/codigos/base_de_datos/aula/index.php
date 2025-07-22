<?php
require '../config/db.php';

$aulas = $pdo->query("
    SELECT 
        a.id_aula,
        a.id_edificio,
        e.nombre AS edificio,
        t.nombre AS tipo_clase,
        a.cupo
    FROM Aula a
    JOIN Edificio e ON a.id_edificio = e.id_edificio
    JOIN Tipo_Clase t ON a.id_tipo_clase = t.id_tipo_clase
")->fetchAll();
?>
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Aulas</title></head>
<body>
<h2>Aulas</h2>
<a href="create.php">Nueva Aula</a>
<table border="1">
    <tr><th>ID Aula</th><th>Edificio</th><th>Tipo de Clase</th><th>Cupo</th><th>Acciones</th></tr>
    <?php foreach ($aulas as $a): ?>
        <tr>
            <td><?= $a['id_aula'] ?></td>
            <td><?= $a['edificio'] ?></td>
            <td><?= $a['tipo_clase'] ?></td>
            <td><?= $a['cupo'] ?></td>
            <td>
                <a href="edit.php?id_aula=<?= $a['id_aula'] ?>&id_edificio=<?= $a['id_edificio'] ?>">Editar</a> |
                <a href="delete.php?id_aula=<?= $a['id_aula'] ?>&id_edificio=<?= $a['id_edificio'] ?>">Eliminar</a>
            </td>
        </tr>
    <?php endforeach; ?>
</table>
<a href="../index.php">Volver</a>
</body>
</html>
