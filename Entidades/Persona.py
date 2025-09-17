class Persona:
    def __init__(self, id, tipo, area, oficina, tipo_profesor=None):
        self.id = id
        self.tipo = tipo  # "Profesor" o "Administrativo"
        self.area = area  # Nombre del área
        self.oficina = oficina  # Nombre de la oficina
        self.tipo_profesor = tipo_profesor  # Solo aplica si es profesor
    
    def __str__(self):
        if self.tipo == "Profesor" and self.tipo_profesor:
            return f"ID: {self.id}, Tipo: {self.tipo} ({self.tipo_profesor}), Área: {self.area}, Oficina: {self.oficina}"
        return f"ID: {self.id}, Tipo: {self.tipo}, Área: {self.area}, Oficina: {self.oficina}"
