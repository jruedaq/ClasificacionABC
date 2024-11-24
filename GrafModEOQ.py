import math
import numpy as np
import matplotlib.pyplot as plt

def calcular_eoq(D, S, H):
    """Calcula la cantidad óptima de pedido (EOQ)."""
    return math.sqrt((2 * D * S) / H)

def calcular_demanda_diaria(D):
    """Calcula la demanda diaria basada en la demanda anual."""
    return D / 365

def calcular_n(D, EOQ):
    """Calcula el número de órdenes necesarias por año."""
    return D / EOQ

def calcular_l(dias_trabajo, D, EOQ):
    """Calcula el tiempo promedio entre pedidos (Lead Time o L)."""
    return dias_trabajo / (D / EOQ)

def calcular_rop(D, dias_trabajo, S, H):
    """
    Calcula el punto de reorden (ROP).
    Fórmula: ROP = demanda_diaria * lead_time
    """
    demanda_diaria = calcular_demanda_diaria(D)
    lead_time = calcular_l(dias_trabajo, D, calcular_eoq(D, S, H))
    return demanda_diaria * lead_time

def calcular_inventario_seguridad(desviacion_semanal, semanas, factor_seguridad):
    """
    Calcula el inventario de seguridad (IS).
    Fórmula: IS = Z * desviación_durante_entrega
    """
    desviacion_durante_entrega = desviacion_semanal * math.sqrt(semanas)
    return factor_seguridad * desviacion_durante_entrega



def mostrar_grafica(D, S, H, dias_trabajo, ruta):
    """
    Genera y guarda un gráfico de nivel de inventario basado en EOQ, ROP y Lead Time.
    """
    EOQ = calcular_eoq(D, S, H)
    demanda_diaria = calcular_demanda_diaria(D)
    N = calcular_n(D, EOQ)
    L = calcular_l(dias_trabajo, D, EOQ)
    ROP = calcular_rop(D, dias_trabajo, S, H)

    tiempo_total = dias_trabajo
    tiempo = np.linspace(0, tiempo_total, 1000)
    inventario = np.zeros_like(tiempo)
    pedidos = int(N)
    duracion_ciclo = tiempo_total / pedidos

    for i in range(pedidos):
        inicio_ciclo = i * duracion_ciclo
        fin_ciclo = (i + 1) * duracion_ciclo
        indices = (tiempo >= inicio_ciclo) & (tiempo < fin_ciclo)
        inventario[indices] = EOQ - (demanda_diaria * (tiempo[indices] - inicio_ciclo))

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(tiempo, inventario, label="Nivel de inventario", color="blue")
    plt.axhline(EOQ, color="green", linestyle="--", label="EOQ (Cantidad Óptima de Pedido)")
    plt.axhline(ROP, color="red", linestyle="--", label="ROP (Punto de Reorden)")
    plt.axvline(L, color="purple", linestyle="--", label="Lead Time")
    plt.title("Nivel de Inventario")
    plt.xlabel("Tiempo (días)")
    plt.ylabel("Inventario")
    plt.legend()
    plt.grid()
    plt.tight_layout()

    # Guardar el gráfico en la ruta especificada
    plt.savefig(ruta)
    plt.close()

