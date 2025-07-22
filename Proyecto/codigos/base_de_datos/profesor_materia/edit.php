<?php
require '../config/db.php';

$id_profesor_original = $_GET['id_profesor'];
$id_materia_original = $_GET['id_materia'];

$profesores = $pdo->query("SELECT id_profesor, nombre FROM Profesor")->fetchAll();
$materias = $pdo->query("SELECT id_materia, nombre FROM Materia")->fetchAll();

// Obtener valores actuales
$stmt = $pdo->prepare("
    SELECT veces_impartida 
    FROM Profesor_Materia 
    WHERE id_profesor = ? AND id_materia = ?
");
$stmt->execute([$id_profesor_original, $id_materia_original]);
$relacion = $stmt->fetch();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nuevo_profesor = $_POST['id_profesor'];
    $nueva_materia = $_POST['id_materia'];
    $veces_impartida = $_POST['veces_impartida'];

    // Actualizar la tabla
    $stmt = $pdo->prepare("
        UPDATE Profesor_Materia
        SET id_profesor = ?, id_materia = ?, veces_impartida = ?
        WHERE id_profesor = ? AND id_materia = ?
    ");
    $stmt->execute([$nuevo_profesor, $nueva_materia, $veces_impartida, $id_profesor_original, $id_materia_original]);

    header("Location: index.php");
    exit;
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Editar Asignación</title>
</head>
<body>
    <h2>Editar Asignación Profesor - Materia</h2>

    <form method="POST">
        <label>Profesor:</label>
        <select name="id_profesor" required>
            <?php foreach ($profesores as $prof): ?>
                <option value="<?= $prof['id_profesor'] ?>" <?= $prof['id_profesor'] == $id_profesor_original ? 'selected' : '' ?>>
                    <?= htmlspecialchars($prof['nombre']) ?>
                </option>
            <?php endforeach; ?>
        </select><br><br>

        <label>Materia:</label>
        <select name="id_materia" required>
            <?php foreach ($materias as $mat): ?>
                <option value="<?= $mat['id_materia'] ?>" <?= $mat['id_materia'] == $id_materia_original ? 'selected' : '' ?>>
                    <?= htmlspecialchars($mat['nombre']) ?>
                </option>
            <?php endforeach; ?>
        </select><br><br>

        <label>Veces Impartida:</label>
        <input type="number" name="veces_impartida" value="<?= htmlspecialchars($relacion['veces_impartida']) ?>" min="1" required><br><br>

        <button type="submit">Guardar Cambios</button>
    </form>

    <br>
    <a href="index.php">Cancelar</a>
</body>
</html>
