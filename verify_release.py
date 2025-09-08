#!/usr/bin/env python3
"""
Script de verificación para la release v2.0
Verifica que todos los archivos están listos para distribución
"""

import os
import sys
from pathlib import Path
import zipfile

def check_file_exists(filepath, description):
    """Verificar que un archivo existe"""
    if Path(filepath).exists():
        size = Path(filepath).stat().st_size
        print(f"✅ {description}: {filepath} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description}: {filepath} - NO ENCONTRADO")
        return False

def check_zip_contents(zip_path):
    """Verificar contenido del ZIP"""
    print(f"\n📦 Verificando contenido de {zip_path}:")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            files = zip_ref.namelist()
            for file in sorted(files):
                print(f"   📄 {file}")
        print(f"   Total archivos: {len(files)}")
        return True
    except Exception as e:
        print(f"❌ Error al verificar ZIP: {e}")
        return False

def main():
    print("🔍 Verificación de Release v2.0 - Biomedical DSP")
    print("=" * 50)
    
    base_dir = Path(__file__).parent
    os.chdir(base_dir)
    
    all_good = True
    
    # Verificar archivos principales
    print("\n📋 Archivos principales:")
    all_good &= check_file_exists("main.py", "Archivo principal")
    all_good &= check_file_exists("requirements.txt", "Dependencias")
    all_good &= check_file_exists("biomedical_dsp.spec", "Configuración PyInstaller")
    all_good &= check_file_exists("icon.ico", "Icono de la aplicación")
    
    # Verificar archivos de documentación
    print("\n📚 Documentación:")
    all_good &= check_file_exists("README.md", "README principal")
    all_good &= check_file_exists("MEJORAS_INTERFAZ.md", "Guía de mejoras")
    all_good &= check_file_exists("RELEASE_NOTES_v2.0.md", "Notas de release")
    
    # Verificar build
    print("\n🔨 Archivos de build:")
    all_good &= check_file_exists("dist/Biomedical-DSP.exe", "Ejecutable principal")
    all_good &= check_file_exists("build_enhanced.bat", "Script de build")
    
    # Verificar distribución
    print("\n📦 Distribución:")
    all_good &= check_file_exists("Biomedical-DSP-v2.0-Portable.zip", "Package portable")
    all_good &= check_file_exists("distribution/Biomedical-DSP.exe", "Ejecutable en distribución")
    all_good &= check_file_exists("distribution/CHANGELOG_v2.0.md", "Changelog")
    all_good &= check_file_exists("distribution/INSTALAR.bat", "Script de instalación")
    
    # Verificar contenido del ZIP
    if Path("Biomedical-DSP-v2.0-Portable.zip").exists():
        all_good &= check_zip_contents("Biomedical-DSP-v2.0-Portable.zip")
    
    # Verificar directorios de contenido
    print("\n📁 Directorios de contenido:")
    unit_dirs = [d for d in Path(".").iterdir() if d.is_dir() and d.name.startswith("Unidad")]
    for unit_dir in sorted(unit_dirs):
        pdf_count = len(list(unit_dir.glob("*.pdf")))
        py_count = len(list(unit_dir.glob("*.py")))
        print(f"   📚 {unit_dir.name}: {pdf_count} PDFs, {py_count} archivos Python")
    
    # Verificar git
    print("\n🔄 Estado Git:")
    try:
        import subprocess
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("⚠️  Hay cambios no committeados:")
            print(result.stdout)
        else:
            print("✅ Repositorio limpio")
        
        # Verificar tags
        result = subprocess.run(["git", "tag", "-l", "v2.0.0"], 
                              capture_output=True, text=True, check=True)
        if "v2.0.0" in result.stdout:
            print("✅ Tag v2.0.0 existe")
        else:
            print("❌ Tag v2.0.0 no encontrado")
            all_good = False
            
    except Exception as e:
        print(f"⚠️  No se pudo verificar Git: {e}")
    
    # Resumen final
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 ¡VERIFICACIÓN EXITOSA!")
        print("✅ La release v2.0 está lista para distribución")
        print("\n📋 Pasos siguientes:")
        print("1. Subir Biomedical-DSP-v2.0-Portable.zip como release asset")
        print("2. Usar RELEASE_NOTES_v2.0.md como descripción de la release")
        print("3. Marcar como 'Latest Release'")
        print("4. ¡Publicar! 🚀")
    else:
        print("❌ HAY PROBLEMAS QUE RESOLVER")
        print("Por favor corrige los errores antes de crear la release")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
