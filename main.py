"""
Biomedical Digital Signal Processing
Aplicación de escritorio para navegar y estudiar el curso de Procesamiento Digital de Señales Biomédicas
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
import os
import sys
import subprocess
import threading
import io
import contextlib
from pathlib import Path
import webbrowser
import tempfile
import shutil
from typing import Dict, List, Tuple
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import numpy as np

# Importar utilidades locales
try:
    from utils import get_resource_path, open_file_with_default_app, check_python_requirements
except ImportError:
    # Fallback si utils.py no está disponible
    def get_resource_path(relative_path):
        return relative_path
    
    def open_file_with_default_app(file_path):
        if sys.platform == "win32":
            os.startfile(file_path)
        elif sys.platform == "darwin":
            subprocess.run(["open", file_path])
        else:
            subprocess.run(["xdg-open", file_path])
    
    def check_python_requirements():
        return []

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")  # "dark" o "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class BiomedicaDSPApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Biomedical Digital Signal Processing")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Variables
        self.current_pdf_path = None
        self.current_py_path = None
        self.pdf_viewer_process = None
        self.selected_button = None  # Para trackear el botón seleccionado
        
        # Variables para el visor de PDF integrado
        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0
        self.pdf_images = []  # Cache de imágenes de páginas
        self.zoom_level = 1.0
        self.is_fullscreen = False
        
        # Obtener el directorio base del proyecto
        if getattr(sys, 'frozen', False):
            # Si estamos ejecutando desde un ejecutable de PyInstaller
            self.base_dir = Path(sys._MEIPASS)
        else:
            # Si estamos ejecutando desde el script Python
            self.base_dir = Path(__file__).parent
        
        # Configurar icono si existe
        icon_path = self.base_dir / "icon.ico"
        if icon_path.exists():
            self.root.iconbitmap(str(icon_path))
        
        self.setup_ui()
        self.load_course_structure()
        self.setup_keyboard_shortcuts()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame superior - Título y navegación
        self.header_frame = ctk.CTkFrame(self.main_frame)
        self.header_frame.pack(fill="x", padx=10, pady=10)
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="🧠 Biomedical Digital Signal Processing",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=15)
        
        # Indicador de clase seleccionada
        self.selected_class_frame = ctk.CTkFrame(self.header_frame)
        self.selected_class_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        self.selected_class_label = ctk.CTkLabel(
            self.selected_class_frame,
            text="📖 Selecciona una clase del curso para comenzar",
            font=ctk.CTkFont(size=14),
            text_color=("#1f538d", "#4a9eff")  # Azul en modo oscuro y claro
        )
        self.selected_class_label.pack(pady=10)
        
        # Frame de contenido principal
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Navegación
        self.nav_frame = ctk.CTkFrame(self.content_frame)
        self.nav_frame.pack(side="left", fill="y", padx=(10, 5), pady=10)
        
        # Título de navegación
        nav_title = ctk.CTkLabel(
            self.nav_frame,
            text="📚 Unidades del Curso",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        nav_title.pack(pady=10)
        
        # Scrollable frame para navegación
        self.nav_scroll = ctk.CTkScrollableFrame(
            self.nav_frame,
            width=300,
            height=600
        )
        self.nav_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Panel derecho - Contenido
        self.right_panel = ctk.CTkFrame(self.content_frame)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        # Tabs para PDF y Código
        self.tabview = ctk.CTkTabview(self.right_panel)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab PDF
        self.pdf_tab = self.tabview.add("📄 Material PDF")
        self.setup_pdf_tab()
        
        # Tab Código
        self.code_tab = self.tabview.add("💻 Código Python")
        self.setup_code_tab()
        
        # Tab Ejecución
        self.exec_tab = self.tabview.add("▶️ Ejecutar Código")
        self.setup_execution_tab()
        
    def setup_pdf_tab(self):
        """Configurar el tab de visualización de PDF"""
        
        # Frame de controles PDF
        pdf_controls = ctk.CTkFrame(self.pdf_tab)
        pdf_controls.pack(fill="x", padx=10, pady=10)
        
        # Panel izquierdo de controles
        left_controls = ctk.CTkFrame(pdf_controls)
        left_controls.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.pdf_label = ctk.CTkLabel(
            left_controls,
            text="Selecciona una clase para ver el material PDF",
            font=ctk.CTkFont(size=14)
        )
        self.pdf_label.pack(side="left", padx=10, pady=10)
        
        # Panel derecho de controles
        right_controls = ctk.CTkFrame(pdf_controls)
        right_controls.pack(side="right", padx=(5, 0))
        
        # Controles de navegación
        nav_frame = ctk.CTkFrame(right_controls)
        nav_frame.pack(side="left", padx=5, pady=5)
        
        self.prev_page_btn = ctk.CTkButton(
            nav_frame,
            text="◀️",
            command=self.prev_page,
            state="disabled",
            width=40
        )
        self.prev_page_btn.pack(side="left", padx=2, pady=5)
        
        self.page_label = ctk.CTkLabel(
            nav_frame,
            text="0/0",
            font=ctk.CTkFont(size=12),
            width=60
        )
        self.page_label.pack(side="left", padx=5, pady=5)
        
        self.next_page_btn = ctk.CTkButton(
            nav_frame,
            text="▶️",
            command=self.next_page,
            state="disabled",
            width=40
        )
        self.next_page_btn.pack(side="left", padx=2, pady=5)
        
        # Controles de zoom
        zoom_frame = ctk.CTkFrame(right_controls)
        zoom_frame.pack(side="left", padx=5, pady=5)
        
        self.zoom_out_btn = ctk.CTkButton(
            zoom_frame,
            text="🔍-",
            command=self.zoom_out,
            state="disabled",
            width=40
        )
        self.zoom_out_btn.pack(side="left", padx=2, pady=5)
        
        self.zoom_label = ctk.CTkLabel(
            zoom_frame,
            text="100%",
            font=ctk.CTkFont(size=12),
            width=50
        )
        self.zoom_label.pack(side="left", padx=5, pady=5)
        
        self.zoom_in_btn = ctk.CTkButton(
            zoom_frame,
            text="🔍+",
            command=self.zoom_in,
            state="disabled",
            width=40
        )
        self.zoom_in_btn.pack(side="left", padx=2, pady=5)
        
        # Botón para ajustar a ventana
        self.fit_window_btn = ctk.CTkButton(
            zoom_frame,
            text="📐",
            command=self.fit_to_window,
            state="disabled",
            width=40
        )
        self.fit_window_btn.pack(side="left", padx=2, pady=5)
        
        # Botón para pantalla completa
        self.fullscreen_btn = ctk.CTkButton(
            right_controls,
            text="🖥️ Pantalla Completa",
            command=self.toggle_fullscreen,
            state="disabled",
            width=120
        )
        self.fullscreen_btn.pack(side="left", padx=5, pady=5)
        
        # Botón para abrir en externo
        self.open_pdf_btn = ctk.CTkButton(
            right_controls,
            text="🔗 Externo",
            command=self.open_pdf_external,
            state="disabled",
            width=80
        )
        self.open_pdf_btn.pack(side="left", padx=5, pady=5)
        
        # Frame principal para el PDF con scrollbars
        self.pdf_main_frame = ctk.CTkFrame(self.pdf_tab)
        self.pdf_main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas con scrollbars para el PDF
        canvas_frame = tk.Frame(self.pdf_main_frame, bg="#2b2b2b")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear canvas y scrollbars
        self.pdf_canvas = tk.Canvas(
            canvas_frame,
            bg="#1e1e1e",
            highlightthickness=0
        )
        
        # Configurar eventos del mouse en el canvas
        self.pdf_canvas.bind("<Button-1>", self.on_pdf_click)
        self.pdf_canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.pdf_canvas.bind("<Button-4>", self.on_mouse_wheel)  # Linux scroll up
        self.pdf_canvas.bind("<Button-5>", self.on_mouse_wheel)  # Linux scroll down
        
        v_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.pdf_canvas.yview)
        h_scrollbar = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.pdf_canvas.xview)
        
        self.pdf_canvas.configure(
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        # Pack scrollbars y canvas
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        self.pdf_canvas.pack(fill="both", expand=True)
        
        # Label para mostrar información cuando no hay PDF
        self.pdf_info_label = ctk.CTkLabel(
            self.pdf_main_frame,
            text="📖 Selecciona una clase para ver el material PDF aquí",
            font=ctk.CTkFont(size=16),
            text_color=("gray50", "gray70")
        )
        self.pdf_info_label.pack(expand=True)
        
    def setup_code_tab(self):
        """Configurar el tab de código Python"""
        
        # Frame de controles de código
        code_controls = ctk.CTkFrame(self.code_tab)
        code_controls.pack(fill="x", padx=10, pady=10)
        
        self.code_label = ctk.CTkLabel(
            code_controls,
            text="Selecciona una clase para ver el código",
            font=ctk.CTkFont(size=14)
        )
        self.code_label.pack(side="left", padx=10, pady=10)
        
        self.save_code_btn = ctk.CTkButton(
            code_controls,
            text="💾 Guardar Cambios",
            command=self.save_code_changes,
            state="disabled"
        )
        self.save_code_btn.pack(side="right", padx=10, pady=10)
        
        # Text widget para el código
        code_frame = ctk.CTkFrame(self.code_tab)
        code_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear un frame para el text widget con scrollbar
        text_frame = tk.Frame(code_frame, bg="#2b2b2b")
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Text widget con scrollbar
        self.code_text = tk.Text(
            text_frame,
            wrap="none",
            font=("Consolas", 11),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff",
            selectbackground="#264f78",
            relief="flat"
        )
        
        # Scrollbars
        v_scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.code_text.yview)
        h_scrollbar = tk.Scrollbar(text_frame, orient="horizontal", command=self.code_text.xview)
        
        self.code_text.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars y text widget
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        self.code_text.pack(fill="both", expand=True)
        
    def setup_execution_tab(self):
        """Configurar el tab de ejecución de código"""
        
        # Frame de controles de ejecución
        exec_controls = ctk.CTkFrame(self.exec_tab)
        exec_controls.pack(fill="x", padx=10, pady=10)
        
        self.run_btn = ctk.CTkButton(
            exec_controls,
            text="▶️ Ejecutar Código",
            command=self.execute_code,
            state="disabled",
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.run_btn.pack(side="left", padx=10, pady=10)
        
        self.clear_output_btn = ctk.CTkButton(
            exec_controls,
            text="🗑️ Limpiar Salida",
            command=self.clear_output,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        self.clear_output_btn.pack(side="left", padx=5, pady=10)
        
        self.stop_btn = ctk.CTkButton(
            exec_controls,
            text="⏹️ Detener",
            command=self.stop_execution,
            state="disabled",
            fg_color="#ffc107",
            hover_color="#e0a800"
        )
        self.stop_btn.pack(side="left", padx=5, pady=10)
        
        # Frame para la salida
        output_frame = ctk.CTkFrame(self.exec_tab)
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        output_label = ctk.CTkLabel(
            output_frame,
            text="📊 Salida del Código:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        output_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Text widget para la salida
        output_text_frame = tk.Frame(output_frame, bg="#2b2b2b")
        output_text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.output_text = tk.Text(
            output_text_frame,
            wrap="word",
            font=("Consolas", 10),
            bg="#0d1117",
            fg="#c9d1d9",
            insertbackground="#ffffff",
            state="disabled",
            relief="flat"
        )
        
        output_scrollbar = tk.Scrollbar(output_text_frame, orient="vertical", command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=output_scrollbar.set)
        
        output_scrollbar.pack(side="right", fill="y")
        self.output_text.pack(fill="both", expand=True)
        
    def load_course_structure(self):
        """Cargar la estructura del curso desde los directorios"""
        
        units = []
        
        # Buscar todas las unidades
        for item in self.base_dir.iterdir():
            if item.is_dir() and item.name.startswith("Unidad"):
                unit_data = {
                    "name": item.name,
                    "path": item,
                    "classes": []
                }
                
                # Buscar clases en cada unidad
                pdf_files = list(item.glob("*.pdf"))
                py_files = list(item.glob("*.py"))
                
                # Agrupar archivos por número de clase
                classes = {}
                
                # Procesar PDFs
                for pdf_file in pdf_files:
                    class_key = self._extract_class_number(pdf_file.name)
                    if class_key:
                        if class_key not in classes:
                            classes[class_key] = {"pdf": None, "py": None, "display_name": ""}
                        classes[class_key]["pdf"] = pdf_file
                        # Usar el nombre del PDF para el display name
                        if not classes[class_key]["display_name"]:
                            classes[class_key]["display_name"] = self.extract_class_name(pdf_file.name)
                
                # Procesar archivos Python
                for py_file in py_files:
                    class_key = self._extract_class_number(py_file.name)
                    if class_key:
                        if class_key not in classes:
                            classes[class_key] = {"pdf": None, "py": None, "display_name": ""}
                        classes[class_key]["py"] = py_file
                        # Si no hay display name del PDF, usar el del Python
                        if not classes[class_key]["display_name"]:
                            classes[class_key]["display_name"] = self.extract_class_name(py_file.name)
                
                # Convertir a lista ordenada por número de clase
                sorted_class_keys = sorted(classes.keys(), key=lambda x: int(x) if x.isdigit() else 999)
                
                for class_key in sorted_class_keys:
                    class_info = classes[class_key]
                    unit_data["classes"].append({
                        "name": class_info["display_name"],
                        "pdf_path": class_info["pdf"],
                        "py_path": class_info["py"]
                    })
                
                units.append(unit_data)
        
        # Ordenar unidades
        units.sort(key=lambda x: x["name"])
        
        # Crear navegación
        self.create_navigation(units)
    
    def _extract_class_number(self, filename):
        """Extraer solo el número de clase del nombre del archivo"""
        import re
        
        # Buscar patrón: "Clase" seguido de número
        match = re.search(r'Clase\s*(\d+)', filename, re.IGNORECASE)
        if match:
            return match.group(1).zfill(2)  # Normalizar con ceros (01, 02, etc.)
        
        return None
        
    def extract_class_name(self, filename):
        """Extraer el nombre de la clase desde el nombre del archivo"""
        # Remover extensión
        name = Path(filename).stem
        
        # Buscar patrón "Clase XX"
        if name.startswith("Clase"):
            # Usar regex para extraer el número de clase más robustamente
            import re
            
            # Buscar patrón: "Clase" seguido de espacio/guión/etc, luego número
            match = re.match(r'Clase\s*(\d+)', name, re.IGNORECASE)
            if match:
                class_num = match.group(1)
                
                # Extraer el tema principal del nombre del archivo
                # Buscar después del número, puede haber varios separadores
                remaining_match = re.search(r'Clase\s*\d+[\s\-\.]*(.+)', name, re.IGNORECASE)
                if remaining_match:
                    topic = remaining_match.group(1).strip()
                    # Limpiar caracteres especiales al inicio
                    topic = re.sub(r'^[\s\-\.]+', '', topic)
                    
                    # Si el topic está vacío o es muy corto, usar nombres más descriptivos
                    if len(topic) < 3:
                        topic = self._get_default_topic(class_num)
                    
                    return f"Clase {class_num}: {topic}"
                else:
                    # Si no hay tema, usar un tema por defecto basado en el número
                    topic = self._get_default_topic(class_num)
                    return f"Clase {class_num}: {topic}"
        
        return name
    
    def _get_default_topic(self, class_num):
        """Obtener tema por defecto basado en el número de clase"""
        # Mapeo de números de clase a temas generales
        default_topics = {
            "01": "Señales Analógicas y Muestreo",
            "02": "Muestreo y Aliasing", 
            "03": "Espectro de Señales",
            "04": "Filtros Antialias",
            "05": "Reconstrucción de Señales",
            "06": "Cuantización",
            "07": "Sistemas LTI",
            "08": "Respuesta al Impulso",
            "09": "Causalidad y Estabilidad",
            "10": "Convolución",
            "11": "Transformada Z",
            "12": "DFT",
            "13": "Filtros FIR",
            "14": "Filtros IIR"
        }
        
        # Normalizar el número de clase (agregar cero inicial si es necesario)
        normalized_num = class_num.zfill(2)
        
        return default_topics.get(normalized_num, f"Tema {class_num}")
    
    def create_navigation(self, units):
        """Crear la navegación por unidades y clases"""
        
        for unit in units:
            # Frame para cada unidad
            unit_frame = ctk.CTkFrame(self.nav_scroll)
            unit_frame.pack(fill="x", padx=5, pady=5)
            
            # Título de la unidad
            unit_label = ctk.CTkLabel(
                unit_frame,
                text=unit["name"],
                font=ctk.CTkFont(size=14, weight="bold"),
                wraplength=280
            )
            unit_label.pack(pady=10)
            
            # Clases de la unidad
            for class_data in unit["classes"]:
                class_btn = ctk.CTkButton(
                    unit_frame,
                    text=class_data["name"],
                    command=lambda cd=class_data, btn=None: self.load_class(cd, btn),
                    width=260,
                    height=40,
                    font=ctk.CTkFont(size=11),
                    anchor="w"
                )
                class_btn.pack(pady=2, padx=10)
                
                # Actualizar la referencia del botón en el comando
                class_btn.configure(command=lambda cd=class_data, btn=class_btn: self.load_class(cd, btn))
    
    def load_class(self, class_data, selected_btn=None):
        """Cargar una clase específica"""
        
        # Resetear el botón anteriormente seleccionado
        if self.selected_button:
            self.selected_button.configure(fg_color=("gray75", "gray25"))  # Color normal
        
        # Destacar el botón actual
        if selected_btn:
            selected_btn.configure(fg_color=("#1f538d", "#4a9eff"))  # Color destacado
            self.selected_button = selected_btn
        
        self.current_pdf_path = class_data.get("pdf_path")
        self.current_py_path = class_data.get("py_path")
        
        # Actualizar indicador de clase seleccionada
        class_name = class_data.get("name", "Clase sin nombre")
        self.selected_class_label.configure(
            text=f"📚 Clase Actual: {class_name}",
            text_color=("#1f538d", "#4a9eff")
        )
        
        # Actualizar labels de PDF
        if self.current_pdf_path:
            self.pdf_label.configure(text=f"📄 {self.current_pdf_path.name}")
            self.open_pdf_btn.configure(state="normal")
            self.load_pdf_document()
        else:
            self.pdf_label.configure(text="❌ No hay PDF disponible para esta clase")
            self.open_pdf_btn.configure(state="disabled")
            self.close_pdf_document()
        
        # Actualizar labels de código
        if self.current_py_path:
            self.code_label.configure(text=f"💻 {self.current_py_path.name}")
            self.load_code_content()
            self.save_code_btn.configure(state="normal")
            self.run_btn.configure(state="normal")
        else:
            self.code_label.configure(text="❌ No hay código disponible para esta clase")
            self.code_text.delete(1.0, tk.END)
            self.save_code_btn.configure(state="disabled")
            self.run_btn.configure(state="disabled")
        
        # Limpiar salida anterior al cambiar de clase
        self.clear_output()
    
    def load_code_content(self):
        """Cargar el contenido del archivo Python"""
        
        if self.current_py_path and self.current_py_path.exists():
            try:
                with open(self.current_py_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                self.code_text.delete(1.0, tk.END)
                self.code_text.insert(1.0, content)
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
    
    def save_code_changes(self):
        """Guardar cambios en el código"""
        
        if not self.current_py_path:
            return
        
        try:
            content = self.code_text.get(1.0, tk.END + "-1c")
            
            with open(self.current_py_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            messagebox.showinfo("Éxito", "Código guardado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")
    
    def open_pdf_external(self):
        """Abrir PDF en el visor externo"""
        
        if not self.current_pdf_path or not self.current_pdf_path.exists():
            messagebox.showerror("Error", "No hay PDF disponible")
            return
        
        try:
            success = open_file_with_default_app(str(self.current_pdf_path))
            if not success:
                messagebox.showerror("Error", "No se pudo abrir el PDF")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el PDF: {str(e)}")
    
    def load_pdf_document(self):
        """Cargar documento PDF en el visor integrado"""
        
        if not self.current_pdf_path or not self.current_pdf_path.exists():
            return
        
        try:
            # Mostrar indicador de carga
            self.show_loading_message("Cargando PDF...")
            
            # Cerrar documento anterior si existe
            self.close_pdf_document()
            
            # Abrir nuevo documento
            self.pdf_document = fitz.open(str(self.current_pdf_path))
            self.total_pages = len(self.pdf_document)
            self.current_page = 0
            self.zoom_level = 1.0
            
            # Habilitar controles
            self.prev_page_btn.configure(state="normal")
            self.next_page_btn.configure(state="normal")
            self.zoom_in_btn.configure(state="normal")
            self.zoom_out_btn.configure(state="normal")
            self.fit_window_btn.configure(state="normal")
            self.fullscreen_btn.configure(state="normal")
            
            # Ocultar el label de información
            self.pdf_info_label.pack_forget()
            
            # Mostrar primera página con ajuste automático
            self.root.after(100, self.fit_to_window)  # Delay para que el canvas tenga dimensiones
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el PDF: {str(e)}")
            self.close_pdf_document()
    
    def show_loading_message(self, message):
        """Mostrar mensaje de carga en el canvas"""
        
        self.pdf_canvas.delete("all")
        self.pdf_canvas.create_text(
            200, 150,
            text=message,
            fill="white",
            font=("Arial", 14),
            anchor="center"
        )
    
    def close_pdf_document(self):
        """Cerrar documento PDF actual"""
        
        # Salir de pantalla completa si está activa
        if self.is_fullscreen:
            self.exit_fullscreen()
        
        if self.pdf_document:
            self.pdf_document.close()
            self.pdf_document = None
        
        self.current_page = 0
        self.total_pages = 0
        self.pdf_images.clear()
        
        # Limpiar canvas
        self.pdf_canvas.delete("all")
        
        # Deshabilitar controles
        self.prev_page_btn.configure(state="disabled")
        self.next_page_btn.configure(state="disabled")
        self.zoom_in_btn.configure(state="disabled")
        self.zoom_out_btn.configure(state="disabled")
        self.fit_window_btn.configure(state="disabled")
        self.fullscreen_btn.configure(state="disabled")
        
        # Actualizar labels
        self.page_label.configure(text="0/0")
        self.zoom_label.configure(text="100%")
        
        # Mostrar el label de información
        self.pdf_info_label.pack(expand=True)
    
    def display_current_page(self):
        """Mostrar la página actual del PDF"""
        
        if not self.pdf_document or self.current_page >= self.total_pages:
            return
        
        try:
            # Obtener la página
            page = self.pdf_document[self.current_page]
            
            # Crear matriz de transformación para el zoom
            mat = fitz.Matrix(self.zoom_level, self.zoom_level)
            
            # Renderizar página como imagen
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("ppm")
            
            # Convertir a PIL Image y luego a PhotoImage
            pil_image = Image.open(io.BytesIO(img_data))
            photo = ImageTk.PhotoImage(pil_image)
            
            # Determinar qué canvas usar
            if self.is_fullscreen and hasattr(self, 'pdf_canvas_fs'):
                current_canvas = self.pdf_canvas_fs
            else:
                current_canvas = self.pdf_canvas
            
            # Obtener dimensiones del canvas y la imagen
            current_canvas.update_idletasks()
            canvas_width = current_canvas.winfo_width()
            canvas_height = current_canvas.winfo_height()
            img_width = photo.width()
            img_height = photo.height()
            
            # Calcular posición para centrar la imagen
            if img_width < canvas_width:
                x_pos = (canvas_width - img_width) // 2
            else:
                x_pos = 0
                
            if img_height < canvas_height:
                y_pos = (canvas_height - img_height) // 2
            else:
                y_pos = 0
            
            # Limpiar canvas y mostrar imagen
            current_canvas.delete("all")
            current_canvas.create_image(x_pos, y_pos, anchor="nw", image=photo)
            
            # Guardar referencia de la imagen para evitar garbage collection
            current_canvas.image = photo
            
            # Configurar región de scroll basada en la imagen completa
            scroll_region = (0, 0, max(img_width, canvas_width), max(img_height, canvas_height))
            current_canvas.configure(scrollregion=scroll_region)
            
            # Actualizar labels de página (en ambos modos)
            page_text = f"{self.current_page + 1}/{self.total_pages}"
            self.page_label.configure(text=page_text)
            
            # Actualizar label en pantalla completa si existe
            if self.is_fullscreen and hasattr(self, 'page_label_fs'):
                self.page_label_fs.configure(text=page_text)
            
        except Exception as e:
            print(f"Error al mostrar página: {e}")  # Log en consola en lugar de messagebox
            
            # Determinar qué canvas usar para mostrar error
            if self.is_fullscreen and hasattr(self, 'pdf_canvas_fs'):
                current_canvas = self.pdf_canvas_fs
            else:
                current_canvas = self.pdf_canvas
                
            # Intentar mostrar un mensaje de error en el canvas
            current_canvas.delete("all")
            current_canvas.create_text(
                200, 100, 
                text=f"Error al cargar página {self.current_page + 1}\n{str(e)[:100]}...",
                fill="red",
                font=("Arial", 12),
                width=400
            )
    
    def prev_page(self):
        """Ir a la página anterior"""
        
        if self.current_page > 0:
            self.current_page -= 1
            self.display_current_page()
    
    def next_page(self):
        """Ir a la página siguiente"""
        
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_current_page()
    
    def zoom_in(self):
        """Aumentar zoom"""
        
        if self.zoom_level < 5.0:  # Límite máximo de zoom aumentado
            self.zoom_level += 0.25  # Incrementos más pequeños
            self.zoom_level = round(self.zoom_level, 2)
            self.update_zoom_display()
            self.display_current_page()
    
    def zoom_out(self):
        """Disminuir zoom"""
        
        if self.zoom_level > 0.25:  # Límite mínimo de zoom
            self.zoom_level -= 0.25  # Decrementos más pequeños
            self.zoom_level = round(self.zoom_level, 2)
            self.update_zoom_display()
            self.display_current_page()
    
    def fit_to_window(self):
        """Ajustar zoom para que la página se ajuste a la ventana"""
        
        if not self.pdf_document:
            return
        
        try:
            # Obtener dimensiones de la página
            page = self.pdf_document[self.current_page]
            page_rect = page.rect
            page_width = page_rect.width
            page_height = page_rect.height
            
            # Obtener dimensiones del canvas disponible
            if self.is_fullscreen and hasattr(self, 'pdf_canvas_fs'):
                canvas = self.pdf_canvas_fs
            else:
                canvas = self.pdf_canvas
            
            # Forzar actualización del canvas para obtener dimensiones reales
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            
            # Si las dimensiones son muy pequeñas, usar valores por defecto
            if canvas_width < 100:
                canvas_width = 800
            if canvas_height < 100:
                canvas_height = 600
            
            # Calcular zoom para ajustar al ancho y alto, tomando el menor
            zoom_width = (canvas_width - 20) / page_width  # 20px de margen
            zoom_height = (canvas_height - 20) / page_height  # 20px de margen
            
            # Usar el zoom más pequeño para que quepa completo
            self.zoom_level = min(zoom_width, zoom_height)
            
            # Limitar el zoom a rangos razonables
            self.zoom_level = max(0.25, min(5.0, self.zoom_level))
            self.zoom_level = round(self.zoom_level, 2)
            
            self.update_zoom_display()
            self.display_current_page()
            
        except Exception as e:
            print(f"Error al ajustar zoom: {e}")
            # Fallback: zoom por defecto
            self.zoom_level = 1.0
            self.update_zoom_display()
            self.display_current_page()
    
    def fit_to_width(self):
        """Ajustar zoom para que la página se ajuste al ancho de la ventana"""
        
        if not self.pdf_document:
            return
        
        try:
            # Obtener dimensiones de la página
            page = self.pdf_document[self.current_page]
            page_rect = page.rect
            page_width = page_rect.width
            
            # Obtener ancho del canvas disponible
            if self.is_fullscreen and hasattr(self, 'pdf_canvas_fs'):
                canvas = self.pdf_canvas_fs
            else:
                canvas = self.pdf_canvas
            
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            
            if canvas_width < 100:
                canvas_width = 800
            
            # Calcular zoom para ajustar al ancho
            self.zoom_level = (canvas_width - 40) / page_width  # 40px de margen
            
            # Limitar el zoom a rangos razonables
            self.zoom_level = max(0.25, min(5.0, self.zoom_level))
            self.zoom_level = round(self.zoom_level, 2)
            
            self.update_zoom_display()
            self.display_current_page()
            
        except Exception as e:
            print(f"Error al ajustar zoom al ancho: {e}")
            self.zoom_level = 1.0
            self.update_zoom_display()
            self.display_current_page()
    
    def update_zoom_display(self):
        """Actualizar el display del zoom"""
        
        zoom_percent = int(self.zoom_level * 100)
        zoom_text = f"{zoom_percent}%"
        
        # Actualizar label principal
        self.zoom_label.configure(text=zoom_text)
        
        # Actualizar label en pantalla completa si existe
        if self.is_fullscreen and hasattr(self, 'zoom_label_fs'):
            self.zoom_label_fs.configure(text=zoom_text)
    
    def execute_code(self):
        """Ejecutar el código Python actual"""
        
        if not self.current_py_path:
            messagebox.showerror("Error", "No hay código para ejecutar")
            return
        
        # Guardar cambios primero
        self.save_code_changes()
        
        # Limpiar salida anterior
        self.clear_output()
        
        # Deshabilitar botón de ejecución
        self.run_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        # Ejecutar en un hilo separado
        self.execution_thread = threading.Thread(target=self._run_code_thread)
        self.execution_thread.daemon = True
        self.execution_thread.start()
    
    def _run_code_thread(self):
        """Ejecutar código en un hilo separado"""
        
        try:
            # Cambiar al directorio del archivo
            original_dir = os.getcwd()
            os.chdir(self.current_py_path.parent)
            
            # Ejecutar el script
            result = subprocess.run(
                [sys.executable, str(self.current_py_path)],
                capture_output=True,
                text=True,
                timeout=60  # Timeout de 60 segundos
            )
            
            # Restaurar directorio original
            os.chdir(original_dir)
            
            # Mostrar resultados en el hilo principal
            self.root.after(0, self._display_execution_result, result)
            
        except subprocess.TimeoutExpired:
            self.root.after(0, self._display_execution_error, "⏰ Ejecución detenida: Timeout de 60 segundos")
        except Exception as e:
            self.root.after(0, self._display_execution_error, f"❌ Error de ejecución: {str(e)}")
        finally:
            # Rehabilitar botones
            self.root.after(0, self._reset_execution_buttons)
    
    def _display_execution_result(self, result):
        """Mostrar resultado de la ejecución"""
        
        self.output_text.configure(state="normal")
        
        if result.stdout:
            self.output_text.insert(tk.END, "📊 Salida:\n")
            self.output_text.insert(tk.END, result.stdout)
            self.output_text.insert(tk.END, "\n")
        
        if result.stderr:
            self.output_text.insert(tk.END, "❌ Errores:\n")
            self.output_text.insert(tk.END, result.stderr)
            self.output_text.insert(tk.END, "\n")
        
        if result.returncode == 0:
            self.output_text.insert(tk.END, "✅ Ejecución completada exitosamente\n")
        else:
            self.output_text.insert(tk.END, f"⚠️ Código de salida: {result.returncode}\n")
        
        self.output_text.configure(state="disabled")
        self.output_text.see(tk.END)
    
    def _display_execution_error(self, error_message):
        """Mostrar error de ejecución"""
        
        self.output_text.configure(state="normal")
        self.output_text.insert(tk.END, error_message + "\n")
        self.output_text.configure(state="disabled")
        self.output_text.see(tk.END)
    
    def _reset_execution_buttons(self):
        """Resetear botones de ejecución"""
        
        self.run_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
    
    def stop_execution(self):
        """Detener la ejecución del código"""
        
        if hasattr(self, 'execution_thread') and self.execution_thread.is_alive():
            # Para simplificar, mostraremos un mensaje
            self.output_text.configure(state="normal")
            self.output_text.insert(tk.END, "\n⏹️ Solicitando detener ejecución...\n")
            self.output_text.configure(state="disabled")
        
        self._reset_execution_buttons()
    
    def clear_output(self):
        """Limpiar la salida de ejecución"""
        
        self.output_text.configure(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.configure(state="disabled")
    
    def setup_keyboard_shortcuts(self):
        """Configurar atajos de teclado para la aplicación"""
        
        # Atajos para navegación del PDF
        self.root.bind('<Left>', lambda e: self.prev_page())
        self.root.bind('<Right>', lambda e: self.next_page())
        self.root.bind('<Up>', lambda e: self.zoom_in())
        self.root.bind('<Down>', lambda e: self.zoom_out())
        
        # Atajos adicionales
        self.root.bind('<Control-o>', lambda e: self.open_pdf_external())
        self.root.bind('<Control-s>', lambda e: self.save_code_changes())
        self.root.bind('<F5>', lambda e: self.execute_code())
        
        # Atajos para navegación por páginas con números
        self.root.bind('<Prior>', lambda e: self.prev_page())  # Page Up
        self.root.bind('<Next>', lambda e: self.next_page())   # Page Down
        
        # Zoom con Ctrl +/-
        self.root.bind('<Control-plus>', lambda e: self.zoom_in())
        self.root.bind('<Control-minus>', lambda e: self.zoom_out())
        self.root.bind('<Control-0>', lambda e: self.reset_zoom())
        self.root.bind('<Control-equal>', lambda e: self.zoom_in())  # Para teclados sin numpad
        
        # Atajos para ajuste de zoom
        self.root.bind('<Control-w>', lambda e: self.fit_to_width())  # Ajustar al ancho
        self.root.bind('<Control-f>', lambda e: self.fit_to_window())  # Ajustar a ventana
        
        # Pantalla completa
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.bind('<Control-Return>', lambda e: self.toggle_fullscreen())
    
    def reset_zoom(self):
        """Resetear zoom al 100%"""
        
        if self.pdf_document:
            self.zoom_level = 1.0
            self.update_zoom_display()
            self.display_current_page()
    
    def on_pdf_click(self, event):
        """Manejar clicks en el PDF (navegación por páginas)"""
        
        if not self.pdf_document:
            return
        
        # Obtener el ancho del canvas
        canvas_width = self.pdf_canvas.winfo_width()
        
        # Si click en la mitad izquierda, ir a página anterior
        if event.x < canvas_width / 2:
            self.prev_page()
        # Si click en la mitad derecha, ir a página siguiente
        else:
            self.next_page()
    
    def on_mouse_wheel(self, event):
        """Manejar scroll del mouse para zoom y navegación"""
        
        if not self.pdf_document:
            return
        
        # Determinar qué canvas usar
        if self.is_fullscreen and hasattr(self, 'pdf_canvas_fs'):
            current_canvas = self.pdf_canvas_fs
        else:
            current_canvas = self.pdf_canvas
        
        # Verificar si Ctrl está presionado para zoom
        if event.state & 0x4:  # Ctrl presionado
            if event.delta > 0 or event.num == 4:  # Scroll up
                self.zoom_in()
            elif event.delta < 0 or event.num == 5:  # Scroll down
                self.zoom_out()
        else:
            # Verificar si Shift está presionado para scroll horizontal
            if event.state & 0x1:  # Shift presionado
                if event.delta > 0 or event.num == 4:  # Scroll left
                    current_canvas.xview_scroll(-1, "units")
                elif event.delta < 0 or event.num == 5:  # Scroll right
                    current_canvas.xview_scroll(1, "units")
            else:
                # Scroll vertical normal
                if event.delta > 0 or event.num == 4:  # Scroll up
                    current_canvas.yview_scroll(-1, "units")
                elif event.delta < 0 or event.num == 5:  # Scroll down
                    current_canvas.yview_scroll(1, "units")

    # ...existing code...
    
    def run(self):
        """Ejecutar la aplicación"""
        # Configurar el manejo del cierre de la aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Manejar el cierre de la aplicación"""
        # Limpiar recursos del PDF
        self.close_pdf_document()
        
        # Cerrar la aplicación
        self.root.destroy()

    def toggle_fullscreen(self):
        """Alternar entre modo normal y pantalla completa del PDF"""
        
        if not self.pdf_document:
            return
        
        if not self.is_fullscreen:
            # Entrar en modo pantalla completa
            self.enter_fullscreen()
        else:
            # Salir del modo pantalla completa
            self.exit_fullscreen()
    
    def enter_fullscreen(self):
        """Entrar en modo pantalla completa"""
        
        # Crear ventana de pantalla completa
        self.fullscreen_window = tk.Toplevel(self.root)
        self.fullscreen_window.title("PDF - Pantalla Completa")
        self.fullscreen_window.attributes('-fullscreen', True)
        self.fullscreen_window.configure(bg='#1e1e1e')
        
        # Configurar escape para salir
        self.fullscreen_window.bind('<Escape>', lambda e: self.exit_fullscreen())
        self.fullscreen_window.bind('<F11>', lambda e: self.exit_fullscreen())
        
        # Frame principal en pantalla completa
        fullscreen_frame = tk.Frame(self.fullscreen_window, bg='#1e1e1e')
        fullscreen_frame.pack(fill="both", expand=True)
        
        # Controles superiores en pantalla completa
        controls_frame = tk.Frame(fullscreen_frame, bg='#2b2b2b', height=50)
        controls_frame.pack(fill="x", pady=5, padx=10)
        controls_frame.pack_propagate(False)
        
        # Botón para salir de pantalla completa
        exit_btn = ctk.CTkButton(
            controls_frame,
            text="❌ Salir (ESC)",
            command=self.exit_fullscreen,
            width=100,
            height=30
        )
        exit_btn.pack(side="left", padx=5, pady=10)
        
        # Controles de navegación en pantalla completa
        nav_frame_fs = tk.Frame(controls_frame, bg='#2b2b2b')
        nav_frame_fs.pack(side="left", padx=20)
        
        prev_btn_fs = ctk.CTkButton(
            nav_frame_fs,
            text="◀️",
            command=self.prev_page,
            width=40,
            height=30
        )
        prev_btn_fs.pack(side="left", padx=2, pady=10)
        
        self.page_label_fs = ctk.CTkLabel(
            nav_frame_fs,
            text=f"{self.current_page + 1}/{self.total_pages}",
            font=ctk.CTkFont(size=12),
            width=60
        )
        self.page_label_fs.pack(side="left", padx=5, pady=10)
        
        next_btn_fs = ctk.CTkButton(
            nav_frame_fs,
            text="▶️",
            command=self.next_page,
            width=40,
            height=30
        )
        next_btn_fs.pack(side="left", padx=2, pady=10)
        
        # Controles de zoom en pantalla completa
        zoom_frame_fs = tk.Frame(controls_frame, bg='#2b2b2b')
        zoom_frame_fs.pack(side="left", padx=20)
        
        zoom_out_btn_fs = ctk.CTkButton(
            zoom_frame_fs,
            text="🔍-",
            command=self.zoom_out,
            width=40,
            height=30
        )
        zoom_out_btn_fs.pack(side="left", padx=2, pady=10)
        
        self.zoom_label_fs = ctk.CTkLabel(
            zoom_frame_fs,
            text=f"{int(self.zoom_level * 100)}%",
            font=ctk.CTkFont(size=12),
            width=50
        )
        self.zoom_label_fs.pack(side="left", padx=5, pady=10)
        
        zoom_in_btn_fs = ctk.CTkButton(
            zoom_frame_fs,
            text="🔍+",
            command=self.zoom_in,
            width=40,
            height=30
        )
        zoom_in_btn_fs.pack(side="left", padx=2, pady=10)
        
        fit_window_btn_fs = ctk.CTkButton(
            zoom_frame_fs,
            text="📐",
            command=self.fit_to_window,
            width=40,
            height=30
        )
        fit_window_btn_fs.pack(side="left", padx=2, pady=10)
        
        # Canvas para el PDF en pantalla completa
        canvas_frame_fs = tk.Frame(fullscreen_frame, bg='#1e1e1e')
        canvas_frame_fs.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.pdf_canvas_fs = tk.Canvas(
            canvas_frame_fs,
            bg="#1e1e1e",
            highlightthickness=0
        )
        
        # Configurar eventos del mouse en canvas de pantalla completa
        self.pdf_canvas_fs.bind("<Button-1>", self.on_pdf_click)
        self.pdf_canvas_fs.bind("<MouseWheel>", self.on_mouse_wheel)
        self.pdf_canvas_fs.bind("<Button-4>", self.on_mouse_wheel)
        self.pdf_canvas_fs.bind("<Button-5>", self.on_mouse_wheel)
        
        # Scrollbars para pantalla completa
        v_scrollbar_fs = tk.Scrollbar(canvas_frame_fs, orient="vertical", command=self.pdf_canvas_fs.yview)
        h_scrollbar_fs = tk.Scrollbar(canvas_frame_fs, orient="horizontal", command=self.pdf_canvas_fs.xview)
        
        self.pdf_canvas_fs.configure(
            yscrollcommand=v_scrollbar_fs.set,
            xscrollcommand=h_scrollbar_fs.set
        )
        
        v_scrollbar_fs.pack(side="right", fill="y")
        h_scrollbar_fs.pack(side="bottom", fill="x")
        self.pdf_canvas_fs.pack(fill="both", expand=True)
        
        # Cambiar estado
        self.is_fullscreen = True
        self.fullscreen_btn.configure(text="📱 Ventana")
        
        # Renderizar página actual en pantalla completa
        self.display_current_page()
        
        # Hacer focus en la ventana de pantalla completa
        self.fullscreen_window.focus_set()
    
    def exit_fullscreen(self):
        """Salir del modo pantalla completa"""
        
        if hasattr(self, 'fullscreen_window'):
            self.fullscreen_window.destroy()
            delattr(self, 'fullscreen_window')
        
        self.is_fullscreen = False
        self.fullscreen_btn.configure(text="🖥️ Pantalla Completa")
        
        # Renderizar página actual en ventana normal
        self.display_current_page()

def main():
    """Función principal"""
    try:
        # Verificar dependencias
        missing_modules = check_python_requirements()
        if missing_modules:
            error_msg = f"Faltan las siguientes dependencias:\n\n"
            error_msg += "\n".join(f"- {module}" for module in missing_modules)
            error_msg += f"\n\nPor favor ejecuta:\npip install {' '.join(missing_modules)}"
            
            if 'tkinter' not in missing_modules:
                messagebox.showerror("Dependencias Faltantes", error_msg)
            else:
                print(error_msg)
                input("Presiona Enter para continuar...")
            return
        
        app = BiomedicaDSPApp()
        app.run()
    except Exception as e:
        error_msg = f"Error al iniciar la aplicación: {e}"
        try:
            messagebox.showerror("Error", error_msg)
        except:
            print(error_msg)
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()
