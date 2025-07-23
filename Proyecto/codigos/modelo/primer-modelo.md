# Conjuntos y funciones

- $S$: Conjunto de salones
    - $S_L$: Conjunto de salones de laboratorio
    - $S_A$: Conjunto de salones de aula
    - $S_T$: Conjunto de salones de taller
    - $S_C$: Conjunto de salones de computo
    - $S = S_L\ \cup\ S_A\ \cup\ S_T\ \cup\ S_C$
- $M$: Conjunto de maestros
    - $M_R$: Conjunto de maestros reales
    - $M_I$: Conjunto de maestros imaginarios
- $C$: Conjunto de cursos
- $D$: Conjunto de dias
    - $D = \{ Lunes, Martes,\ \dots, Viernes \}$
- $H_d$: Conjunto de horas de un dia $d \in D$
    - $H_d = \{ 1, 2,\ \dots, 10 \}$
- $TipoCurso\, (c)$: Tipo de curso para el curso $c \in C$
    - $TipoCurso: C \rightarrow \{\text{Taller}, \text{Laboratorio de Ciencias}, \text{Computo}, \text{Aulas}\}$
- $TipoSalon\, (s)$: Tipo de salon para el salon $s \in S$
    - $TipoSalon: S \rightarrow \{\text{Taller}, \text{Laboratorio de Ciencias}, \text{Computo}, \text{Aulas}\}$
- $Posibles\, (m)$: Posibles materias que puede dar un maestro $m \in M$
    - $Posibles: M \rightarrow C$

# Variables

$$ x_{m, h_d} \begin{cases}
1 & \text{si el profesor}\ m\ \text{esta disponible en la hora}\ h\ \text{del dia}\ d. \\
0 & \text{si no}
\end{cases}$$

# Restricciones Duras

## Restricciones Duras
- Todas las materias tienen que estar cubiertas
- Un maestro no puede dar dos clases al mismo tiempo
- Una clase no puede ser impartida en dos salones al mismo tiempo

## Restricciones Blandas

- Minimizar el numero de maestros imaginarios
    - Funcion que nos diga si el maestro es imaginario