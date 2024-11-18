import math

class Operations:
    def __init__(self, A, S, n):
        self.A = A
        self.S = S
        self.n = n

    def Lq(self):  # Longitud promedio de la línea
        return (self.A ** 2) / (self.S * (self.S - self.A))

    def Wq(self):  # Tiempo de espera promedio
        return (self.Lq() / self.A) * 60

    def Ls(self):  # Longitud promedio del sistema
        return self.A / (self.S - self.A)

    def Ws(self):  # Tiempo de espera promedio del sistema
        return (self.Ls() / self.A) * 60

    def U(self):  # La caja está ocupada
        return (self.A / self.S) * 100

    def PLs(self):  # Probabilidad de que haya personas esperando
        return (self.A / self.S) ** (self.Ls() + 1) * 100

    def ocio(self):  # Tiempo de distracción
        return (1 - (self.A / self.S)) * 100

    def Pn(self):  # Probabilidad de n clientes en el sistema
        return (1 - (self.A / self.S)) * (self.A / self.S) ** self.n * 100

    @staticmethod
    def leer_numero_positivo(variable):
        while True:
            try:
                numero = float(input(f"Introduce un valor positivo para {variable}: "))
                if numero <= 0:
                    print("Error: El número debe ser positivo. Intenta de nuevo.")
                else:
                    return numero
            except ValueError:
                print("Error: Solo se permiten números positivos en decimal o entero.")

    def redondear_hacia_arriba(self, cantidad):
        return math.ceil(cantidad)

    def redondear_hacia_abajo(self, cantidad):
        return math.floor(cantidad)
