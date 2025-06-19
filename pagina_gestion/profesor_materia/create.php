<?php
require '../config/db.php';

$profesores = $pdo->query("SELECT id_profesor, nombre FROM Profesor")->fetchAll();
$materias = $pdo->query("SELECT id_materia, nombre FROM Materia")->fetchAll();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $id_profesor = $_POST['id_profesor'];
    $id_materia = $_POST['id_materia'];
    $veces_impartida = $_POST['veces_impartida'];

    $stmt = $pdo->prepare("
        INSERT INTO Profesor_Materia (id_profesor, id_materia, veces_impartida)
        VALUES (:id_profesor, :id_materia, :veces_impartida)
    ");
    $stmt->execute([
        'id_profesor' => $id_profesor,
        'id_materia' => $id_materia,
        'veces_impartida' => $veces_impartida
    ]);

    header("Location: index.php");
    exit;
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Nueva Asignación</title>
    <link rel="stylesheet" href="../style.css"> 
</head>
<body>
<h2>Asignar Profesor a Materia</h2>
<form method="POST">
    <label>Profesor:</label>
    <select name="id_profesor" required>
        <option value="">Seleccione un profesor</option>
        <?php foreach ($profesores as $p): ?>
            <option value="<?= $p['id_profesor'] ?>"><?= htmlspecialchars($p['nombre']) ?></option>
        <?php endforeach; ?>
    </select><br><br>

    <label>Materia:</label>
    <select name="id_materia" required>
        <option value="">Seleccione una materia</option>
        <?php foreach ($materias as $m): ?>
            <option value="<?= $m['id_materia'] ?>"><?= htmlspecialchars($m['nombre']) ?></option>
        <?php endforeach; ?>
    </select><br><br>

    <label>Veces Impartida:</label>
    <input type="number" name="veces_impartida" min="1" value="1" required><br><br>

    <button type="submit">Guardar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
