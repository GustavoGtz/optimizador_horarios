# Visualización

Los principales programas de visualización fueron desarrollados utilizando **PyQt5** y **psycopg2-binary**, junto con una serie de recursos gráficos en estilo *pixel art*.

A continuación se presenta una breve descripción de los archivos más relevantes contenidos en esta sección:

- `cu2map.py`: Aplicación principal de visualización. Permite explorar el campus universitario de manera interactiva, utilizando datos extraídos desde la base de datos o generados por el modelo. Ofrece una representación espacial de la ocupación por aula, edificio y zona.

- `agregador.py`: Aplicación encargada de generar materias de ejemplo, así como la estructura de carga académica que posteriormente será utilizada por el optimizador.

- `dataExplore.py`: Script sencillo para explorar y analizar archivos CSV. Fue utilizado durante las pruebas para verificar la estructura de los datos antes de integrarlos al sistema principal.

- `dataPreOpt.csv`: Archivo de ejemplo que contiene un horario generado antes de pasar por el optimizador. Este archivo sirve como referencia o entrada de prueba para validar la visualización.
