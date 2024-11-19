from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Operations import Operations

app = Flask(__name__)
app.secret_key = 'secret_key'

# Configuración de rutas
UPLOAD_FOLDER = './tmp/uploads'
STATIC_FOLDER = './static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/abc', methods=['GET', 'POST'])
def abc():
    resultados = None
    mensaje_error = None

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No se ha subido ningún archivo.', 'danger')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('El archivo seleccionado está vacío.', 'danger')
            return redirect(request.url)

        try:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            items = pd.read_csv(file_path)

            if 'nombre' not in items.columns or 'valor' not in items.columns:
                mensaje_error = "El archivo CSV debe contener las columnas 'nombre' y 'valor'."
                return render_template('abc.html', resultados=None, mensaje_error=mensaje_error)

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

            resultados = items_ordenados.to_dict(orient='records')

            plt.figure(figsize=(12, 6))
            colores = ['red' if cat == 'A' else 'yellow' if cat == 'B' else 'green' for cat in categorias]
            plt.bar(items_ordenados['nombre'], items_ordenados['valor'], color=colores)
            plt.xlabel('Artículos')
            plt.ylabel('Valor')
            plt.title('Clasificación ABC - Histograma de Valores')
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(os.path.join(STATIC_FOLDER, 'histograma.png'))
            plt.close()

            plt.figure(figsize=(12, 6))
            plt.plot(items_ordenados['nombre'], items_ordenados['acumulado'], marker='o', color='blue')
            plt.axhline(y=80, color='orange', linestyle='--', label='Límite Categoría A (80%)')
            plt.axhline(y=95, color='purple', linestyle='--', label='Límite Categoría B (95%)')
            plt.xlabel('Artículos')
            plt.ylabel('Porcentaje Acumulado (%)')
            plt.title('Clasificación ABC - Porcentaje Acumulado')
            plt.xticks(rotation=45, ha="right")
            plt.legend(loc='upper left')
            plt.tight_layout()
            plt.savefig(os.path.join(STATIC_FOLDER, 'linea_acumulado.png'))
            plt.close()

        except Exception as e:
            mensaje_error = f"Error al procesar el archivo: {str(e)}"
            return render_template('abc.html', resultados=None, mensaje_error=mensaje_error)

    return render_template('abc.html', resultados=resultados, mensaje_error=mensaje_error)

@app.route('/colas', methods=['GET', 'POST'])
def colas():
    """Teoría de Colas"""
    resultados = None
    mensaje_error = None

    if request.method == 'POST':
        try:
            # Leer parámetros desde el formulario
            A = float(request.form.get('A', 0))  # Tasa de Llegada
            S = float(request.form.get('S', 0))  # Tasa de Servicio
            n = int(request.form.get('n', 1))   # Número de Servidores

            # Validar que los valores sean mayores a 0
            if A <= 0 or S <= 0 or n <= 0:
                mensaje_error = "Los valores de A, S y n deben ser mayores a 0."
            else:
                # Crear instancia de Operations y calcular métricas
                operations = Operations(A, S, n)
                resultados = {
                    "Lq": operations.Lq(),     # Longitud promedio de la línea
                    "Wq": operations.Wq(),     # Tiempo de espera promedio en la línea
                    "Ls": operations.Ls(),     # Longitud promedio del sistema
                    "Ws": operations.Ws(),     # Tiempo de espera promedio en el sistema
                    "U": operations.U(),       # Porcentaje de ocupación del servidor
                    "PLs": operations.PLs(),   # Probabilidad de que las personas estén esperando
                    "Ocio": operations.ocio(), # Tiempo de distracción (ocio)
                }

        except ValueError:
            mensaje_error = "Por favor, introduce valores numéricos válidos."
        except Exception as e:
            mensaje_error = f"Error al procesar los datos: {str(e)}"

    return render_template('colas.html', resultados=resultados, mensaje_error=mensaje_error)

@app.route('/descargar-ejemplo')
def descargar_ejemplo():
    """Permite descargar el archivo de ejemplo inventario.csv"""
    try:
        return send_from_directory('static', 'inventario.csv', as_attachment=True)
    except Exception as e:
        flash(f"Error al intentar descargar el archivo: {str(e)}", 'danger')
        return redirect(url_for('abc'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
