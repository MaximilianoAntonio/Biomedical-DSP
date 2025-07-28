"""
Script de prueba para CI/CD (sin emojis para compatibilidad)
"""

import sys
import os
from pathlib import Path
import traceback

def test_imports():
    """Probar todas las importaciones necesarias"""
    print("Probando importaciones...")
    
    modules = {
        'tkinter': 'GUI base',
        'customtkinter': 'GUI moderna', 
        'PIL': 'Procesamiento de imagenes',
        'numpy': 'Calculos numericos',
        'matplotlib': 'Graficos',
        'pathlib': 'Manejo de rutas'
    }
    
    failed_imports = []
    
    for module, description in modules.items():
        try:
            __import__(module)
            print(f"  OK {module} - {description}")
        except ImportError as e:
            print(f"  FAIL {module} - {description} - Error: {e}")
            failed_imports.append(module)
    
    return failed_imports

def test_file_structure():
    """Verificar la estructura de archivos"""
    print("\nVerificando estructura de archivos...")
    
    base_dir = Path(__file__).parent
    
    required_files = [
        'main.py',
        'utils.py',
        'requirements.txt',
        'README.md'
    ]
    
    required_dirs = [
        'Unidad 01 Muestreo-reconstrucción-cuantiación',
        'Unidad 02 Sistemas de tiempo discreto'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        file_path = base_dir / file
        if file_path.exists():
            print(f"  OK {file}")
        else:
            print(f"  MISSING {file}")
            missing_files.append(file)
    
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"  OK {dir_name}/")
            
            # Verificar contenido
            pdf_files = list(dir_path.glob("*.pdf"))
            py_files = list(dir_path.glob("*.py"))
            
            print(f"    PDF files: {len(pdf_files)}")
            print(f"    Python files: {len(py_files)}")
            
        else:
            print(f"  MISSING {dir_name}/")
            missing_dirs.append(dir_name)
    
    return missing_files, missing_dirs

def test_application_startup():
    """Probar que la aplicacion puede iniciarse"""
    print("\nProbando inicio de aplicacion...")
    
    try:
        # Importar sin ejecutar
        sys.path.insert(0, str(Path(__file__).parent))
        
        from main import BiomedicaDSPApp
        print("  OK Clase principal importada correctamente")
        
        # No vamos a crear la ventana para evitar problemas en CI
        print("  OK Aplicacion lista para ejecutar")
        
        return True
        
    except Exception as e:
        print(f"  FAIL Error al importar aplicacion: {e}")
        traceback.print_exc()
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("=" * 50)
    print("PRUEBAS DE LA APLICACION BIOMEDICAL DSP")
    print("=" * 50)
    
    # Prueba 1: Importaciones
    failed_imports = test_imports()
    
    # Prueba 2: Estructura de archivos
    missing_files, missing_dirs = test_file_structure()
    
    # Prueba 3: Inicio de aplicacion
    app_startup_ok = test_application_startup()
    
    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    if failed_imports:
        print(f"FAIL Dependencias faltantes: {len(failed_imports)}")
        print(f"   Ejecuta: pip install {' '.join(failed_imports)}")
        return False
    else:
        print("OK Todas las dependencias estan disponibles")
    
    if missing_files or missing_dirs:
        print(f"FAIL Archivos/directorios faltantes:")
        for item in missing_files + missing_dirs:
            print(f"   - {item}")
        return False
    else:
        print("OK Estructura de archivos completa")
    
    if app_startup_ok:
        print("OK Aplicacion lista para ejecutar")
    else:
        print("FAIL Problemas al iniciar aplicacion")
        return False
    
    # Verificacion final
    all_good = not failed_imports and not missing_files and not missing_dirs and app_startup_ok
    
    if all_good:
        print("\nSUCCESS - TODO ESTA LISTO!")
        print("   Aplicacion lista para compilar")
        return True
    else:
        print("\nFAIL - Hay problemas que resolver")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
