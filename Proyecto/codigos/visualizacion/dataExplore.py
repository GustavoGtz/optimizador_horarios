#Script to explore the classrooms

import pandas as pd

# Ruta del archivo
data = '' # Broken root, change it

# Leer la hoja (puedes especificar `sheet_name` si conoces el nombre)
df = pd.read_excel(data)

# Asegurarse de que las columnas existen
required_columns = ['MATERIA', 'TIPO_HR', 'UBICACION']
if not all(col in df.columns for col in required_columns):
    missing = [col for col in required_columns if col not in df.columns]
    raise ValueError(f"Faltan las siguientes columnas en el archivo: {missing}")

# Filtrar solo las columnas relevantes
df_filtered = df[required_columns].dropna()

# Mostrar ubicaciones únicas
print("=== UBICACIONES DISPONIBLES ===")
ubicaciones = sorted(df_filtered['UBICACION'].unique())
for i, ub in enumerate(ubicaciones, start=1):
    print(f"{i}. {ub}")

# Filtro interactivo
while True:
    try:
        selection = input("\nSelecciona el número de una ubicación para ver sus materias (o 'q' para salir): ")
        if selection.lower() == 'q':
            print("Saliendo.")
            break
        idx = int(selection) - 1
        if 0 <= idx < len(ubicaciones):
            ub_filter = ubicaciones[idx]
            subset = df_filtered[df_filtered['UBICACION'] == ub_filter]
            print(f"\n=== Datos para UBICACION: {ub_filter} ===")
            print(subset.to_string(index=False))
        else:
            print("Número fuera de rango. Intenta de nuevo.")
    except ValueError:
        print("Entrada no válida. Escribe un número o 'q'.")
