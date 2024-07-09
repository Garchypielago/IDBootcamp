-- Crear base de datos
DROP DATABASE IF EXISTS colegio;
CREATE DATABASE IF NOT EXISTS colegio;
USE colegio;

-- Crear tabla Profesores
CREATE TABLE Profesores (
    Profesor_ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Cumpleaños DATE
);

-- Crear tabla Alumnos
CREATE TABLE Alumnos (
    Alumno_ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Cumpleaños DATE
);

-- Crear tabla Asignatura
CREATE TABLE Asignatura (
    Asignatura_ID INT AUTO_INCREMENT PRIMARY KEY,
    Asignatura VARCHAR(100) NOT NULL,
    Profesor_ID INT NOT NULL,
    Año INT NOT NULL,
    constraint FK_PROFE_ASIG
    FOREIGN KEY (Profesor_ID) REFERENCES Profesores(Profesor_ID)
);

-- Crear tabla Notas
CREATE TABLE Notas (
    Asignatura_ID INT,
    Alumno_ID INT,
    Nota FLOAT,
    PRIMARY KEY (Asignatura_ID, Alumno_ID),
    constraint FK_ASIG_NOTA
    FOREIGN KEY (Asignatura_ID) REFERENCES Asignatura(Asignatura_ID),
    constraint FK_ALUM_NOTA
    FOREIGN KEY (Alumno_ID) REFERENCES Alumnos(Alumno_ID)
);


-- Insertar datos en Profesores
INSERT INTO Profesores (Nombre, Apellido, Cumpleaños) VALUES
('Ana', 'García', '1970-04-23'),
('Luis', 'Martínez', '1980-06-15'),
('Pedro', 'Sánchez', '1975-09-10');

-- Insertar datos en Alumnos
INSERT INTO Alumnos (Nombre, Apellido, Cumpleaños) VALUES
('Juanito', 'Pérez', '2000-01-10'),
('María', 'López', '1999-05-20'),
('Carlos', 'Gómez', '2001-08-30');

-- Insertar datos en Asignatura
INSERT INTO Asignatura (Asignatura, Profesor_ID, Año) VALUES
('Matemáticas', 1, 2022),
('Física', 2, 2022),
('Química', 3, 2022),
('Matemáticas', 1, 2023); -- Juanito toma Matemáticas en 2023 también

-- Insertar datos en Notas
INSERT INTO Notas (Asignatura_ID, Alumno_ID, Nota) VALUES
(1, 1, 7.5),  -- Juanito en Matemáticas 2022
(2, 2, 8.0),  -- María en Física
(3, 3, 6.5),  -- Carlos en Química
(3, 1, 9.0),  -- Juanito en Química
(4, 1, 7.8),  -- Juanito en Matemáticas 2023 (segunda vez)
(1, 2, 8.5),  -- María en Matemáticas 2022
(2, 1, 7.0),  -- Juanito en Física
(4, 2, 8.2);  -- María en Matemáticas 2023


-- Nota media de cada asignatura:
SELECT Asignatura, AVG(Nota) AS Nota_Media
FROM Asignatura a
JOIN Notas n ON a.Asignatura_ID = n.Asignatura_ID
GROUP BY Asignatura;

-- Nota media asociada a cada profesor:
SELECT p.Nombre, p.Apellido, AVG(n.Nota) AS Nota_Media
FROM Profesores p
JOIN Asignatura a ON p.Profesor_ID = a.Profesor_ID
JOIN Notas n ON a.Asignatura_ID = n.Asignatura_ID
GROUP BY p.Nombre, p.Apellido;

-- Notas del alumno con mayor nota media:
SELECT a.Nombre, a.Apellido, n.Nota
FROM Alumnos a
JOIN Notas n ON a.Alumno_ID = n.Alumno_ID
WHERE a.Alumno_ID = (
    SELECT Alumno_ID
    FROM Notas
    GROUP BY Alumno_ID
    ORDER BY AVG(Nota) DESC
    LIMIT 1
);


-- Asignatura más difícil (nota media más baja):
SELECT Asignatura, AVG(Nota) Nota_Media
FROM Asignatura a
JOIN Notas n ON a.Asignatura_ID = n.Asignatura_ID
GROUP BY Asignatura
ORDER BY Nota_Media ASC
LIMIT 1;





