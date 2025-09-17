import tkinter as tk
from tkinter import ttk

class EstilosApp:
    def __init__(self):
        # Configurar estilos
        self.configurar_estilos()
    
    def configurar_estilos(self):
        # Crear un objeto Style
        style = ttk.Style()
        
        # Configurar el tema (puedes probar: 'clam', 'alt', 'default', 'classic')
        style.theme_use('clam')
        
        # Definir colores principales
        self.COLOR_PRIMARIO = "#2E86AB"      # Azul principal
        self.COLOR_SECUNDARIO = "#A23B72"    # Rosa/morado
        self.COLOR_ACENTO = "#F18F01"        # Naranja/amarillo
        self.COLOR_FONDO = "#F5F5F5"         # Gris claro
        self.COLOR_TEXTO = "#333333"         # Gris oscuro
        self.COLOR_EXITO = "#4CAF50"         # Verde
        self.COLOR_ERROR = "#F44336"         # Rojo
        self.COLOR_ADVERTENCIA = "#FF9800"   # Naranja
        
        # Configurar estilos para botones principales
        style.configure('BotonPrincipal.TButton',
                       background=self.COLOR_PRIMARIO,
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(10, 8),
                       font=('Arial', 10, 'bold'))
        
        style.map('BotonPrincipal.TButton',
                  background=[('active', self.COLOR_SECUNDARIO),
                             ('pressed', self.COLOR_ACENTO)])
        
        # Configurar estilos para botones secundarios
        style.configure('BotonSecundario.TButton',
                       background='white',
                       foreground=self.COLOR_PRIMARIO,
                       borderwidth=1,
                       relief='solid',
                       focuscolor='none',
                       padding=(10, 8),
                       font=('Arial', 10))
        
        style.map('BotonSecundario.TButton',
                  background=[('active', self.COLOR_FONDO),
                             ('pressed', '#E0E0E0')])
        
        # Configurar estilos para botones de acción (Agregar, Editar, Eliminar)
        style.configure('BotonAccion.TButton',
                       padding=(8, 6),
                       font=('Arial', 9),
                       focuscolor='none')
        
        style.configure('BotonAgregar.TButton',
                       parent='BotonAccion.TButton',
                       background=self.COLOR_EXITO,
                       foreground='white')
        
        style.configure('BotonEditar.TButton',
                       parent='BotonAccion.TButton',
                       background='#2196F3',
                       foreground='white')
        
        style.configure('BotonEliminar.TButton',
                       parent='BotonAccion.TButton',
                       background=self.COLOR_ERROR,
                       foreground='white')
        
        # Configurar estilos para etiquetas de título
        style.configure('Titulo.TLabel',
                       font=('Arial', 18, 'bold'),
                       foreground=self.COLOR_PRIMARIO)
        
        # Configurar estilos para etiquetas de subtítulo
        style.configure('Subtitulo.TLabel',
                       font=('Arial', 14, 'bold'),
                       foreground=self.COLOR_SECUNDARIO)
        
        # Configurar estilos para etiquetas informativas
        style.configure('Info.TLabel',
                       font=('Arial', 10),
                       foreground=self.COLOR_TEXTO)
        
        # Configurar estilos para Treeview
        style.configure('Treeview',
                       background='white',
                       foreground=self.COLOR_TEXTO,
                       rowheight=25,
                       fieldbackground='white',
                       borderwidth=1,
                       relief='solid')
        
        style.configure('Treeview.Heading',
                       background=self.COLOR_PRIMARIO,
                       foreground='white',
                       relief='flat',
                       font=('Arial', 10, 'bold'))
        
        style.map('Treeview.Heading',
                  background=[('active', self.COLOR_SECUNDARIO)])
        
        # Configurar estilos para frames
        style.configure('Frame.TFrame',
                       background=self.COLOR_FONDO)
        
        # Configurar estilos para etiquetas de campos
        style.configure('Campo.TLabel',
                       font=('Arial', 10),
                       foreground=self.COLOR_TEXTO)
        
        # Configurar estilos para entradas de texto
        style.configure('Entrada.TEntry',
                       font=('Arial', 10),
                       padding=(5, 5),
                       borderwidth=1,
                       relief='solid')
        
        # Configurar estilos para etiquetas de mensaje vacío
        style.configure('Vacio.TLabel',
                       font=('Arial', 12, 'italic'),
                       foreground='gray')
        
        # Configurar estilos para etiquetas de contador
        style.configure('Contador.TLabel',
                       font=('Arial', 9),
                       foreground='gray')