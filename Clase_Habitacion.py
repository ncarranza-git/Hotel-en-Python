class Habitacion:
    def __init__(self, tipo, numero, precio):
        self.tipo = tipo
        self.numero = numero
        self.precio = precio
        self.ocupada = False
        
    def reservar(self):
        if not self.ocupada:
            self.ocupada = True
            return True
        return False