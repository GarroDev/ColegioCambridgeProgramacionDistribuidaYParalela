import sys, os
# Permite importar paquetes del proyecto cuando se lanza desde raíz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import strawberry
from typing import List, Optional

# ---------- Tipos e inputs ----------
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
    area: Optional[str] = None
    oficina: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    edad: Optional[int] = None
    tipo_profesor: Optional[str] = None
    especialidad: Optional[str] = None
    puesto: Optional[str] = None

@strawberry.type
class ResOk:
    ok: bool

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
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    edad: Optional[int] = None
    area: Optional[str] = None
    oficina: Optional[str] = None
    tipo_profesor: Optional[str] = None
    especialidad: Optional[str] = None
    puesto: Optional[str] = None

@strawberry.type
class ReporteAreaEmpleados:
    area: str
    total_empleados: int
    profesores: int
    administrativos: int
    profesores_planta: int
    profesores_contratistas: int

# ---------- Servicios (con import flexible) ----------
from Servicios.crud import CRUD
try:
    # si tienes Servicios/reportes.py
    from Servicios.reportes import Reportes
except Exception:
    # si la clase Reportes está definida en el mismo archivo crud.py
    from Servicios.crud import Reportes  # type: ignore

crud = CRUD()
reportes = Reportes(crud)

# ---------- Helpers de mapeo ----------
def _map_area(row: dict) -> AreaType:
    # row = {'id': int, 'nombre': str}
    return AreaType(id=int(row["id"]), nombre=str(row["nombre"]))

def _map_oficina(row: dict) -> OficinaType:
    return OficinaType(id=int(row["id"]), nombre=str(row["nombre"]))

def _map_persona(row: dict) -> PersonaType:
    # row = columnas de tu SELECT con LEFT JOINs
    return PersonaType(
        id=int(row["id"]),
        tipo=str(row["tipo"]),
        area=row.get("area"),
        oficina=row.get("oficina"),
        nombre=row.get("nombre"),
        apellido=row.get("apellido"),
        edad=row.get("edad"),
        tipo_profesor=row.get("tipo_profesor"),
        especialidad=row.get("especialidad"),
        puesto=row.get("puesto"),
    )

# ===================== QUERIES =====================
@strawberry.type
class Query:
    @strawberry.field
    def areas(self) -> List[AreaType]:
        return [_map_area(r) for r in crud.leer_areas()]

    @strawberry.field
    def oficinas(self) -> List[OficinaType]:
        return [_map_oficina(r) for r in crud.leer_oficinas()]

    @strawberry.field
    def personas(self) -> List[PersonaType]:
        return [_map_persona(r) for r in crud.leer_personas()]

    @strawberry.field
    def persona_por_id(self, id: int) -> Optional[PersonaType]:
        for p in crud.leer_personas():
            if int(p["id"]) == id:
                return _map_persona(p)
        return None

    @strawberry.field
    def reporte_areas_empleados(self) -> List[ReporteAreaEmpleados]:
        return [ReporteAreaEmpleados(**r) for r in reportes.generar_reporte_areas_empleados()]

# ===================== MUTATIONS =====================
@strawberry.type
class Mutation:
    # Áreas
    @strawberry.mutation
    def crear_area(self, input: AreaInput) -> AreaType:
        r = crud.crear_area(input.nombre)  # ideal: {"id":..., "nombre":...}
        # si tu CRUD aún no devuelve id, obtenlo con la última fila por nombre
        if "id" not in r:
            fila = [a for a in crud.leer_areas() if a["nombre"] == r["nombre"]][-1]
            return _map_area(fila)
        return AreaType(id=int(r["id"]), nombre=r["nombre"])

    @strawberry.mutation
    def actualizar_area(self, nombre_actual: str, nuevo_nombre: str) -> ResOk:
        ok = crud.actualizar_area(nombre_actual, nuevo_nombre)
        return ResOk(ok=bool(ok))

    @strawberry.mutation
    def eliminar_area(self, nombre: str) -> ResOk:
        ok = crud.eliminar_area(nombre)
        return ResOk(ok=bool(ok))

    # Oficinas
    @strawberry.mutation
    def crear_oficina(self, input: OficinaInput) -> OficinaType:
        r = crud.crear_oficina(input.nombre)
        if "id" not in r:
            fila = [o for o in crud.leer_oficinas() if o["nombre"] == r["nombre"]][-1]
            return _map_oficina(fila)
        return OficinaType(id=int(r["id"]), nombre=r["nombre"])

    @strawberry.mutation
    def actualizar_oficina(self, nombre_actual: str, nuevo_nombre: str) -> ResOk:
        ok = crud.actualizar_oficina(nombre_actual, nuevo_nombre)
        return ResOk(ok=bool(ok))

    @strawberry.mutation
    def eliminar_oficina(self, nombre: str) -> ResOk:
        ok = crud.eliminar_oficina(nombre)
        return ResOk(ok=bool(ok))

    # Personas
    @strawberry.mutation
    def crear_profesor(self, input: ProfesorInput) -> PersonaType:
        r = crud.crear_profesor(
            nombre=input.nombre,
            apellido=input.apellido,
            edad=int(input.edad),
            area=input.area,
            oficina=input.oficina,
            tipo_profesor=input.tipo_profesor,
            especialidad=input.especialidad or "",
        )
        # r ya es un dict con todos los campos
        return _map_persona(r)

    @strawberry.mutation
    def crear_administrativo(self, input: AdministrativoInput) -> PersonaType:
        r = crud.crear_administrativo(
            nombre=input.nombre,
            apellido=input.apellido,
            edad=int(input.edad),
            area=input.area,
            oficina=input.oficina,
            puesto=input.puesto or "",
        )
        return _map_persona(r)

    @strawberry.mutation
    def actualizar_persona(self, id: int, input: PersonaUpdateInput) -> ResOk:
        # Convierte el input (dataclass) a dict llano
        patch = {k: v for k, v in input.__dict__.items() if v is not None}
        ok = crud.actualizar_persona(id, patch)
        return ResOk(ok=bool(ok))

    @strawberry.mutation
    def eliminar_persona(self, id: int) -> ResOk:
        ok = crud.eliminar_persona(id)
        return ResOk(ok=bool(ok))

schema = strawberry.Schema(Query, Mutation)
