@echo off
echo ========================================
echo  Biomedical DSP - Build Avanzado
echo ========================================
echo.

echo Verificando dependencias...
pip install -r requirements.txt

echo.
echo Limpiando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"

echo.
echo Generando ejecutable con configuracion personalizada...
pyinstaller biomedical_dsp.spec

echo.
echo ========================================
echo  Proceso completado
echo ========================================
echo.

if exist "dist\Biomedical-DSP.exe" (
    echo ✅ Ejecutable creado exitosamente!
    echo.
    echo Ubicacion: dist\Biomedical-DSP.exe
    echo Tamaño: 
    for %%A in ("dist\Biomedical-DSP.exe") do echo   %%~zA bytes
    echo.
    echo Para distribuir el ejecutable:
    echo 1. El ejecutable ya incluye todos los archivos necesarios
    echo 2. Solo necesitas distribuir: Biomedical-DSP.exe
    echo 3. El ejecutable es completamente portable
    echo.
    
    set /p choice="¿Deseas probar el ejecutable ahora? (S/N): "
    if /i "%choice%"=="S" (
        echo Ejecutando...
        "dist\Biomedical-DSP.exe"
    )
    
    echo.
    set /p choice="¿Deseas abrir la carpeta dist? (S/N): "
    if /i "%choice%"=="S" (
        explorer dist
    )
) else (
    echo ❌ Error al generar el ejecutable
    echo.
    echo Posibles soluciones:
    echo 1. Verifica que todas las dependencias esten instaladas
    echo 2. Ejecuta: pip install -r requirements.txt
    echo 3. Revisa los mensajes de error anteriores
    echo.
)

echo.
pause
