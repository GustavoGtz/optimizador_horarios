# Conjuntos

- $P: \text{Profesores}$
- $M: \text{Materias}$
- $A: \text{Aulas}$
    - $A = A_{salon}\ \cup\ A_{edificio}$
- $BH: \text{Bloques Horarios}$
    - $D: \text{Dias}, D = \{1, 2,\ \dots, 5\}$
    - $H: \text{Horarios}, H = \{1, 2,\ \dots, 10\}$
    - $BH = D \times H = \{(d, h)\ |\ d \in D, h \in H\}$

# Parametros

- $\text{HorasSemanaMateria}(m) = n$, donde $n$ es el numero de horas que la materia $m$ tiene por semana
- $\text{TipoClase}(m) = t$, donde $t \in \{1,2,3,4\}$ es el tipo de clase de la materia $m$
- $\text{TipoAula}(a) = t$, donde $t \in \{1,2,3,4\}$ es el tipo de aula de la aula $a$
- $ \text{Compatibles}(a, m) \begin{cases} 1 & \text{si el aula}\ a\ \text{es compatible con la materia}\ m\\ 0 & \text{si no} \end{cases}$

- $ \text{Relacion}(p, m) \begin{cases} 1 & \text{si el profesor}\ p\ \text{puede dar la materia}\ m\\ 0 & \text{si no} \end{cases}$

# Variables

- $
x^{i, j}_{k, t} =
\begin{cases}
    1 & \text{si el profesor } i
    \text{ tiene asignada la materia } j
    \text{ en el aula } k
    \text{ en el horario } t \\
    0 & \text{si no}
\end{cases}
$

PROBABLEMENTE REPETIDA/INNECESARIA
- $
y_{i, j} =
\begin{cases}
    1 & \text{si el profesor } i
    \text{ puede enseñar la materia } j \\
    0 & \text{si no}
\end{cases}
$

- $
z_{k, j} =
\begin{cases}
    1 & \text{si el aula } k
    \text{ esta asignada a la materia } j \\
    0 & \text{si no}
\end{cases}
$

# Restricciones

- Horas Semana Materia (Asignar exactamente las horas semanales requeridas por cada materia):

$$
\sum_{i \in P} \sum_{k \in A} \sum_{t \in BH} x^{i, j}_{k, t} = \text{HorasSemanaMateria}(j) \quad \forall\ j \in M
$$

- No Solapamiento Profesor (No asignar un profesor a más de una materia en un bloque horario):
$$
\sum_{j \in M} \sum_{k \in A} x^{i, j}_{k, t} \le 1 \quad \forall\ i \in P,\ t \in BH
$$

- No Solapamiento Aula (No asignar un aula a más de una materia en un bloque horario):
$$
\sum_{i \in P} \sum_{j \in M} x^{i, j}_{k, t} \le 1 \quad \forall\ k \in A,\ t \in BH
$$

- Profesor Puede Enseñar (Asignar un profesor a una materia solo si el profesor puede enseñar esa materia):
$$
x^{i, j}_{k, t} \le \text{Relacion}(i,j) \quad \forall\ i \in P,\ j \in M,\ k \in A,\ t \in BH
$$

- Aula Compatible Materia (Asignar un aula a una materia solo si el tipo de aula es compatible con el tipo de materia):

$$
x^{i, j}_{k, t} \le \text{Compatibles}(j,k) \quad \forall\ i \in P,\ j \in M,\ k \in A,\ t \in BH
$$

# Restricciones variables generales con variables combinadas

REPETIDA
$$
x^{i, j}_{k, t} \le y_{i,j} \quad \forall\ i \in P,\ j \in M,\ k \in A,\ t \in BH
$$

$$
x^{i, j}_{k, t} \le z_{k,j} \quad \forall\ i \in P,\ j \in M,\ k \in A,\ t \in BH
$$

# Restricciones adicionales para asegurar que cada materia tenga asignado al menos un profesor y un aula

- Materia tiene profesor:
$$
\sum_{i \in P} y_{i,j} \ge 1 \quad \forall j \in M
$$

- Materia tiene aula:
ORIGINAL
$$
\sum_{j \in M} z_{j,k} \ge 1 \quad \forall k \in A
$$

ARREGLADA
$$
\sum_{k \in A} z_{j,k} \ge 1 \quad \forall j \in M
$$

# Objetivos

- Total Profesores
$$
\sum_{i \in P} \sum_{j \in M} y_{i, j}
$$

- Total Aulas
$$
\sum_{j \in M} \sum_{k \in A} z_{j, k}
$$

- Total Asignaciones
$$
\sum_{i \in P} \sum_{j \in M} \sum_{k \in A} \sum_{t \in BH} x^{i, j}_{k, t}
$$

- Funcion Objetivo
$$
\text{max} \quad
w_1\sum_{i \in P} \sum_{j \in M} y_{i, j} +
w_2 \sum_{j \in M} \sum_{k \in A} z_{j, k} +
w_3 \sum_{i \in P} \sum_{j \in M} \sum_{k \in A} \sum_{t \in BH} x^{i, j}_{k, t}
$$