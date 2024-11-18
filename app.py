import os
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Configurar Matplotlib para un backend sin GUI
import matplotlib.pyplot as plt

app = Flask(__name__)

# Configuración de rutas
app.config['UPLOAD_FOLDER'] = './uploads'
STATIC_FOLDER = './static'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# Función de clasificación ABC
def clasificacion_abc(items):
    valor_total = items['valor'].sum()
    items['porcentaje'] = (items['valor'] / valor_total) * 100
    items_ordenados = items.sort_values(by='valor', ascending=False).reset_index(drop=True)

    acumulado = 0
    categorias = []
    acumulado_porcentaje = []
    for _, item in items_ordenados.iterrows():
        acumulado += item['porcentaje']
        acumulado_porcentaje.append(acumulado)
        if acumulado <= 80:
            categorias.append('A')
        elif acumulado <= 95:
            categorias.append('B')
        else:
            categorias.append('C')

    items_ordenados['categoria'] = categorias
    items_ordenados['acumulado'] = acumulado_porcentaje
    items_ordenados['porcentaje'] = items_ordenados['porcentaje'].round(2)
    items_ordenados['acumulado'] = items_ordenados['acumulado'].round(2)
    return items_ordenados

# Generar gráficos
def generar_histograma(resultado, file_path):
    plt.figure(figsize=(12, 6))
    categorias = resultado['categoria']
    valores = resultado['valor']
    nombres = resultado['nombre']
    colores = ['red' if cat == 'A' else 'yellow' if cat == 'B' else 'green' for cat in categorias]
    plt.bar(nombres, valores, color=colores, alpha=0.7)
    plt.xlabel('Artículos')
    plt.ylabel('Valor')
    plt.title('Clasificación ABC - Histograma de Valores')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

def generar_linea_acumulado(resultado, file_path):
    plt.figure(figsize=(12, 6))
    nombres = resultado['nombre']
    acumulado = resultado['acumulado']
    plt.plot(nombres, acumulado, marker='o', color='blue', linewidth=2)
    plt.axhline(y=80, color='orange', linestyle='--', label='Límite Categoría A (80%)')
    plt.axhline(y=95, color='purple', linestyle='--', label='Límite Categoría B (95%)')
    plt.xlabel('Artículos')
    plt.ylabel('Porcentaje Acumulado (%)')
    plt.title('Clasificación ABC - Porcentaje Acumulado')
    plt.xticks(rotation=45, ha="right")
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            items = pd.read_csv(file_path)
            resultado = clasificacion_abc(items)

            # Convertir el DataFrame en una lista de diccionarios
            tabla = resultado.to_dict(orient='records')

            # Generar gráficos
            generar_histograma(resultado, os.path.join(STATIC_FOLDER, 'histograma.png'))
            generar_linea_acumulado(resultado, os.path.join(STATIC_FOLDER, 'linea_acumulado.png'))

            return render_template('index.html', tabla=tabla)
    return render_template('index.html', tabla=None)

if __name__ == '__main__':
    app.run(debug=True)
