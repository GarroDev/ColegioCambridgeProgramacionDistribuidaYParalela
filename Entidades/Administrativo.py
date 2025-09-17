from Entidades.Persona import Persona

class Administrativo(Persona):
    def __init__(self, id, area, oficina):
        super().__init__(id, "Administrativo", area, oficina)