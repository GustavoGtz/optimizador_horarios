<?php
require '../config/db.php';

$id_profesor = $_GET['id_profesor'];
$id_materia = $_GET['id_materia'];

$profesores = $pdo->query("SELECT id_profesor, nombre FROM Profesor")->fetchAll();
$materias = $pdo->query("SELECT id_materia, nombre FROM Materia")->fetchAll();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nuevo_id_profesor = $_POST['id_profesor'];
    $nuevo_id_materia = $_POST['id_materia'];

    // Eliminar la relación original
    $stmt = $pdo->prepare("DELETE FROM Profesor_Materia WHERE id_profesor = :id_profesor AND id_materia = :id_materia");
    $stmt->execute([
        'id_profesor' => $id_profesor,
        'id_materia' => $id_materia
    ]);

    // Insertar la nueva relación
    $stmt = $pdo->prepare("INSERT INTO Profesor_Materia (id_profesor, id_materia) VALUES (:nuevo_id_profesor, :nuevo_id_materia)");
    $stmt->execute([
        'nuevo_id_profesor' => $nuevo_id_profesor,
        'nuevo_id_materia' => $nuevo_id_materia
    ]);

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
<h2>Editar Asignación Profesor - Materia</h2>
<form method="POST">
    Profesor:
    <select name="id_profesor" required>
        <?php foreach ($profesores as $prof): ?>
            <option value="<?= $prof['id_profesor'] ?>" <?= $prof['id_profesor'] == $id_profesor ? 'selected' : '' ?>>
                <?= $prof['nombre'] ?>
            </option>
        <?php endforeach; ?>
    </select>

    Materia:
    <select name="id_materia" required>
        <?php foreach ($materias as $mat): ?>
            <option value="<?= $mat['id_materia'] ?>" <?= $mat['id_materia'] == $id_materia ? 'selected' : '' ?>>
                <?= $mat['nombre'] ?>
            </option>
        <?php endforeach; ?>
    </select>

    <button type="submit">Actualizar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
