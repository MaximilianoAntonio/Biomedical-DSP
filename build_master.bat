@echo off
title Biomedical DSP - Build Master
color 0A

echo ╔══════════════════════════════════════════════════════╗
echo ║           BIOMEDICAL DSP - BUILD MASTER              ║
echo ║              Construcción Automática                 ║
echo ╚══════════════════════════════════════════════════════╝
echo.

echo 🧹 [PASO 1] Limpieza de archivos innecesarios...
echo ========================================

REM Eliminar archivos de cache y temporales
if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo ✅ Eliminado: __pycache__
)

if exist "build" (
    rmdir /s /q "build"
    echo ✅ Eliminado: build/
)

if exist "dist" (
    rmdir /s /q "dist"
    echo ✅ Eliminado: dist/
)

if exist "distribution" (
    rmdir /s /q "distribution"
    echo ✅ Eliminado: distribution/
)

REM Eliminar archivos .pyc si existen
for /r %%i in (*.pyc) do (
    del "%%i" >nul 2>&1
)

echo ✅ Limpieza completada
echo.

echo 🔍 [PASO 2] Verificación de dependencias...
echo ========================================

C:/Users/maxim/AppData/Local/Microsoft/WindowsApps/python3.13.exe -c "import sys; print(f'Python: {sys.version}')"
echo.

echo Verificando librerías...
C:/Users/maxim/AppData/Local/Microsoft/WindowsApps/python3.13.exe -c "try: import customtkinter; print('✅ CustomTkinter: OK'); except: print('❌ CustomTkinter: FALTA')"
C:/Users/maxim/AppData/Local/Microsoft/WindowsApps/python3.13.exe -c "try: import fitz; print('✅ PyMuPDF: OK'); except: print('❌ PyMuPDF: FALTA')"
C:/Users/maxim/AppData/Local/Microsoft/WindowsApps/python3.13.exe -c "try: import matplotlib; print('✅ Matplotlib: OK'); except: print('❌ Matplotlib: FALTA')"
C:/Users/maxim/AppData/Local/Microsoft/WindowsApps/python3.13.exe -c "try: import numpy; print('✅ NumPy: OK'); except: print('❌ NumPy: FALTA')"
C:/Users/maxim/AppData/Local/Microsoft/WindowsApps/python3.13.exe -c "try: import PIL; print('✅ Pillow: OK'); except: print('❌ Pillow: FALTA')"
C:/Users/maxim/AppData/Local/Microsoft/WindowsApps/python3.13.exe -c "try: import PyInstaller; print('✅ PyInstaller: OK'); except: print('❌ PyInstaller: FALTA')"

echo.
echo 🔨 [PASO 3] Construcción del ejecutable...
echo ========================================

echo ⚙️ Iniciando PyInstaller (esto puede tomar varios minutos)...
C:/Users/maxim/AppData/Local/Microsoft/WindowsApps/python3.13.exe -m PyInstaller biomedical_dsp.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo ❌ ERROR: Fallo en la construcción del ejecutable
    echo 📝 Revisa los mensajes de error arriba
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Ejecutable creado exitosamente
)

echo.
echo 🎨 [PASO 4] Optimización y empaquetado...
echo ========================================

C:/Users/maxim/AppData/Local/Microsoft/WindowsApps/python3.13.exe optimize_build.py

if errorlevel 1 (
    echo ❌ ERROR: Fallo en la optimización
    pause
    exit /b 1
)

echo.
echo 🧪 [PASO 5] Prueba del ejecutable...
echo ========================================

if exist "dist\Biomedical-DSP.exe" (
    echo ✅ Ejecutable encontrado
    
    echo 📊 Información del archivo:
    for %%i in ("dist\Biomedical-DSP.exe") do (
        echo    📁 Tamaño: %%~zi bytes
        echo    📅 Fecha: %%~ti
    )
    
    echo.
    echo 🧪 ¿Deseas probar el ejecutable ahora? (S/N)
    set /p test=""
    if /i "%test%"=="S" (
        echo 🚀 Iniciando prueba...
        timeout /t 2 /nobreak >nul
        start "" "dist\Biomedical-DSP.exe"
        echo ✅ Aplicación iniciada. Revisa que funcione correctamente.
        timeout /t 3 /nobreak >nul
    )
) else (
    echo ❌ ERROR: No se encontró el ejecutable final
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║                 BUILD COMPLETADO                     ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo 🎉 ¡Construcción exitosa!
echo.
echo 📁 Archivos generados:
echo    • dist/Biomedical-DSP.exe          (Ejecutable principal)
echo    • distribution/                    (Paquete completo)
echo    • Biomedical-DSP-Portable.zip     (Archivo para distribución)
echo.
echo 📋 Próximos pasos:
echo    1. Prueba el ejecutable en dist/
echo    2. Usa distribution/ para distribución local
echo    3. Usa el .zip para compartir
echo.
echo 🚀 ¡Tu aplicación está lista para usar!

pause
