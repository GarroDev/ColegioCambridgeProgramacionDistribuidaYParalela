import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ReportesVista:
    def __init__(self, parent, crud, volver_callback, estilos):
        self.parent = parent
        self.crud = crud
        self.volver_callback = volver_callback
        self.estilos = estilos

        for widget in parent.winfo_children():
            widget.destroy()

        self.crear_interfaz()
        self.generar_reporte()

    def crear_interfaz(self):
        titulo = ttk.Label(self.parent, text="Reporte de Áreas y Empleados", style="Titulo.TLabel")
        titulo.pack(pady=10)

        frame_tabla = ttk.Frame(self.parent, style="Frame.TFrame")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Tabla con más columnas
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("Área", "ID", "Nombre", "Apellido", "Edad", "Tipo", "Oficina"),
            show="headings",
            height=15
        )

        self.tree.heading("Área", text="Área")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Oficina", text="Oficina")

        for col in ("Área", "ID", "Nombre", "Apellido", "Edad", "Tipo", "Oficina"):
            self.tree.column(col, width=120, anchor=tk.CENTER)

        scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        frame_botones = ttk.Frame(self.parent, style="Frame.TFrame")
        frame_botones.pack(fill=tk.X, padx=20, pady=10)

        # 🔹 Ahora exporta en TXT en lugar de actualizar
        ttk.Button(frame_botones, text="Exportar TXT", command=self.exportar_txt, style="BotonPrincipal.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Volver", command=self.volver_callback, style="BotonPrincipal.TButton").pack(side=tk.RIGHT, padx=5)

        self.label_info = ttk.Label(self.parent, text="Total de áreas: 0 | Total de empleados: 0", style="Contador.TLabel")
        self.label_info.pack(side=tk.LEFT, padx=20)

    def generar_reporte(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        areas = self.crud.leer_areas()
        personas = self.crud.leer_personas()

        total_empleados = 0
        for area in areas:
            # Nodo del área
            area_item = self.tree.insert("", tk.END, values=(area["nombre"], "", "", "", "", "", ""))

            empleados = [p for p in personas if p["area"] == area["nombre"]]

            for persona in empleados:
                tipo = persona["tipo"]
                if tipo == "Profesor":
                    tipo = f"{tipo} ({persona.get('tipo_profesor','')} - {persona.get('especialidad','')})"
                elif tipo == "Administrativo":
                    tipo = f"{tipo} ({persona.get('puesto','')})"

                self.tree.insert(area_item, tk.END, values=(
                    "",
                    persona["id"],
                    persona.get("nombre", ""),
                    persona.get("apellido", ""),
                    persona.get("edad", ""),
                    tipo,
                    persona["oficina"]
                ))

            total_empleados += len(empleados)

        self.label_info.config(text=f"Total de áreas: {len(areas)} | Total de empleados: {total_empleados}")

    def exportar_txt(self):
        """
        Exporta el reporte en un archivo TXT
        """
        fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"reporte_{fecha_hora}.txt"

        try:
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write("REPORTE DE ÁREAS Y EMPLEADOS\n")
                f.write("="*60 + "\n")
                f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                areas = self.crud.leer_areas()
                personas = self.crud.leer_personas()

                total_empleados = 0
                for area in areas:
                    f.write(f"Área: {area['nombre']}\n")
                    empleados = [p for p in personas if p["area"] == area["nombre"]]

                    if empleados:
                        for persona in empleados:
                            tipo = persona["tipo"]
                            if tipo == "Profesor":
                                tipo = f"{tipo} ({persona.get('tipo_profesor','')} - {persona.get('especialidad','')})"
                            elif tipo == "Administrativo":
                                tipo = f"{tipo} ({persona.get('puesto','')})"

                            f.write(f"  - ID: {persona['id']}, Nombre: {persona.get('nombre','')} {persona.get('apellido','')}, Edad: {persona.get('edad','')}, Tipo: {tipo}, Oficina: {persona['oficina']}\n")
                        total_empleados += len(empleados)
                    else:
                        f.write("  Sin empleados asignados\n")
                    f.write("\n")

                f.write("="*60 + "\n")
                f.write(f"Total de áreas: {len(areas)}\n")
                f.write(f"Total de empleados: {total_empleados}\n")

            messagebox.showinfo("Éxito", f"Reporte exportado como {nombre_archivo}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el reporte: {str(e)}")
