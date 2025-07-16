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

- $
y_{i, j} =
\begin{cases}
    1 & \text{si el profesor } i
    \text{ puede ense\~{n}ar la materia } j \\
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

$$
\sum_{i \in P} \sum_{k \in A} \sum_{t \in BH} x^{i, j}_{k, t} \ge \text{HorasSemanaMateria}(j) \quad \forall\ j \in M
$$

- Asignar un aula a una materia solo si el tipo de aula es compatible con el tipo de materia

$$
x^{i, j}_{k, t} \leq \text{Compatibilidad}(k,j) \quad \forall i \in P, \forall j \in M, \forall k \in A, \forall t \in BH
$$

