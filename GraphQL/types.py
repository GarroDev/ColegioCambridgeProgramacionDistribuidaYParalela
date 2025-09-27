import strawberry
from typing import Optional, List

@strawberry.type
class AreaType:
    id: int
    nombre: str

@strawberry.type
class OficinaType:
    id: int
    nombre: str

@strawberry.type
class PersonaType:
    id: int
    tipo: str
    area: Optional[str]
    oficina: Optional[str]
    nombre: Optional[str]
    apellido: Optional[str]
    edad: Optional[int]
    # campos opcionales según el tipo
    tipo_profesor: Optional[str] = None
    especialidad: Optional[str] = None
    puesto: Optional[str] = None

@strawberry.type
class ResOk:
    ok: bool

# ---------- Inputs ----------
@strawberry.input
class AreaInput:
    nombre: str

@strawberry.input
class OficinaInput:
    nombre: str

@strawberry.input
class PersonaBaseInput:
    nombre: str
    apellido: str
    edad: int
    area: str
    oficina: str

@strawberry.input
class ProfesorInput(PersonaBaseInput):
    tipo_profesor: str        # "Planta" | "Contratista"
    especialidad: Optional[str] = ""

@strawberry.input
class AdministrativoInput(PersonaBaseInput):
    puesto: Optional[str] = ""

@strawberry.input
class PersonaUpdateInput:
    # todos opcionales para actualización parcial
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    edad: Optional[int] = None
    area: Optional[str] = None
    oficina: Optional[str] = None
    # según el tipo
    tipo_profesor: Optional[str] = None
    especialidad: Optional[str] = None
    puesto: Optional[str] = None

# ---------- Reporte ----------
@strawberry.type
class ReporteAreaEmpleados:
    area: str
    total_empleados: int
    profesores: int
    administrativos: int
    profesores_planta: int
    profesores_contratistas: int
