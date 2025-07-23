# Conjuntos

- $S$: Conjunto de salones
    - $S_L$: Conjunto de salones de laboratorio
    - $S_T$: Conjunto de salones de teoria
- $M$: Conjunto de maestros
    - $M_{TC}$: Conjunto de maestros de tiempo completo
    - $M_{MT}$: Conjunto de maestros de medio tiempo
    - $M_{HS}$: Conjunto de maestros de horas sueltas
    - $M_{PA}$: Conjunto de maestros por asignar
    - $M = M_{TC}\ \cup\ M_{MT}\ \cup\ M_{HS}\ \cup\ M_{PA}$
- $C$: Conjunto de cursos
- $D$: Conjunto de dias
    - $D = \{ Lunes, Martes,\ \dots, Viernes \}$
- $H_d$: Conjunto de horas de un dia $d \in D$
    - $H_d = \{ 1, 2,\ \dots, 10 \}$
- $Tipo\, (c)$: Tipo de curso para el curso $c \in C$
    - $Tipo: C \rightarrow \{\text{Taller}, \text{Laboratorio de Ciencias}, \text{Computo}, \text{Aulas}\}$
- $Posibles\, (m)$: Posibles materias que puede dar un maestro
    - $Posibles: M \rightarrow C$