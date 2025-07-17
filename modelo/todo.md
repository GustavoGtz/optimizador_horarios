# TODO del modelo

## Version 1

- [x] Modelo base
- [ ] Escribir las matematicas arriba del codigo
- [x] Arreglar profesores imaginarios (usa variable Y_Gorro)
    - [X] Agregar conjunto de profes imaginarios
    - [X] Agregar funcion a minimizar en la funcion objetivo, que sea la suma
          de las asignaciones de prof. imaginarios.
    - [X] Agregar Conjunto de Profesores_Totaltes (Profesores Reales y Imaginarios)
- [ ] Arreglar que los horarios no se hagan todos en un dia, y no sean sesiones muy larga
    - [x] Agregar la variable $\hat{y}$ (significa asignacion profe-materia)
    - [x] Agregar las restriccions de $\hat{y}$
    - [x] Agregar variable $s$
    - [ ] Agregar funciones $\psi_{min}(j)$ y $\psi_{max}(j)$
        - [x] Agregar en datos, la duracion de sesion min. y max. para cada materia (Se agrego por ahora como duracion de 1 hora para Sesion Minima y Maxima)
    - [ ] Agregar restricciones para $s$ y $\psi$
- [ ] Mejorar Funcion objetivo
- [ ] Checar si la restriccion "materia_tiene_profesor_rule" es necesaria
- [ ] Evitar sobreescribir variables

## Version 2

- [ ] Agregar salones
- [ ] Agregar limite de 20 horas por profesor
- [ ] Agregar contratos para cada profesor

## Version 3

- [ ] Agregar bloques