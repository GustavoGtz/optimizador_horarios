CREATE TABLE Unidad_Academica (
    id_unidad_academica SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    abreviatura VARCHAR(5)
);

CREATE TABLE Tipo_Clase (
    id_tipo_clase SERIAL PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE Contrato (
    id_contrato SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    horas_minimas INT NOT NULL,
    horas_maximas INT NOT NULL
);

CREATE TABLE Programa_Educativo (
    id_programa_educativo SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    abreviatura VARCHAR(5),
    id_unidad_academica INT NOT NULL,
    FOREIGN KEY (id_unidad_academica) REFERENCES Unidad_Academica(id_unidad_academica)
);

CREATE TABLE Materia (
    id_materia SERIAL PRIMARY KEY,
    clave VARCHAR(20),
    nombre VARCHAR(100),
    creditos INT NOT NULL,
    semestre INT NOT NULL,
    horas_por_semana INT NOT NULL,
    id_tipo_clase INT NOT NULL,
    id_programa_educativo INT NOT NULL,
    FOREIGN KEY (id_tipo_clase) REFERENCES Tipo_Clase(id_tipo_clase),
    FOREIGN KEY (id_programa_educativo) REFERENCES Programa_Educativo(id_programa_educativo)
);

CREATE TABLE Profesor (
    id_profesor INT NOT NULL PRIMARY KEY,
    nombre VARCHAR(100),
    id_contrato INT NOT NULL,
    tiene_discapacidad BOOLEAN DEFAULT FALSE,   
    FOREIGN KEY (id_contrato) REFERENCES Contrato(id_contrato)
);

CREATE TABLE Profesor_Materia (
    id_profesor INT NOT NULL,
    id_materia INT NOT NULL,
    veces_impartida INT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_profesor, id_materia),
    FOREIGN KEY (id_profesor) REFERENCES Profesor(id_profesor),
    FOREIGN KEY (id_materia) REFERENCES Materia(id_materia)
);

CREATE TABLE Edificio (
    id_edificio SERIAL PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE Aula (
    id_aula INT NOT NULL,
    id_edificio INT NOT NULL,
    id_tipo_clase INT NOT NULL,
    cupo INT NOT NULL,
    PRIMARY KEY (id_aula, id_edificio),
    FOREIGN KEY (id_edificio) REFERENCES Edificio(id_edificio),
    FOREIGN KEY (id_tipo_clase) REFERENCES Tipo_Clase(id_tipo_clase)
);
