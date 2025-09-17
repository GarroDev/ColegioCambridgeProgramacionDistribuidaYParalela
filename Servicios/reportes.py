class Reportes:
    def __init__(self, crud):
        self.crud = crud
    
    def generar_reporte_areas_empleados(self):
        areas = self.crud.leer_areas()
        personas = self.crud.leer_personas()
        
        reporte = []
        for area in areas:
            empleados_area = [p for p in personas if p["area"] == area["nombre"]]
            
            profesores = [p for p in empleados_area if p["tipo"] == "Profesor"]
            administrativos = [p for p in empleados_area if p["tipo"] == "Administrativo"]
            
            profesores_planta = [p for p in profesores if p["tipo_profesor"] == "Planta"]
            profesores_contratistas = [p for p in profesores if p["tipo_profesor"] == "Contratista"]
            
            reporte.append({
                "area": area["nombre"],
                "total_empleados": len(empleados_area),
                "profesores": len(profesores),
                "administrativos": len(administrativos),
                "profesores_planta": len(profesores_planta),
                "profesores_contratistas": len(profesores_contratistas)
            })
        
        return reporte
