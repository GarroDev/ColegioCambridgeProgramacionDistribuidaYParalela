class Oficina:
    def __init__(self, codigo):
        self.codigo = codigo
        self.empleados = []  # Lista de IDs de empleados
    
    def agregar_empleado(self, id_empleado):
        if id_empleado not in self.empleados:
            self.empleados.append(id_empleado)
    
    def __str__(self):
        return f"Oficina: {self.codigo}, Empleados: {len(self.empleados)}"