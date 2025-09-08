@echo off
echo ========================================
echo    BIOMEDICAL DSP - BUILD SCRIPT
echo ========================================
echo.

echo [1/5] Limpiando archivos anteriores...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "__pycache__" rmdir /s /q "__pycache__"
echo ✅ Limpieza completada

echo.
echo [2/5] Verificando dependencias...
python -c "import customtkinter, fitz, matplotlib, numpy, PIL; print('✅ Todas las dependencias están instaladas')" 2>nul
if errorlevel 1 (
    echo ❌ Error: Faltan dependencias. Instalando...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias
        pause
        exit /b 1
    )
)

echo.
echo [3/5] Verificando que PyInstaller está instalado...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ❌ PyInstaller no está instalado. Instalando...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Error al instalar PyInstaller
        pause
        exit /b 1
    )
)

echo.
echo [4/5] Construyendo ejecutable...
echo ⚙️ Esto puede tomar varios minutos...
pyinstaller biomedical_dsp.spec --clean --noconfirm

if errorlevel 1 (
    echo ❌ Error al construir el ejecutable
    pause
    exit /b 1
)

echo.
echo [5/5] Verificando construcción...
if exist "dist\Biomedical-DSP.exe" (
    echo ✅ ¡Ejecutable creado exitosamente!
    echo.
    echo 📁 Ubicación: dist\Biomedical-DSP.exe
    echo 📊 Tamaño: 
    for %%i in ("dist\Biomedical-DSP.exe") do echo    %%~zi bytes
    echo.
    echo 🚀 ¿Deseas ejecutar la aplicación ahora? (S/N)
    set /p ejecutar=""
    if /i "%ejecutar%"=="S" (
        echo 🔄 Iniciando aplicación...
        start "" "dist\Biomedical-DSP.exe"
    )
) else (
    echo ❌ Error: No se pudo crear el ejecutable
    echo 📝 Revisa los logs arriba para más detalles
)

echo.
echo ========================================
echo           BUILD COMPLETADO
echo ========================================
pause
