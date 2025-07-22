<?php
require '../config/db.php';

// Obtener contratos para el select
$contratos = $pdo->query("SELECT * FROM Contrato")->fetchAll();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $id_profesor = $_POST['id_profesor'];
    $nombre = $_POST['nombre'];
    $id_contrato = $_POST['id_contrato'];
    $tiene_discapacidad = isset($_POST['tiene_discapacidad']) ? 1 : 0;

    $stmt = $pdo->prepare("
        INSERT INTO Profesor (id_profesor, nombre, id_contrato, tiene_discapacidad) 
        VALUES (:id_profesor, :nombre, :id_contrato, :tiene_discapacidad)
    ");
    $stmt->execute([
        'id_profesor' => $id_profesor,
        'nombre' => $nombre,
        'id_contrato' => $id_contrato,
        'tiene_discapacidad' => $tiene_discapacidad
    ]);

    header("Location: index.php");
    exit;
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Nuevo Profesor</title>
</head>
<body>
<h2>Agregar Profesor</h2>
<form method="POST">
    ID Profesor: <input type="number" name="id_profesor" required><br><br>

    Nombre: <input type="text" name="nombre" required><br><br>

    Contrato:
    <select name="id_contrato" required>
        <?php foreach ($contratos as $contrato): ?>
            <option value="<?= $contrato['id_contrato'] ?>"><?= htmlspecialchars($contrato['nombre']) ?></option>
        <?php endforeach; ?>
    </select><br><br>

    ¿Tiene Discapacidad?
    <input type="checkbox" name="tiene_discapacidad" value="1"><br><br>

    <button type="submit">Guardar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
