<?php
require '../config/db.php';

$id = $_GET['id'];

// Obtener contratos para el select
$contratos = $pdo->query("SELECT * FROM Contrato")->fetchAll();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = $_POST['nombre'];
    $id_contrato = $_POST['id_contrato'];
    $tiene_discapacidad = isset($_POST['tiene_discapacidad']) ? 1 : 0;

    $stmt = $pdo->prepare("
        UPDATE Profesor 
        SET nombre = :nombre, id_contrato = :id_contrato, tiene_discapacidad = :tiene_discapacidad 
        WHERE id_profesor = :id
    ");
    $stmt->execute([
        'nombre' => $nombre,
        'id_contrato' => $id_contrato,
        'tiene_discapacidad' => $tiene_discapacidad,
        'id' => $id
    ]);

    header("Location: index.php");
    exit;
} else {
    $stmt = $pdo->prepare("SELECT * FROM Profesor WHERE id_profesor = :id");
    $stmt->execute(['id' => $id]);
    $profesor = $stmt->fetch(PDO::FETCH_ASSOC);
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Editar Profesor</title>
</head>
<body>
<h2>Editar Profesor</h2>
<form method="POST">
    ID Profesor: <?= htmlspecialchars($profesor['id_profesor']) ?><br><br>
    
    Nombre:
    <input type="text" name="nombre" value="<?= htmlspecialchars($profesor['nombre']) ?>" required><br><br>
    
    Contrato:
    <select name="id_contrato" required>
        <?php foreach ($contratos as $contrato): ?>
            <option value="<?= $contrato['id_contrato'] ?>" <?= $contrato['id_contrato'] == $profesor['id_contrato'] ? 'selected' : '' ?>>
                <?= htmlspecialchars($contrato['nombre']) ?>
            </option>
        <?php endforeach; ?>
    </select><br><br>

    ¿Tiene Discapacidad?
    <input type="checkbox" name="tiene_discapacidad" value="1" <?= $profesor['tiene_discapacidad'] ? 'checked' : '' ?>><br><br>

    <button type="submit">Actualizar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
