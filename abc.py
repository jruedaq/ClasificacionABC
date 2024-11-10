import pandas as pd

def clasificacion_abc(items):
    valor_total = items['valor'].sum()

    items['porcentaje'] = (items['valor'] / valor_total) * 100

    items_ordenados = items.sort_values(by='valor', ascending=False).reset_index(drop=True)

    acumulado = 0
    categorias = []
    for _, item in items_ordenados.iterrows():
        acumulado += item['porcentaje']
        if acumulado <= 80:
            categorias.append('A')
        elif acumulado <= 95:
            categorias.append('B')
        else:
            categorias.append('C')

    items_ordenados['categoria'] = categorias

    return items_ordenados

def procesar_csv(ruta_csv):
    items = pd.read_csv(ruta_csv)
    resultado = clasificacion_abc(items)
    return resultado

ruta_csv = 'inventario.csv'
resultado = procesar_csv(ruta_csv)

print("Clasificación ABC de los artículos:")
print(resultado)
