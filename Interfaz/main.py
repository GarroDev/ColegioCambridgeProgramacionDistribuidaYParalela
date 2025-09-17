from Interfaz.form_personas import FormPersonas
from Almacenamiento.db_setup import inicializar_bd

inicializar_bd()

import sys
import os
# Agregar el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from tkinter import ttk, messagebox
from Servicios.crud import CRUD  # Importación correcta con S mayúscula
from Interfaz.estilos import EstilosApp  # Importar los estilos

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Colegio Cambridge - Sistema de Gestion")
        self.root.geometry("900x700")
        
        # Configurar color de fondo
        self.root.configure(bg="#F5F5F5")
        
        # Inicializar estilos
        self.estilos = EstilosApp()
        
        # Crear el CRUD
        self.crud = CRUD()
        
        # Crear el menú
        self.crear_menu()
        
        # Crear el marco principal
        self.marco_principal = ttk.Frame(self.root, style="Frame.TFrame")
        self.marco_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Mostrar mensaje de bienvenida
        self.mostrar_bienvenida()
    
    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Gestión
        gestion_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Gestión", menu=gestion_menu)
        gestion_menu.add_command(label="Áreas", command=self.abrir_form_areas)
        gestion_menu.add_command(label="Oficinas", command=self.abrir_form_oficinas)
        gestion_menu.add_command(label="Personas", command=self.abrir_form_personas)
        
        # Menú Reportes
        reportes_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reportes", menu=reportes_menu)
        reportes_menu.add_command(label="Áreas y Empleados", command=self.abrir_reportes)
    
    def mostrar_bienvenida(self):
        for widget in self.marco_principal.winfo_children():
            widget.destroy()
        
        # Frame para el contenido de bienvenida
        frame_bienvenida = ttk.Frame(self.marco_principal, style="Frame.TFrame")
        frame_bienvenida.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        titulo = ttk.Label(
            frame_bienvenida,
            text="Sistema de Gestion",
            style="Titulo.TLabel"
        )
        titulo.pack(pady=(20, 10))
        
        # Subtítulo
        subtitulo = ttk.Label(
            frame_bienvenida,
            text="Colegio Cambridge",
            style="Subtitulo.TLabel"
        )
        subtitulo.pack(pady=(0, 30))
        
        # Instrucciones
        instrucciones = ttk.Label(
            frame_bienvenida,
            text="Use el menú superior para gestionar áreas, oficinas y personas.",
            style="Info.TLabel",
            wraplength=400
        )
        instrucciones.pack(pady=(0, 40))
        
        # Frame para botones de acceso rápido
        frame_botones = ttk.Frame(frame_bienvenida, style="Frame.TFrame")
        frame_botones.pack()
        
        # Botones de acceso rápido
        btn_areas = ttk.Button(
            frame_botones,
            text="Gestionar Áreas",
            style="BotonSecundario.TButton",
            command=self.abrir_form_areas,
            width=20
        )
        btn_areas.grid(row=0, column=0, padx=10, pady=5)
        
        btn_oficinas = ttk.Button(
            frame_botones,
            text="Gestionar Oficinas",
            style="BotonSecundario.TButton",
            command=self.abrir_form_oficinas,
            width=20
        )
        btn_oficinas.grid(row=0, column=1, padx=10, pady=5)
        
        btn_personas = ttk.Button(
            frame_botones,
            text="Gestionar Personas",
            style="BotonSecundario.TButton",
            command=self.abrir_form_personas,
            width=20
        )
        btn_personas.grid(row=1, column=0, padx=10, pady=5)
        
        btn_reportes = ttk.Button(
            frame_botones,
            text="Ver Reportes",
            style="BotonSecundario.TButton",
            command=self.abrir_reportes,
            width=20
        )
        btn_reportes.grid(row=1, column=1, padx=10, pady=5)
            
    def mostrar_mensaje(self, texto, tipo="info"):
        """Muestra un mensaje en la interfaz"""
        for widget in self.marco_principal.winfo_children():
            widget.destroy()
        
        # Determinar el color según el tipo
        if tipo == "error":
            color = self.estilos.COLOR_ERROR
            icono = "❌"
        elif tipo == "exito":
            color = self.estilos.COLOR_EXITO
            icono = "✅"
        else:
            color = self.estilos.COLOR_PRIMARIO
            icono = "ℹ️"
        
        # Frame para el mensaje
        frame_mensaje = ttk.Frame(self.marco_principal, style="Frame.TFrame")
        frame_mensaje.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Icono y mensaje
        frame_contenido = ttk.Frame(frame_mensaje, style="Frame.TFrame")
        frame_contenido.pack(expand=True)
        
        ttk.Label(
            frame_contenido,
            text=icono,
            font=("Arial", 24),
            foreground=color
        ).pack(pady=(0, 10))
        
        mensaje = ttk.Label(
            frame_contenido,
            text=texto,
            style="Info.TLabel",
            wraplength=400
        )
        mensaje.pack()
        
        # Botón para continuar
        ttk.Button(
            frame_contenido,
            text="Continuar",
            style="BotonPrincipal.TButton",
            command=self.mostrar_bienvenida
        ).pack(pady=(20, 0))
    
    def abrir_form_areas(self):
        try:
            from Interfaz.form_areas import FormAreas
            FormAreas(self.marco_principal, self.crud, self.mostrar_bienvenida, self.estilos)
        except Exception as e:
            self.mostrar_mensaje(f"Error al abrir formulario de áreas: {str(e)}", "error")
    
    def abrir_form_oficinas(self):
        try:
            from Interfaz.form_oficinas import FormOficinas
            FormOficinas(self.marco_principal, self.crud, self.mostrar_bienvenida, self.estilos)
        except Exception as e:
            self.mostrar_mensaje(f"Error al abrir formulario de oficinas: {str(e)}", "error")
    
    def abrir_form_personas(self):
        try:
            from Interfaz.form_personas import FormPersonas
            FormPersonas(self.marco_principal, self.crud, self.mostrar_bienvenida, self.estilos)
        except Exception as e:
            self.mostrar_mensaje(f"Error al abrir formulario de personas: {str(e)}", "error")
    
    def abrir_reportes(self):
        try:
            from Interfaz.reportes_vista import ReportesVista
            ReportesVista(self.marco_principal, self.crud, self.mostrar_bienvenida, self.estilos)
        except Exception as e:
            self.mostrar_mensaje(f"Error al abrir reportes: {str(e)}", "error")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()