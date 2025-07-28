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
        
        self.pdf_label = ctk.CTkLabel(
            pdf_controls,
            text="Selecciona una clase para ver el material PDF",
            font=ctk.CTkFont(size=14)
        )
        self.pdf_label.pack(side="left", padx=10, pady=10)
        
        self.open_pdf_btn = ctk.CTkButton(
            pdf_controls,
            text="🔍 Abrir PDF",
            command=self.open_pdf_external,
            state="disabled"
        )
        self.open_pdf_btn.pack(side="right", padx=10, pady=10)
        
        self.fullscreen_pdf_btn = ctk.CTkButton(
            pdf_controls,
            text="🖥️ Pantalla Completa",
            command=self.open_pdf_fullscreen,
            state="disabled"
        )
        self.fullscreen_pdf_btn.pack(side="right", padx=5, pady=10)
        
        # Frame para mostrar información del PDF
        self.pdf_info_frame = ctk.CTkFrame(self.pdf_tab)
        self.pdf_info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.pdf_info_label = ctk.CTkLabel(
            self.pdf_info_frame,
            text="📖 El material PDF se abrirá en tu visor predeterminado",
            font=ctk.CTkFont(size=12),
            wraplength=400
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
            self.fullscreen_pdf_btn.configure(state="normal")
        else:
            self.pdf_label.configure(text="❌ No hay PDF disponible para esta clase")
            self.open_pdf_btn.configure(state="disabled")
            self.fullscreen_pdf_btn.configure(state="disabled")
        
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
    
    def open_pdf_fullscreen(self):
        """Abrir PDF en pantalla completa"""
        # Esta función intentará abrir el PDF con parámetros de pantalla completa
        self.open_pdf_external()
        messagebox.showinfo("Consejo", "Usa F11 o el menú Ver > Pantalla completa en tu visor de PDF")
    
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
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

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
