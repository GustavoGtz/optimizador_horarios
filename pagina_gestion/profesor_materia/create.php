<?php
require '../config/db.php';

// Obtener profesores y materias para llenar el formulario
$profesores = $pdo->query("SELECT id_profesor, nombre FROM Profesor")->fetchAll();
$materias = $pdo->query("SELECT id_materia, nombre FROM Materia")->fetchAll();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $id_profesor = $_POST['id_profesor'];
    $id_materia = $_POST['id_materia'];

    $stmt = $pdo->prepare("INSERT INTO Profesor_Materia (id_profesor, id_materia) VALUES (:id_profesor, :id_materia)");
    $stmt->execute([
        'id_profesor' => $id_profesor,
        'id_materia' => $id_materia
    ]);

    header("Location: index.php");
    exit;
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Asignar Materia a Profesor</title>
    <link rel="stylesheet" href="../style.css"> 
</head>
<body>
<h2>Asignar Materia a Profesor</h2>
<form method="POST">
    Profesor:
    <select name="id_profesor" required>
        <option value="">Seleccione un profesor</option>
        <?php foreach ($profesores as $profesor): ?>
            <option value="<?= $profesor['id_profesor'] ?>">
                <?= $profesor['nombre'] ?>
            </option>
        <?php endforeach; ?>
    </select>

    Materia:
    <select name="id_materia" required>
        <option value="">Seleccione una materia</option>
        <?php foreach ($materias as $materia): ?>
            <option value="<?= $materia['id_materia'] ?>">
                <?= $materia['nombre'] ?>
            </option>
        <?php endforeach; ?>
    </select>

    <button type="submit">Asignar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
