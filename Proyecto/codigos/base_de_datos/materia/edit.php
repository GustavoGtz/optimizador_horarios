<?php
require '../config/db.php';

$id = $_GET['id'];

$tipos = $pdo->query("SELECT * FROM Tipo_Clase")->fetchAll();
$programas = $pdo->query("SELECT * FROM Programa_Educativo")->fetchAll();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $clave = $_POST['clave'];
    $nombre = $_POST['nombre'];
    $creditos = $_POST['creditos'];
    $semestre = $_POST['semestre'];
    $horas = $_POST['horas'];
    $id_tipo = $_POST['id_tipo_clase'];
    $id_programa = $_POST['id_programa_educativo'];

    $stmt = $pdo->prepare("UPDATE Materia SET clave = :clave, nombre = :nombre, creditos = :creditos, semestre = :semestre,
                           horas_por_semana = :horas, id_tipo_clase = :id_tipo, id_programa_educativo = :id_programa
                           WHERE id_materia = :id");
    $stmt->execute([
        'clave' => $clave,
        'nombre' => $nombre,
        'creditos' => $creditos,
        'semestre' => $semestre,
        'horas' => $horas,
        'id_tipo' => $id_tipo,
        'id_programa' => $id_programa,
        'id' => $id
    ]);

    header("Location: index.php");
    exit;
} else {
    $stmt = $pdo->prepare("SELECT * FROM Materia WHERE id_materia = :id");
    $stmt->execute(['id' => $id]);
    $materia = $stmt->fetch(PDO::FETCH_ASSOC);
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Editar Materia</title>
</head>
<body>
<h2>Editar Materia</h2>
<form method="POST">
    Clave: <input type="text" name="clave" value="<?= $materia['clave'] ?>" required><br>
    Nombre: <input type="text" name="nombre" value="<?= $materia['nombre'] ?>" required><br>
    Créditos: <input type="number" name="creditos" value="<?= $materia['creditos'] ?>" required><br>
    Semestre: <input type="number" name="semestre" value="<?= $materia['semestre'] ?>" required><br>
    Horas/semana: <input type="number" name="horas" value="<?= $materia['horas_por_semana'] ?>" required><br>
    Tipo de Clase:
    <select name="id_tipo_clase" required>
        <?php foreach ($tipos as $tipo): ?>
            <option value="<?= $tipo['id_tipo_clase'] ?>" <?= $tipo['id_tipo_clase'] == $materia['id_tipo_clase'] ? 'selected' : '' ?>>
                <?= $tipo['nombre'] ?>
            </option>
        <?php endforeach; ?>
    </select><br>
    Programa Educativo:
    <select name="id_programa_educativo" required>
        <?php foreach ($programas as $programa): ?>
            <option value="<?= $programa['id_programa_educativo'] ?>" <?= $programa['id_programa_educativo'] == $materia['id_programa_educativo'] ? 'selected' : '' ?>>
                <?= $programa['nombre'] ?>
            </option>
        <?php endforeach; ?>
    </select><br>
    <button type="submit">Actualizar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
