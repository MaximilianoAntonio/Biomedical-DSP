"""
Utilidades para la aplicación Biomedical DSP
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

def get_resource_path(relative_path):
    """
    Obtener la ruta de un recurso, funciona tanto en desarrollo como en ejecutable
    """
    if getattr(sys, 'frozen', False):
        # Si estamos ejecutando desde un ejecutable de PyInstaller
        base_path = sys._MEIPASS
    else:
        # Si estamos ejecutando desde el script Python
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)

def open_file_with_default_app(file_path):
    """
    Abrir archivo con la aplicación predeterminada del sistema
    """
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", file_path])
        else:  # Linux y otros Unix
            subprocess.run(["xdg-open", file_path])
        return True
    except Exception as e:
        print(f"Error al abrir archivo: {e}")
        return False

def check_python_requirements():
    """
    Verificar que las dependencias de Python estén disponibles
    """
    required_modules = [
        'tkinter',
        'customtkinter', 
        'PIL',
        'numpy',
        'matplotlib',
        'fitz'  # PyMuPDF
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    return missing_modules

def get_system_info():
    """
    Obtener información del sistema para debugging
    """
    info = {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'python_version': sys.version,
        'architecture': platform.architecture()[0],
        'executable_path': sys.executable if not getattr(sys, 'frozen', False) else 'Ejecutable PyInstaller'
    }
    
    return info

def ensure_directory_exists(directory_path):
    """
    Asegurar que un directorio existe, crearlo si no
    """
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def get_safe_filename(filename):
    """
    Convertir un nombre de archivo a uno seguro para el sistema
    """
    import string
    
    # Caracteres válidos para nombres de archivo
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    
    # Reemplazar caracteres inválidos
    safe_name = ''.join(c for c in filename if c in valid_chars)
    
    # Limitar longitud
    if len(safe_name) > 255:
        safe_name = safe_name[:255]
    
    return safe_name
