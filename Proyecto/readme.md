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

Para más detalles, en cada una de las carpetas mencionadas se puede consultar documentación técnica adicional.