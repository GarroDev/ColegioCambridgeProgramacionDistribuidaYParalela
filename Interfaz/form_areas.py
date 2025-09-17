import tkinter as tk
from tkinter import ttk, messagebox

class FormAreas:
    def __init__(self, parent, crud, volver_callback, estilos):
        self.parent = parent
        self.crud = crud
        self.volver_callback = volver_callback
        self.estilos = estilos

        for widget in parent.winfo_children():
            widget.destroy()

        self.crear_interfaz()
        self.cargar_areas()

    def crear_interfaz(self):
        titulo = ttk.Label(self.parent, text="Gestión de Áreas", style="Titulo.TLabel")
        titulo.pack(pady=10)

        frame_tabla = ttk.Frame(self.parent, style="Frame.TFrame")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(frame_tabla, columns=("nombre",), show="headings", height=15)
        self.tree.heading("nombre", text="Nombre del Área")
        self.tree.column("nombre", width=400, anchor=tk.CENTER)

        scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        frame_botones = ttk.Frame(self.parent, style="Frame.TFrame")
        frame_botones.pack(fill=tk.X, padx=20, pady=10)

        ttk.Button(frame_botones, text="Agregar", command=self.agregar_area, style="BotonAgregar.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Editar", command=self.editar_area, style="BotonEditar.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Eliminar", command=self.eliminar_area, style="BotonEliminar.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Volver", command=self.volver_callback, style="BotonPrincipal.TButton").pack(side=tk.RIGHT, padx=5)

        frame_info = ttk.Frame(self.parent, style="Frame.TFrame")
        frame_info.pack(fill=tk.X, padx=20, pady=(0, 10))

        self.label_info = ttk.Label(frame_info, text="Total de áreas: 0", style="Contador.TLabel")
        self.label_info.pack(side=tk.LEFT)

        self.label_vacio = ttk.Label(frame_tabla, text="No hay áreas registradas", style="Vacio.TLabel")
        self.label_vacio.grid(row=0, column=0, sticky="nsew")

    def cargar_areas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        areas = self.crud.leer_areas()

        for area in areas:
            self.tree.insert("", tk.END, values=(area["nombre"],))

        self.label_info.config(text=f"Total de áreas: {len(areas)}")

        if len(areas) == 0:
            self.label_vacio.grid(row=0, column=0, sticky="nsew")
            self.tree.grid_remove()
        else:
            self.label_vacio.grid_remove()
            self.tree.grid()
            self.tree.selection_set(self.tree.get_children()[0])
            self.tree.focus(self.tree.get_children()[0])

    def agregar_area(self):
        ventana = tk.Toplevel(self.parent)
        ventana.title("Agregar Área")
        ventana.geometry("400x200")
        ventana.resizable(False, False)

        ventana.transient(self.parent)
        ventana.grab_set()
        ventana.configure(bg="#F5F5F5")

        frame = ttk.Frame(ventana, style="Frame.TFrame", padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Nombre del Área:", style="Campo.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))
        entry_nombre = ttk.Entry(frame, style="Entrada.TEntry", width=30)
        entry_nombre.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        entry_nombre.focus()

        frame_botones = ttk.Frame(frame, style="Frame.TFrame")
        frame_botones.grid(row=2, column=0, sticky="ew")

        def guardar():
            nombre = entry_nombre.get().strip()
            if nombre:
                areas = self.crud.leer_areas()
                for area in areas:
                    if area["nombre"].lower() == nombre.lower():
                        messagebox.showerror("Error", f"Ya existe un área con el nombre '{nombre}'")
                        return

                self.crud.crear_area(nombre)
                self.cargar_areas()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "El nombre no puede estar vacío")

        ttk.Button(frame_botones, text="Guardar", command=guardar, style="BotonPrincipal.TButton", width=15).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy, style="BotonSecundario.TButton", width=15).pack(side=tk.RIGHT)

        frame.columnconfigure(0, weight=1)
        ventana.bind('<Return>', lambda e: guardar())
        ventana.bind('<Escape>', lambda e: ventana.destroy())

    def editar_area(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un área para editar")
            return

        nombre_actual = self.tree.item(seleccion[0])['values'][0]

        ventana = tk.Toplevel(self.parent)
        ventana.title("Editar Área")
        ventana.geometry("400x200")
        ventana.resizable(False, False)

        ventana.transient(self.parent)
        ventana.grab_set()
        ventana.configure(bg="#F5F5F5")

        frame = ttk.Frame(ventana, style="Frame.TFrame", padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Nuevo Nombre:", style="Campo.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))
        entry_nombre = ttk.Entry(frame, style="Entrada.TEntry", width=30)
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        entry_nombre.focus()

        frame_botones = ttk.Frame(frame, style="Frame.TFrame")
        frame_botones.grid(row=2, column=0, sticky="ew")

        def guardar():
            nuevo_nombre = entry_nombre.get().strip()
            if nuevo_nombre and nuevo_nombre != nombre_actual:
                areas = self.crud.leer_areas()
                for area in areas:
                    if area["nombre"].lower() == nuevo_nombre.lower():
                        messagebox.showerror("Error", f"Ya existe un área con el nombre '{nuevo_nombre}'")
                        return

                if self.crud.actualizar_area(nombre_actual, nuevo_nombre):
                    self.cargar_areas()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el área")
            else:
                messagebox.showerror("Error", "Ingrese un nombre válido y diferente")

        ttk.Button(frame_botones, text="Guardar", command=guardar, style="BotonPrincipal.TButton", width=15).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy, style="BotonSecundario.TButton", width=15).pack(side=tk.RIGHT)

        frame.columnconfigure(0, weight=1)
        ventana.bind('<Return>', lambda e: guardar())
        ventana.bind('<Escape>', lambda e: ventana.destroy())

    def eliminar_area(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un área para eliminar")
            return

        nombre = self.tree.item(seleccion[0])['values'][0]

        respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro que desea eliminar el área '{nombre}'?")
        if respuesta:
            if self.crud.eliminar_area(nombre):
                self.cargar_areas()
                messagebox.showinfo("Éxito", f"Área '{nombre}' eliminada")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el área")
