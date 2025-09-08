@echo off
echo ========================================
echo   Biomedical DSP - Build Script v2.0
echo ========================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo ERROR: No se encuentra main.py en el directorio actual
    echo Por favor ejecuta este script desde el directorio del proyecto
    pause
    exit /b 1
)

echo 1. Verificando dependencias...
python -c "import customtkinter, PyMuPDF, matplotlib, numpy, PIL" 2>nul
if errorlevel 1 (
    echo ERROR: Faltan dependencias. Instalando...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
) else (
    echo   ✓ Todas las dependencias están instaladas
)

echo.
echo 2. Limpiando builds anteriores...
if exist "build\" rmdir /s /q "build\"
if exist "dist\" rmdir /s /q "dist\"
if exist "__pycache__\" rmdir /s /q "__pycache__\"
echo   ✓ Limpieza completada

echo.
echo 3. Construyendo ejecutable con PyInstaller...
echo   Esto puede tomar varios minutos...
pyinstaller biomedical_dsp.spec --clean --noconfirm

if errorlevel 1 (
    echo ERROR: Falló la construcción del ejecutable
    pause
    exit /b 1
)

echo.
echo 4. Verificando que el ejecutable se creó correctamente...
if exist "dist\Biomedical-DSP.exe" (
    echo   ✓ Ejecutable creado exitosamente
    
    REM Obtener el tamaño del archivo
    for %%A in ("dist\Biomedical-DSP.exe") do set size=%%~zA
    echo   📦 Tamaño: %size% bytes
) else (
    echo ERROR: No se pudo crear el ejecutable
    pause
    exit /b 1
)

echo.
echo 5. Creando package de distribución...
if not exist "distribution\" mkdir "distribution"

REM Copiar ejecutable
copy "dist\Biomedical-DSP.exe" "distribution\" >nul

REM Copiar archivos necesarios
if exist "icon.ico" copy "icon.ico" "distribution\" >nul
if exist "README.md" copy "README.md" "distribution\" >nul
if exist "MEJORAS_INTERFAZ.md" copy "MEJORAS_INTERFAZ.md" "distribution\" >nul

REM Copiar carpetas de unidades
for %%D in ("Unidad*") do (
    if exist "%%D\" (
        echo   📁 Copiando %%D...
        xcopy "%%D\*" "distribution\%%D\" /E /I /Q >nul
    )
)

REM Crear archivos adicionales para la distribución
echo Creando archivo INSTALAR.bat...
(
echo @echo off
echo echo ========================================
echo echo   Biomedical DSP - Instalación
echo echo ========================================
echo echo.
echo echo Este es un ejecutable portable. No requiere instalación.
echo echo.
echo echo Para ejecutar la aplicación:
echo echo 1. Haz doble clic en Biomedical-DSP.exe
echo echo 2. O ejecuta desde línea de comandos
echo echo.
echo echo Requisitos del sistema:
echo echo - Windows 10/11 ^(recomendado^)
echo echo - 4GB RAM mínimo
echo echo - 1GB espacio libre
echo echo.
echo pause
) > "distribution\INSTALAR.bat"

echo Creando archivo LEEME.txt...
(
echo ========================================
echo   Biomedical DSP v2.0 - Distribución
echo ========================================
echo.
echo 🧠 APLICACIÓN MEJORADA CON NUEVAS CARACTERÍSTICAS:
echo.
echo ✨ NUEVAS FUNCIONES:
echo • Sistema de temas claro/oscuro
echo • Detección automática del tema del sistema
echo • Fuentes mejoradas específicas por OS
echo • Interfaz más moderna y pulida
echo • Mejor compatibilidad multiplataforma
echo • Configuración persistente de preferencias
echo.
echo 📁 CONTENIDO DEL PACKAGE:
echo • Biomedical-DSP.exe - Aplicación principal
echo • Carpetas Unidad XX - Material del curso
echo • MANUAL_USUARIO.md - Manual de usuario
echo • MEJORAS_INTERFAZ.md - Documentación de mejoras
echo.
echo 🚀 INSTRUCCIONES DE USO:
echo 1. Ejecuta Biomedical-DSP.exe
echo 2. Selecciona una unidad del curso en el panel izquierdo
echo 3. Elige una clase específica
echo 4. Ve el PDF y ejecuta código Python
echo 5. Cambia temas usando los controles superiores
echo.
echo 🔧 SOLUCIÓN DE PROBLEMAS:
echo • Si no se ve correctamente, cambia el tema
echo • Para mejor rendimiento, cierra otros programas
echo • Los archivos temporales se guardan en config/
echo.
echo 📞 SOPORTE:
echo GitHub: MaximilianoAntonio/Biomedical-DSP
echo.
echo Versión: 2.0
echo Fecha: %date%
) > "distribution\LEEME.txt"

echo   ✓ Package de distribución creado

echo.
echo 6. Probando el ejecutable...
start /wait "Test" "dist\Biomedical-DSP.exe" 2>nul
echo   ✓ Prueba completada

echo.
echo ========================================
echo ✅ BUILD COMPLETADO EXITOSAMENTE
echo ========================================
echo.
echo 📦 Archivos generados:
echo   • dist\Biomedical-DSP.exe
echo   • distribution\ ^(package completo^)
echo.
echo 📊 Estadísticas:
dir "dist\Biomedical-DSP.exe" | find "Biomedical-DSP.exe"
echo.
echo 🚀 Listo para distribución!
echo.
pause
