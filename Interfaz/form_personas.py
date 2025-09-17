import tkinter as tk
from tkinter import ttk, messagebox

class FormPersonas:
    def __init__(self, parent, crud, volver_callback, estilos):
        self.parent = parent
        self.crud = crud
        self.volver_callback = volver_callback
        self.estilos = estilos

        for widget in parent.winfo_children():
            widget.destroy()

        self.crear_interfaz()
        self.cargar_personas()

    def crear_interfaz(self):
        titulo = ttk.Label(self.parent, text="Gestión de Personas", style="Titulo.TLabel")
        titulo.pack(pady=10)

        frame_tabla = ttk.Frame(self.parent, style="Frame.TFrame")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Tabla
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=("id", "nombre", "apellido", "edad", "tipo", "area", "oficina"),
            show="headings",
            height=15
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("apellido", text="Apellido")
        self.tree.heading("edad", text="Edad")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("area", text="Área")
        self.tree.heading("oficina", text="Oficina")

        for col in ("id", "nombre", "apellido", "edad", "tipo", "area", "oficina"):
            self.tree.column(col, width=120, anchor=tk.CENTER)

        scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # Botones
        frame_botones = ttk.Frame(self.parent, style="Frame.TFrame")
        frame_botones.pack(fill=tk.X, padx=20, pady=10)

        ttk.Button(frame_botones, text="Agregar Profesor", command=self.agregar_profesor, style="BotonAgregar.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Agregar Admin", command=self.agregar_administrativo, style="BotonAgregar.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Editar", command=self.editar_persona, style="BotonEditar.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Eliminar", command=self.eliminar_persona, style="BotonEliminar.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Volver", command=self.volver_callback, style="BotonPrincipal.TButton").pack(side=tk.RIGHT, padx=5)

    def cargar_personas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        personas = self.crud.leer_personas()

        for p in personas:
            tipo_extra = ""
            if p["tipo"] == "Profesor" and p.get("tipo_profesor"):
                tipo_extra = f" ({p['tipo_profesor']} - {p.get('especialidad','')})"
            if p["tipo"] == "Administrativo" and p.get("puesto"):
                tipo_extra = f" ({p['puesto']})"

            self.tree.insert("", tk.END, values=(
                p["id"], p["nombre"], p["apellido"], p["edad"],
                f"{p['tipo']}{tipo_extra}", p["area"], p["oficina"]
            ))

    # =========================
    #   AGREGAR PROFESOR
    # =========================
    def agregar_profesor(self):
        ventana = tk.Toplevel(self.parent)
        ventana.title("Agregar Profesor")
        ventana.geometry("400x450")
        ventana.resizable(False, False)
        ventana.transient(self.parent)
        ventana.grab_set()

        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        labels = ["Nombre", "Apellido", "Edad", "Área", "Oficina", "Tipo Profesor", "Especialidad"]
        entries = {}

        for i, label in enumerate(labels):
            ttk.Label(frame, text=f"{label}:").grid(row=i*2, column=0, sticky="w")
            if label == "Área":
                entries[label] = ttk.Combobox(frame, values=[a["nombre"] for a in self.crud.leer_areas()], state="readonly")
            elif label == "Oficina":
                entries[label] = ttk.Combobox(frame, values=[o["nombre"] for o in self.crud.leer_oficinas()], state="readonly")
            elif label == "Tipo Profesor":
                entries[label] = ttk.Combobox(frame, values=["Planta", "Contratista"], state="readonly")
                entries[label].set("Planta")
            else:
                entries[label] = ttk.Entry(frame)
            entries[label].grid(row=i*2+1, column=0, sticky="ew", pady=5)

        def guardar():
            try:
                self.crud.crear_profesor(
                    entries["Nombre"].get(),
                    entries["Apellido"].get(),
                    int(entries["Edad"].get()),
                    entries["Área"].get(),
                    entries["Oficina"].get(),
                    entries["Tipo Profesor"].get(),
                    entries["Especialidad"].get()
                )
                self.cargar_personas()
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}")

        ttk.Button(frame, text="Guardar", command=guardar, style="BotonPrincipal.TButton").grid(row=len(labels)*2, column=0, pady=10)

    # =========================
    #   AGREGAR ADMINISTRATIVO
    # =========================
    def agregar_administrativo(self):
        ventana = tk.Toplevel(self.parent)
        ventana.title("Agregar Administrativo")
        ventana.geometry("400x350")
        ventana.resizable(False, False)
        ventana.transient(self.parent)
        ventana.grab_set()

        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        labels = ["Nombre", "Apellido", "Edad", "Área", "Oficina", "Puesto"]
        entries = {}

        for i, label in enumerate(labels):
            ttk.Label(frame, text=f"{label}:").grid(row=i*2, column=0, sticky="w")
            if label == "Área":
                entries[label] = ttk.Combobox(frame, values=[a["nombre"] for a in self.crud.leer_areas()], state="readonly")
            elif label == "Oficina":
                entries[label] = ttk.Combobox(frame, values=[o["nombre"] for o in self.crud.leer_oficinas()], state="readonly")
            else:
                entries[label] = ttk.Entry(frame)
            entries[label].grid(row=i*2+1, column=0, sticky="ew", pady=5)

        def guardar():
            try:
                self.crud.crear_administrativo(
                    entries["Nombre"].get(),
                    entries["Apellido"].get(),
                    int(entries["Edad"].get()),
                    entries["Área"].get(),
                    entries["Oficina"].get(),
                    entries["Puesto"].get()
                )
                self.cargar_personas()
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}")

        ttk.Button(frame, text="Guardar", command=guardar, style="BotonPrincipal.TButton").grid(row=len(labels)*2, column=0, pady=10)

    # =========================
    #   EDITAR PERSONA
    # =========================
    def editar_persona(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una persona para editar")
            return

        item = self.tree.item(seleccion[0])
        persona_id, nombre, apellido, edad, tipo, area, oficina = item["values"]

        ventana = tk.Toplevel(self.parent)
        ventana.title("Editar Persona")
        ventana.geometry("400x400")
        ventana.resizable(False, False)
        ventana.transient(self.parent)
        ventana.grab_set()

        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Campos básicos
        ttk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="w")
        entry_nombre = ttk.Entry(frame)
        entry_nombre.insert(0, nombre)
        entry_nombre.grid(row=1, column=0, sticky="ew", pady=5)

        ttk.Label(frame, text="Apellido:").grid(row=2, column=0, sticky="w")
        entry_apellido = ttk.Entry(frame)
        entry_apellido.insert(0, apellido)
        entry_apellido.grid(row=3, column=0, sticky="ew", pady=5)

        ttk.Label(frame, text="Edad:").grid(row=4, column=0, sticky="w")
        entry_edad = ttk.Entry(frame)
        entry_edad.insert(0, edad)
        entry_edad.grid(row=5, column=0, sticky="ew", pady=5)

        ttk.Label(frame, text="Área:").grid(row=6, column=0, sticky="w")
        combo_area = ttk.Combobox(frame, values=[a["nombre"] for a in self.crud.leer_areas()], state="readonly")
        combo_area.set(area)
        combo_area.grid(row=7, column=0, sticky="ew", pady=5)

        ttk.Label(frame, text="Oficina:").grid(row=8, column=0, sticky="w")
        combo_oficina = ttk.Combobox(frame, values=[o["nombre"] for o in self.crud.leer_oficinas()], state="readonly")
        combo_oficina.set(oficina)
        combo_oficina.grid(row=9, column=0, sticky="ew", pady=5)

        def guardar():
            try:
                nuevos_datos = {
                    "nombre": entry_nombre.get(),
                    "apellido": entry_apellido.get(),
                    "edad": int(entry_edad.get()),
                    "area": combo_area.get(),
                    "oficina": combo_oficina.get()
                }
                self.crud.actualizar_persona(persona_id, nuevos_datos)
                self.cargar_personas()
                ventana.destroy()
                messagebox.showinfo("Éxito", "Persona actualizada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {e}")

        ttk.Button(frame, text="Guardar", command=guardar, style="BotonPrincipal.TButton").grid(row=10, column=0, pady=10)

    # =========================
    #   ELIMINAR PERSONA
    # =========================
    def eliminar_persona(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una persona para eliminar")
            return

        item = self.tree.item(seleccion[0])
        persona_id = item["values"][0]

        confirmar = messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar la persona con ID {persona_id}?")
        if confirmar:
            try:
                self.crud.eliminar_persona(persona_id)
                self.cargar_personas()
                messagebox.showinfo("Éxito", "Persona eliminada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")
