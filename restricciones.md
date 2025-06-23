# Restricciones

## Variables

- Maestros
- Clases
- Salones
- Tiempo
- Bloques

> **Asignamos laboratorios?**

## Restricciones duras
- Un maestro no puede dar dos o mas clases al mismo tiempo
- Una clase no puede ser impartida en dos o mas salones al mismo tiempo
- Un maestro solo puede tener asignado una clase y un salon para cualquier tiempo
- Una clase solo puede ser impartida por un maestro
- No puede haber recursos asignados antes de las 8 am o despues de las 6 pm
- Dos clases del mismo bloque no pueden estar asignadas a la misma hora
- Una clase de laboratorio no puede estar asignada en un salon que no sea de laboratorio y viceversa
- Un maestros que no puede subir escaleras, no puede dar clases en salones que esten en un segundo o mayor piso
- Las horas semanales que trabaja un maestro tienen que cumplir el intervalo establecido segun su contrato
    - Maestro de Asignatura: 1-18 horas
    - Maestro de Medio Tiempo: 9-15 horas
    - Maestro de Tiempo Completo: 12-20 horas

## Restricciones blandas
- Maximizar el numero de clases impartidas en la manana
- Maximizar el espacio utilizado
- Minimizar el numero de clases sin maestro asignado
- Minimizar el numero de salones asignador para una clase (puede ser dura)
- El salon asignado para una clase debera corresponder al tipo de clase (a excepcion de las clases de laboratorio)
- Los maestros que mas veces han impartido una clase, tienen prioridad para ser asignados esa clase
- Los maestros tienen horarios preferidos
- Los horarios de las clases deberan estar asignados, de tal manera que se minimicen los tiempos entre clases, para maestros y para bloques
- Los maestros pueden pedir salones especificos para ciertas clases
