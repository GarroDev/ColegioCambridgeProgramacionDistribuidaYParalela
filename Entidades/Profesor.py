from Entidades.Persona import Persona

class Profesor(Persona):
    def __init__(self, id, area, oficina, tipo_profesor):
        super().__init__(id, "Profesor", area, oficina)
        self.tipo_profesor = tipo_profesor  # "Planta" o "Contratista"
    
    def __str__(self):
        return f"{super().__str__()}, Tipo Profesor: {self.tipo_profesor}"