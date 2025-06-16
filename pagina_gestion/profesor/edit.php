<?php
require '../config/db.php';

$id = $_GET['id'];

// Obtener contratos para el select
$contratos = $pdo->query("SELECT * FROM Contrato")->fetchAll();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = $_POST['nombre'];
    $id_contrato = $_POST['id_contrato'];

    $stmt = $pdo->prepare("UPDATE Profesor SET nombre = :nombre, id_contrato = :id_contrato WHERE id_profesor = :id");
    $stmt->execute([
        'nombre' => $nombre,
        'id_contrato' => $id_contrato,
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
    ID Profesor: <?= htmlspecialchars($profesor['id_profesor']) ?><br>
    Nombre: <input type="text" name="nombre" value="<?= htmlspecialchars($profesor['nombre']) ?>" required><br>
    Contrato:
    <select name="id_contrato" required>
        <?php foreach ($contratos as $contrato): ?>
            <option value="<?= $contrato['id_contrato'] ?>" <?= $contrato['id_contrato'] == $profesor['id_contrato'] ? 'selected' : '' ?>>
                <?= $contrato['nombre'] ?>
            </option>
        <?php endforeach; ?>
    </select><br>
    <button type="submit">Actualizar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
