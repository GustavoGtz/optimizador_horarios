## Variables

- Maestros
- Clases
- Salones
	-Tipo de Salon
- Tiempo
- Bloques

> **Asignamos laboratorios?**

## Restricciones duras
- Un maestro no puede dar dos o mas clases al mismo tiempo
- Una clase no puede ser impartida en dos o mas salones al mismo tiempo
- Un maestro solo puede tener asignado una clase y un salon para cualquier tiempo
- Una clase solo puede ser impartida por un maestro
	*Si es laboratorio puede ser impartido por otro profesor(depende como tomemos los laboratorios, actualmente
	están separados pero aja, checar esa shit
- No puede haber recursos asignados antes de las 8 am o despues de las 6 pm
- Dos clases del mismo bloque no pueden estar asignadas a la misma hora
- Una clase de laboratorio no puede estar asignada en un salon que no sea de laboratorio y viceversa
	*Tambien la misma madre cuando son talleres/Laboratorios/Computo/Aula
- Un maestros que no puede subir escaleras, no puede dar clases en salones que esten en un segundo o mayor piso
	*Pues como no sabemos cuales profes son lisiados tendríamos que hacer que el don que hace los horarios
	segregue a los profes que no pueden caminar
- Las horas semanales que trabaja un maestro tienen que cumplir el intervalo establecido segun su contrato
    - Maestro de Asignatura: 1-18 horas
    - Maestro de Medio Tiempo: 9-15 horas
    - Maestro de Tiempo Completo: 12-20 horas

## Restricciones blandas
- Maximizar el numero de clases impartidas en la mañana
- Maximizar el espacio utilizado
- Minimizar el numero de clases sin maestro asignado
- Minimizar el numero de salones asignador para una clase (puede ser dura)
- El salon asignado para una clase debera corresponder al tipo de clase (a excepcion de las clases de laboratorio)
	*si tiene laboratorio debe de tener 2 salones Uno normal y el de laboratorio(Como tenemos separados el lab de las 	normales en el excel pues aja, seria revisarlo después)
- Los maestros que mas veces han impartido una clase, tienen prioridad para ser asignados esa clase
- Los maestros tienen horarios preferidos
- Los horarios de las clases deberan estar asignados, de tal manera que se minimicen los tiempos entre clases, para maestros y para bloques
- Los maestros pueden pedir salones especificos para ciertas clases


## PDF
![[Restricciones_202506251248_18126_125208.pdf]]


---
[Intro to Mixed-Integer Linear Programming (MILP) - Marvik](https://blog.marvik.ai/2025/01/10/linear-programming/)
## Parametros

### Materia

Cada materia tiene un salon asignado, un maestro, una clave unica, un horario(Hora y dia), una unidad academica, un semestre, creditos, un bloque asignado y un tipo de clase 

### Maestro

Cada maestro tiene una id unica, nombre, una id del contrato(Completo, medio tiempo y horas sueltas), y si tiene una discapacidad.
Aparte tiene una relacion con las materias, cada profesor tiene al menos una materia asignada y las veces que la a impartido.

### Salon

Cada salon tiene un tipo asignado(laboratorio/taller/computacion/aula), una materia asignada en un horario especifico en un dia especifico, un maestro asignado, y un cupo maximo(algunos son salones grandes y pueden ser partidos(?))

## Variables

### Materia

- Tipo
- Maestro
- id
- salon
- horario(dia/hora)

### Maestro

- id
- Materias que imparte
- si es lisiado
- contrato
- Horas libres
- horas preferentes

### Salon

- ID
- Tipo de salon
- Materias asignadas segun el horario
- Cupo

## Restricciones

#### Materia

- Un solo profesor asignado por horario especifico
- un Salon especifico
- un tipo especifico

### Maestro

- Una sola materia asignada por horario especifico
- un salon especifico
- Contrato especifico(Horas totales que puede impartir)
- si el cabron puede caminar
- preferencia a materias por las veces que la impartio
- un horario que tienen preferido.

### Salon

- Tipo del salon
- posibles materias a impartir en el salon
- el cupo maximo(Si sobrepasa X cantidad de cupo puede ser dividido en 2 salones(?)
- Materia que se imparte en tiempo especifico
- si la materia a impartir es un laboratorio

## Funcion objetivo

El objetivo es minimizar el uso excesivo de salones mientras se maximiza el uso de los maestros y la cantidad de aulas.

## Sets:
- $\mathcal{A}$: Los maestros disponibles para utilizar en el problema en cuestion. Maestro individual es Subindex_a $(a \in \mathcal{A})$
- $\mathcal{C}$: Las aulas disponibles para utilizar en el problema.  Cada aula es un Subindex_c $(c \in \mathcal{C})$
- $\mathcal{B}$: Las materias que se tienen que optimizar. subindex_b $(b \in \mathcal{B})$

## Definicion Parametros

### Materia

- $\mathrm{b\_maestro}_{ab}$: El Maestro A asignado a la materia B
- $\mathrm{b\_Salon}_{cb}$ : La Aula C asignada a la materia B
- $\mathrm{b\_tipo}_{b}$ : El tipo de materia que es la materia B
- $\mathrm{b\_Cupo}_{cb}$: El posible cupo de la materia B contando el cupo maximo de el salon asignado.
	
### Maestro:

- $A\_Materia_{ab}$ : La materia B asignada al profesor A
- $A\_Salon_{cab}$: El salon C asignado al profesor A para impartir la materia B
- $A\_Contrato_{a}$: El tipo de contrato del profesor A
- $A\_Impartido_{ab}$: La cantidad de veces que el profesor A a impartido la materia B
- $A\_Lisiado_{a}$: Booleano para saber si el profesor A tiene alguna discapacida
- $A\_Horario\_Preferido_{a}$: Horario preferido del profesor A, Si dos profesores que imparten la misma materia tienen el mismo horario preferido posible dos opciones, dependiendo del cupo maximo que se pueda llegar a inscribir a la materia abrir 2 grupos, si no utilizar la antiguead o la cantidad de veces impartidas para dar preferencia.

### Salon:

- $C\_Tipo_{c}$: Tipo de aula del salon  C
- $C\_Posibles\_Materias_{cb}$: Las posibles materias B que se pueden impartir en el salon C
- $C\_Cupo_Maximo$: El cupo maximo posible del Salon C
- $C\_Materias_Impartidas_{cb}$: Las materias b que se estan impartiendo en el salon C
- $C\_Laboratorio_{cb}$: Booleano para saber si la materia B va a ocupar laboratorio.

## Variables de decision:

- $Es\_Profe\_Materia_{a,b}$: Booleano para ver si el profesor a puede dar la materia b
- $Si\_Materia\_Salon_{c,b}$: Booleano para ver si la materia B se puede dar en el salon C
- $Materia\_Horario_{b,h}$: Booleano para saber si la materia B es impartida en el horario C

## Posibles Auxiliares:
- $Maestro\_Horario_{a,h}$: Booleano para saber si el profesor A esta ocupado durante el horario H
- $Salon\_Horario_{c,h}$: Booleano para saber si el salon C esta ocupado durante el horario H

## Restricciones

### Materia:
- Una sola asignación de profesor por materia
	- $\sum_{a \in A} Es\_Profe\_Materia_{a,b} = 1 \quad \forall b \in B$
- Una sola asignación de salón por materia
	- $\sum_{c \in C} Si\_Materia\_Salon_{c,b} = 1 \quad \forall b \in B$
- Una sola asignación de horario por materia
	- $\sum_{h \in H} Materia\_Horario_{b,h} = 1 \quad \forall b \in B$
- Compatibilidad entre tipo de materia y tipo de salón
	- $Si\_Materia\_Salon_{c,b} \leq C\_Posibles\_Materias_{c,b} \quad \forall c \in C,\; \forall b \in B$
- Cupo suficiente para impartir la materia en el salón
	- $b\_Cupo_{cb} \leq C\_Cupo\_Maximo_c \quad \text{si } Si\_Materia\_Salon_{c,b} = 1$

### Maestro

- Un maestro no puede impartir más de una materia por horario
	- $\sum_{b \in B} Es\_Profe\_Materia_{a,b} \cdot Materia\_Horario_{b,h} \leq 1 \quad \forall a \in A,\; \forall h \in H$
- Horas totales asignadas a un maestro no superan su contrato
	- $\sum_{b \in B} \sum_{h \in H} Es\_Profe\_Materia_{a,b} \cdot Materia\_Horario_{b,h} \leq HorasPermitidas(A\_Contrato_{a}) \quad \forall a \in A$
- Profesores con discapacidad deben tener horarios preferentes (si es restricción dura)
	- $A\_Lisiado_{a} = 1 \Rightarrow Materia\_Horario_{b,h} = 0 \quad \forall h \notin A\_Horario\_Preferido_{a},\; \forall b \in B\; \text{tal que } Es\_Profe\_Materia_{a,b} = 1$

### Salon

- Un salón no puede tener más de una materia por horario
	- $\sum_{b \in B} Si\_Materia\_Salon_{c,b} \cdot Materia\_Horario_{b,h} \leq 1 \quad \forall c \in C,\; \forall h \in H$
- Tipo de materia compatible con tipo de salón
	- $Si\_Materia\_Salon_{c,b} = 1 \Rightarrow b\_tipo_{b} = C\_Tipo_{c}$
- Solo asignar laboratorio si la materia lo requiere
	- $C\_Laboratorio_{c,b} = 1 \quad \text{si } b\_tipo_{b} = \text{laboratorio}$

### Auxiliares

- Maestro ocupado en horario h si da alguna materia
	- $Maestro\_Horario_{a,h} = \sum_{b \in B} Es\_Profe\_Materia_{a,b} \cdot Materia\_Horario_{b,h} \quad \forall a \in A,\; \forall h \in H$
- Salón ocupado en horario h si se imparte alguna materia en él
	- $Salon\_Horario_{c,h} = \sum_{b \in B} Si\_Materia\_Salon_{c,b} \cdot Materia\_Horario_{b,h} \quad \forall c \in C,\; \forall h \in H$

## Funcion Objetivo

**Maximizar el uso eficiente de maestros**:

Queremos que los profesores asignados sean los que tienen experiencia y disponibilidad, y que se aprovechen lo más posible dentro de sus límites contractuales.

$\mathrm{max} \sum_{a \in \mathcal{A}} \sum_{b \in \mathcal{B}} A\_Impartido_{a,b} \cdot Es\_Profe\_Materia_{a,b}$

Esto da preferencia a maestros con más experiencia impartiendo una materia.

**Minimizar el uso innecesario de salones**:

Esto se puede modelar minimizando el número total de horarios en los que un salón es ocupado:

$\text{min} \sum_{c \in C} \sum_{h \in H} Salon\_Horario_{c,h}$ 

Esto reduce el número total de bloques de salón utilizados — es decir, **compacta** la asignación en menos salones o menos bloques.

 **Maximizar la asignación de materias**:

Aseguramos que se cubran tantas materias como sea posible	

$\text{max} \sum_{b \in B} \sum_{c \in C} \sum_{h \in H} Si\_Materia\_Salon_{c,b} \cdot Materia\_Horario_{b,h}$

Esto maximiza la cantidad de materias que efectivamente fueron asignadas a un aula y un horario.

## Posibles errores

- Cambiar lo de horarios ya que es la madre que intentamos predecir ( Cambiar el objetivo y los parametros)
- Ajustar el codigo para unirlo a la base de datos con el posgres(python se la rifa)
- ver como hacer para que el modelo regreso aja la info como en el excel
