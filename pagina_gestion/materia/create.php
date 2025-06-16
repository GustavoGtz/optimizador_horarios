<?php
require '../config/db.php';

// Obtener datos para selects
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

    $stmt = $pdo->prepare("INSERT INTO Materia (clave, nombre, creditos, semestre, horas_por_semana, id_tipo_clase, id_programa_educativo) 
                           VALUES (:clave, :nombre, :creditos, :semestre, :horas, :id_tipo, :id_programa)");
    $stmt->execute([
        'clave' => $clave,
        'nombre' => $nombre,
        'creditos' => $creditos,
        'semestre' => $semestre,
        'horas' => $horas,
        'id_tipo' => $id_tipo,
        'id_programa' => $id_programa
    ]);

    header("Location: index.php");
    exit;
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Nueva Materia</title>
</head>
<body>
<h2>Agregar Materia</h2>
<form method="POST">
    Clave: <input type="text" name="clave" required><br>
    Nombre: <input type="text" name="nombre" required><br>
    Créditos: <input type="number" name="creditos" required><br>
    Semestre: <input type="number" name="semestre" required><br>
    Horas/semana: <input type="number" name="horas" required><br>
    Tipo de Clase:
    <select name="id_tipo_clase" required>
        <?php foreach ($tipos as $tipo): ?>
            <option value="<?= $tipo['id_tipo_clase'] ?>"><?= $tipo['nombre'] ?></option>
        <?php endforeach; ?>
    </select><br>
    Programa Educativo:
    <select name="id_programa_educativo" required>
        <?php foreach ($programas as $programa): ?>
            <option value="<?= $programa['id_programa_educativo'] ?>"><?= $programa['nombre'] ?></option>
        <?php endforeach; ?>
    </select><br>
    <button type="submit">Guardar</button>
</form>
<a href="index.php">Cancelar</a>
</body>
</html>
