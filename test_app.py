"""
Script de prueba para verificar que la aplicación funciona correctamente
"""

import sys
import os
from pathlib import Path
import traceback

def test_imports():
    """Probar todas las importaciones necesarias"""
    print("🔍 Probando importaciones...")
    
    modules = {
        'tkinter': 'GUI base',
        'customtkinter': 'GUI moderna', 
        'PIL': 'Procesamiento de imágenes',
        'numpy': 'Cálculos numéricos',
        'matplotlib': 'Gráficos',
        'pathlib': 'Manejo de rutas'
    }
    
    failed_imports = []
    
    for module, description in modules.items():
        try:
            __import__(module)
            print(f"  ✅ {module} - {description}")
        except ImportError as e:
            print(f"  ❌ {module} - {description} - Error: {e}")
            failed_imports.append(module)
    
    return failed_imports

def test_file_structure():
    """Verificar la estructura de archivos"""
    print("\n📁 Verificando estructura de archivos...")
    
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
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
            missing_files.append(file)
    
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"  ✅ {dir_name}/")
            
            # Verificar contenido
            pdf_files = list(dir_path.glob("*.pdf"))
            py_files = list(dir_path.glob("*.py"))
            
            print(f"    📄 {len(pdf_files)} archivos PDF")
            print(f"    🐍 {len(py_files)} archivos Python")
            
        else:
            print(f"  ❌ {dir_name}/")
            missing_dirs.append(dir_name)
    
    return missing_files, missing_dirs

def test_application_startup():
    """Probar que la aplicación puede iniciarse"""
    print("\n🚀 Probando inicio de aplicación...")
    
    try:
        # Importar sin ejecutar
        sys.path.insert(0, str(Path(__file__).parent))
        
        from main import BiomedicaDSPApp
        print("  ✅ Clase principal importada correctamente")
        
        # No vamos a crear la ventana para evitar problemas en testing
        print("  ✅ Aplicación lista para ejecutar")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error al importar aplicación: {e}")
        traceback.print_exc()
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("=" * 50)
    print("🧪 PRUEBAS DE LA APLICACIÓN BIOMEDICAL DSP")
    print("=" * 50)
    
    # Prueba 1: Importaciones
    failed_imports = test_imports()
    
    # Prueba 2: Estructura de archivos
    missing_files, missing_dirs = test_file_structure()
    
    # Prueba 3: Inicio de aplicación
    app_startup_ok = test_application_startup()
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    if failed_imports:
        print(f"❌ Dependencias faltantes: {len(failed_imports)}")
        print(f"   Ejecuta: pip install {' '.join(failed_imports)}")
    else:
        print("✅ Todas las dependencias están disponibles")
    
    if missing_files or missing_dirs:
        print(f"❌ Archivos/directorios faltantes:")
        for item in missing_files + missing_dirs:
            print(f"   - {item}")
    else:
        print("✅ Estructura de archivos completa")
    
    if app_startup_ok:
        print("✅ Aplicación lista para ejecutar")
    else:
        print("❌ Problemas al iniciar aplicación")
    
    # Verificación final
    all_good = not failed_imports and not missing_files and not missing_dirs and app_startup_ok
    
    if all_good:
        print("\n🎉 ¡TODO ESTÁ LISTO!")
        print("   Ejecuta: python main.py")
        print("   O genera el ejecutable con: build_advanced.bat")
    else:
        print("\n⚠️  Hay problemas que resolver antes de continuar")
        
        if failed_imports:
            print(f"\n🔧 Para instalar dependencias:")
            print(f"   pip install -r requirements.txt")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para continuar...")
