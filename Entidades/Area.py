class Area:
    def __init__(self, nombre):
        self.nombre = nombre
        self.oficinas = []  # Lista de códigos de oficinas
    
    def agregar_oficina(self, codigo_oficina):
        if codigo_oficina not in self.oficinas:
            self.oficinas.append(codigo_oficina)
    
    def __str__(self):
        return f"Área: {self.nombre}, Oficinas: {len(self.oficinas)}"