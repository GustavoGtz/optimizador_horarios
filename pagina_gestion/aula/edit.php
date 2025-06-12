<?php
require '../config/db.php';

$id_aula = $_GET['id_aula'];
$id_edificio = $_GET['id_edificio'];

$edificios = $pdo->query("SELECT nombre, id_edificio FROM Edificio")->fetchAll();
$tipos = $pdo->query("SELECT nombre, id_tipo_clase FROM Tipo_Clase")->fetchAll();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $id_tipo_clase = $_POST['id_tipo_clase'];
    $cupo = $_POST['cupo'];

    $stmt = $pdo->prepare("UPDATE Aula SET id_tipo_clase = :id_tipo_clase, cupo = :cupo
                           WHERE id_aula = :id_aula AND id_edificio = :id_edificio");
    $stmt->execute([
        'id_tipo_clase' => $id_tipo_clase,
        'cupo' => $cupo,
        'id_aula' => $id_aula,
        'id_edificio' => $id_edificio
    ]);

    header("Location: index.php");
} else {
    $stmt = $pdo->prepare("SELECT * FROM Aula WHERE id_aula = :id_aula AND id_edificio = :id_edificio");
    $stmt->execute(['id_aula' => $id_aula, 'id_edificio' => $id_edificio]);
    $aula = $stmt->fetch(PDO::FETCH_ASSOC);
}
?>
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Editar Aula</title></head>
<body>
<h2>Editar Aula</h2>
<form method="POST">
    Tipo de Clase:
    <select name="id_tipo_clase" required>
        <?php foreach ($tipos as $tipo): ?>
            <option value="<?= $tipo['id_tipo_clase'] ?>" <?= $tipo['id_tipo_clase'] == $aula['id_tipo_clase'] ? 'selected' : '' ?>>
                <?= $tipo['nombre'] ?>
            </option>
        <?php endforeach; ?>
    </select><br>
    Cupo: <input type="number" name="cupo" value="<?= $aula['cupo'] ?>" required><br>
    <button type="submit">Actualizar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
