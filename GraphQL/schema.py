import sys, os
# Permite importar paquetes del proyecto cuando se lanza desde raíz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import strawberry
from typing import List, Optional

from GraphQL.types import (
    AreaType, OficinaType, PersonaType, ResOk,
    AreaInput, OficinaInput,
    ProfesorInput, AdministrativoInput, PersonaUpdateInput,
    ReporteAreaEmpleados
)

from Servicios.crud import CRUD
from Servicios.reportes import Reportes

crud = CRUD()
reportes = Reportes(crud)

# --------- Helpers para mapear dicts -> tipos Strawberry ---------
def _map_area(row: dict) -> AreaType:
    return AreaType(id=row["id"], nombre=row["nombre"])

def _map_oficina(row: dict) -> OficinaType:
    return OficinaType(id=row["id"], nombre=row["nombre"])

def _map_persona(row: dict) -> PersonaType:
    return PersonaType(
        id=row["id"],
        tipo=row["tipo"],
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
    # ----- áreas -----
    @strawberry.field
    def areas(self) -> List[AreaType]:
        return [_map_area(r) for r in crud.leer_areas()]

    # ----- oficinas -----
    @strawberry.field
    def oficinas(self) -> List[OficinaType]:
        return [_map_oficina(r) for r in crud.leer_oficinas()]

    # ----- personas -----
    @strawberry.field
    def personas(self) -> List[PersonaType]:
        return [_map_persona(r) for r in crud.leer_personas()]

    @strawberry.field
    def persona_por_id(self, id: int) -> Optional[PersonaType]:
        data = [p for p in crud.leer_personas() if p["id"] == id]
        return _map_persona(data[0]) if data else None

    # ----- reportes -----
    @strawberry.field
    def reporte_areas_empleados(self) -> List[ReporteAreaEmpleados]:
        return [ReporteAreaEmpleados(**r) for r in reportes.generar_reporte_areas_empleados()]

# ===================== MUTATIONS =====================
@strawberry.type
class Mutation:
    # ----- Áreas -----
    @strawberry.mutation
    def crear_area(self, input: AreaInput) -> AreaType:
        r = crud.crear_area(input.nombre)
        # obtener id recién creado: una consulta rápida
        fila = [a for a in crud.leer_areas() if a["nombre"] == r["nombre"]][-1]
        return _map_area(fila)

    @strawberry.mutation
    def actualizar_area(self, nombre_actual: str, nuevo_nombre: str) -> ResOk:
        ok = crud.actualizar_area(nombre_actual, nuevo_nombre)
        return ResOk(ok=bool(ok))

    @strawberry.mutation
    def eliminar_area(self, nombre: str) -> ResOk:
        ok = crud.eliminar_area(nombre)
        return ResOk(ok=bool(ok))

    # ----- Oficinas -----
    @strawberry.mutation
    def crear_oficina(self, input: OficinaInput) -> OficinaType:
        r = crud.crear_oficina(input.nombre)
        fila = [o for o in crud.leer_oficinas() if o["nombre"] == r["nombre"]][-1]
        return _map_oficina(fila)

    @strawberry.mutation
    def actualizar_oficina(self, nombre_actual: str, nuevo_nombre: str) -> ResOk:
        ok = crud.actualizar_oficina(nombre_actual, nuevo_nombre)
        return ResOk(ok=bool(ok))

    @strawberry.mutation
    def eliminar_oficina(self, nombre: str) -> ResOk:
        ok = crud.eliminar_oficina(nombre)
        return ResOk(ok=bool(ok))

    # ----- Personas -----
    @strawberry.mutation
    def crear_profesor(self, input: ProfesorInput) -> PersonaType:
        r = crud.crear_profesor(
            nombre=input.nombre,
            apellido=input.apellido,
            edad=input.edad,
            area=input.area,
            oficina=input.oficina,
            tipo_profesor=input.tipo_profesor,
            especialidad=input.especialidad or ""
        )
        return _map_persona(r)

    @strawberry.mutation
    def crear_administrativo(self, input: AdministrativoInput) -> PersonaType:
        r = crud.crear_administrativo(
            nombre=input.nombre,
            apellido=input.apellido,
            edad=input.edad,
            area=input.area,
            oficina=input.oficina,
            puesto=input.puesto or ""
        )
        return _map_persona(r)

    @strawberry.mutation
    def actualizar_persona(self, id: int, input: PersonaUpdateInput) -> ResOk:
        ok = crud.actualizar_persona(id, dict(input.__dict__))
        return ResOk(ok=bool(ok))

    @strawberry.mutation
    def eliminar_persona(self, id: int) -> ResOk:
        ok = crud.eliminar_persona(id)
        return ResOk(ok=bool(ok))

schema = strawberry.Schema(Query, Mutation)
