import tkinter as tk
from tkinter import ttk, messagebox

class FormOficinas:
    def __init__(self, parent, crud, volver_callback, estilos):
        self.parent = parent
        self.crud = crud
        self.volver_callback = volver_callback
        self.estilos = estilos

        for widget in parent.winfo_children():
            widget.destroy()

        self.crear_interfaz()
        self.cargar_oficinas()

    def crear_interfaz(self):
        titulo = ttk.Label(self.parent, text="Gestión de Oficinas", style="Titulo.TLabel")
        titulo.pack(pady=10)

        frame_tabla = ttk.Frame(self.parent, style="Frame.TFrame")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(frame_tabla, columns=("nombre",), show="headings", height=15)
        self.tree.heading("nombre", text="Nombre de la Oficina")
        self.tree.column("nombre", width=400, anchor=tk.CENTER)

        scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        frame_botones = ttk.Frame(self.parent, style="Frame.TFrame")
        frame_botones.pack(fill=tk.X, padx=20, pady=10)

        ttk.Button(frame_botones, text="Agregar", command=self.agregar_oficina, style="BotonAgregar.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Editar", command=self.editar_oficina, style="BotonEditar.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Eliminar", command=self.eliminar_oficina, style="BotonEliminar.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Volver", command=self.volver_callback, style="BotonPrincipal.TButton").pack(side=tk.RIGHT, padx=5)

        frame_info = ttk.Frame(self.parent, style="Frame.TFrame")
        frame_info.pack(fill=tk.X, padx=20, pady=(0, 10))

        self.label_info = ttk.Label(frame_info, text="Total de oficinas: 0", style="Contador.TLabel")
        self.label_info.pack(side=tk.LEFT)

        self.label_vacio = ttk.Label(frame_tabla, text="No hay oficinas registradas", style="Vacio.TLabel")
        self.label_vacio.grid(row=0, column=0, sticky="nsew")

    def cargar_oficinas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        oficinas = self.crud.leer_oficinas()

        for oficina in oficinas:
            self.tree.insert("", tk.END, values=(oficina["nombre"],))

        self.label_info.config(text=f"Total de oficinas: {len(oficinas)}")

        if len(oficinas) == 0:
            self.label_vacio.grid(row=0, column=0, sticky="nsew")
            self.tree.grid_remove()
        else:
            self.label_vacio.grid_remove()
            self.tree.grid()
            self.tree.selection_set(self.tree.get_children()[0])
            self.tree.focus(self.tree.get_children()[0])

    def agregar_oficina(self):
        ventana = tk.Toplevel(self.parent)
        ventana.title("Agregar Oficina")
        ventana.geometry("400x200")
        ventana.resizable(False, False)

        ventana.transient(self.parent)
        ventana.grab_set()
        ventana.configure(bg="#F5F5F5")

        frame = ttk.Frame(ventana, style="Frame.TFrame", padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Nombre de la Oficina:", style="Campo.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))
        entry_nombre = ttk.Entry(frame, style="Entrada.TEntry", width=30)
        entry_nombre.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        entry_nombre.focus()

        frame_botones = ttk.Frame(frame, style="Frame.TFrame")
        frame_botones.grid(row=2, column=0, sticky="ew")

        def guardar():
            nombre = entry_nombre.get().strip()
            if nombre:
                oficinas = self.crud.leer_oficinas()
                for oficina in oficinas:
                    if oficina["nombre"].lower() == nombre.lower():
                        messagebox.showerror("Error", f"Ya existe una oficina con el nombre '{nombre}'")
                        return

                self.crud.crear_oficina(nombre)
                self.cargar_oficinas()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "El nombre no puede estar vacío")

        ttk.Button(frame_botones, text="Guardar", command=guardar, style="BotonPrincipal.TButton", width=15).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy, style="BotonSecundario.TButton", width=15).pack(side=tk.RIGHT)

        frame.columnconfigure(0, weight=1)
        ventana.bind('<Return>', lambda e: guardar())
        ventana.bind('<Escape>', lambda e: ventana.destroy())

    def editar_oficina(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una oficina para editar")
            return

        nombre_actual = self.tree.item(seleccion[0])['values'][0]

        ventana = tk.Toplevel(self.parent)
        ventana.title("Editar Oficina")
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
                oficinas = self.crud.leer_oficinas()
                for oficina in oficinas:
                    if oficina["nombre"].lower() == nuevo_nombre.lower():
                        messagebox.showerror("Error", f"Ya existe una oficina con el nombre '{nuevo_nombre}'")
                        return

                if self.crud.actualizar_oficina(nombre_actual, nuevo_nombre):
                    self.cargar_oficinas()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar la oficina")
            else:
                messagebox.showerror("Error", "Ingrese un nombre válido y diferente")

        ttk.Button(frame_botones, text="Guardar", command=guardar, style="BotonPrincipal.TButton", width=15).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy, style="BotonSecundario.TButton", width=15).pack(side=tk.RIGHT)

        frame.columnconfigure(0, weight=1)
        ventana.bind('<Return>', lambda e: guardar())
        ventana.bind('<Escape>', lambda e: ventana.destroy())

    def eliminar_oficina(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una oficina para eliminar")
            return

        nombre = self.tree.item(seleccion[0])['values'][0]

        respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro que desea eliminar la oficina '{nombre}'?")
        if respuesta:
            if self.crud.eliminar_oficina(nombre):
                self.cargar_oficinas()
                messagebox.showinfo("Éxito", f"Oficina '{nombre}' eliminada")
            else:
                messagebox.showerror("Error", "No se pudo eliminar la oficina")
