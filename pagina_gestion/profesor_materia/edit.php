<?php
require '../config/db.php';

$id_profesor_original = $_GET['id_profesor'];
$id_materia_original = $_GET['id_materia'];

$profesores = $pdo->query("SELECT id_profesor, nombre FROM Profesor")->fetchAll();
$materias = $pdo->query("SELECT id_materia, nombre FROM Materia")->fetchAll();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nuevo_profesor = $_POST['id_profesor'];
    $nueva_materia = $_POST['id_materia'];

    // Eliminar relación antigua
    $pdo->prepare("DELETE FROM Profesor_Materia WHERE id_profesor = :idp AND id_materia = :idm")
        ->execute(['idp' => $id_profesor_original, 'idm' => $id_materia_original]);

    // Insertar nueva
    $pdo->prepare("INSERT INTO Profesor_Materia (id_profesor, id_materia) VALUES (:idp, :idm)")
        ->execute(['idp' => $nuevo_profesor, 'idm' => $nueva_materia]);

    header("Location: index.php");
    exit;
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Editar Asignación</title>
    <link rel="stylesheet" href="../style.css"> 
</head>
<body>
<h2>Editar Asignación</h2>
<form method="POST">
    Profesor:
    <select name="id_profesor" required>
        <?php foreach ($profesores as $p): ?>
            <option value="<?= $p['id_profesor'] ?>" <?= $p['id_profesor'] == $id_profesor_original ? 'selected' : '' ?>>
                <?= htmlspecialchars($p['nombre']) ?>
            </option>
        <?php endforeach; ?>
    </select>

    Materia:
    <select name="id_materia" required>
        <?php foreach ($materias as $m): ?>
            <option value="<?= $m['id_materia'] ?>" <?= $m['id_materia'] == $id_materia_original ? 'selected' : '' ?>>
                <?= htmlspecialchars($m['nombre']) ?>
            </option>
        <?php endforeach; ?>
    </select>

    <button type="submit">Actualizar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
