<?php
require '../config/db.php';

// Obtener edificios y tipos de clase
$edificios = $pdo->query("SELECT nombre, id_edificio FROM Edificio")->fetchAll();
$tipos = $pdo->query("SELECT nombre, id_tipo_clase FROM Tipo_Clase")->fetchAll();

// Calcular siguiente ID de aula
$maxId = $pdo->query("SELECT MAX(id_aula) as max_id FROM Aula")->fetch(PDO::FETCH_ASSOC);
$nextId = $maxId['max_id'] + 1;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $id_aula = $_POST['id_aula'];
    $id_edificio = $_POST['id_edificio'];
    $id_tipo_clase = $_POST['id_tipo_clase'];
    $cupo = $_POST['cupo'];

    $stmt = $pdo->prepare("INSERT INTO Aula (id_aula, id_edificio, id_tipo_clase, cupo)
                           VALUES (:id_aula, :id_edificio, :id_tipo_clase, :cupo)");
    $stmt->execute([
        'id_aula' => $id_aula,
        'id_edificio' => $id_edificio,
        'id_tipo_clase' => $id_tipo_clase,
        'cupo' => $cupo
    ]);

    header("Location: index.php");
    exit;
}
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Nueva Aula</title>
</head>
<body>
<h2>Nueva Aula</h2>
<form method="POST">
    ID Aula: <input type="number" name="id_aula" value="<?= $nextId ?>" required readonly><br>
    Edificio:
    <select name="id_edificio" required>
        <option value="">Seleccione un edificio</option>
        <?php foreach ($edificios as $edificio): ?>
            <option value="<?= $edificio['id_edificio'] ?>"><?= $edificio['nombre'] ?></option>
        <?php endforeach; ?>
    </select><br>
    Tipo de Clase:
    <select name="id_tipo_clase" required>
        <option value="">Seleccione un tipo</option>
        <?php foreach ($tipos as $tipo): ?>
            <option value="<?= $tipo['id_tipo_clase'] ?>"><?= $tipo['nombre'] ?></option>
        <?php endforeach; ?>
    </select><br>
    Cupo: <input type="number" name="cupo" required><br>
    <button type="submit">Guardar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
