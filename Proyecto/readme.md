# Proyecto

Dentro de esta carpeta encontrarás dos componentes principales:

- `datos/`: Contiene toda la documentación utilizada durante el desarrollo del proyecto, incluyendo fuentes, referencias, estadísticas y material de apoyo.

- `codigos/`: Contiene el código fuente del proyecto, el cual implementa los algoritmos y herramientas desarrolladas para cumplir con los objetivos de esta investigación.

El desarrollo del proyecto se dividió en tres partes fundamentales, cada una con un objetivo específico para construir un sistema integral que atienda las necesidades actuales de la administración escolar.

## 1. Base de Datos

Como primer paso, se reorganizó la información obtenida (disponible en la carpeta `datos/`) para construir un sistema completo de base de datos. Este sistema no solo permitió facilitar el desarrollo del proyecto, sino que también representa una posible base para un futuro sistema de administración universitaria.

La base de datos incluye:

- Esquemas y definiciones.  
- Conjuntos de datos utilizados para la simulación.  
- Una página web funcional de consulta.  
- Documentación técnica detallada.

Todo este material se encuentra en `codigos/base_de_datos/`.

## 2. Visualización

Dentro de la carpeta `codigos/visualizacion/` se encuentran dos programas clave para la visualización de resultados:

- `agregador.py`: Utiliza la base de datos para generar una lista de materias y la carga académica del semestre. Esta información es esencial para alimentar el modelo de optimización.

- `cu2map.py`: Genera una visualización interactiva del campus universitario a partir de los resultados del modelo. Esta herramienta permite explorar el campus, consultar datos de ocupación y detectar posibles áreas de oportunidad.

## 3. Modelo

Con la información estructurada en la base de datos, se desarrolló un **modelo de satisfacción de restricciones**. Este modelo tiene como objetivo, a partir de la lista de materias generada por `agregador.py`, producir un horario lo más óptimo posible considerando diversas restricciones académicas y espaciales.

El modelo representa un sistema funcional con potencial de mejora, especialmente si se integra con más datos reales y se realizan múltiples iteraciones de refinamiento.

---

## Uso del Proyecto

El uso del sistema completo sigue una secuencia de pasos estructurada. A continuación se describe el flujo de trabajo recomendado:

1. **Configuración de la base de datos**  
   El primer paso es crear y configurar la base de datos. Toda la información necesaria (scripts, estructura, carga de datos y documentación) se encuentra en la carpeta `codigos/base_de_datos/`.

2. **Ajuste de credenciales**  
   Varios de los programas requieren conexión a la base de datos. Es necesario editar las credenciales en el código (usuario, contraseña, nombre de la base de datos, host, etc.) para que coincidan con la configuración creada en el paso anterior.

3. **Generación de la lista de materias**  
   Ejecutar `agregador.py`, el cual se encargará de generar la lista de materias y carga académica con base en los datos disponibles en la base de datos. Este archivo es esencial para alimentar el modelo de optimización.

4. **Ejecución del modelo de optimización**  
   Con la lista generada, se puede ejecutar el modelo de satisfacción de restricciones para obtener un horario optimizado.

5. **Visualización de resultados**  
   Finalmente, los resultados generados por el modelo pueden visualizarse de manera interactiva mediante `cu2map.py`, que permite explorar gráficamente la ocupación del campus.

Detalles adicionales se podra encontrar en los distintos archivos del proyecto
