@echo off
echo ========================================
echo  Generando ejecutable de Biomedical DSP
echo ========================================
echo.

echo Instalando pyinstaller si no esta presente...
pip install pyinstaller

echo.
echo Generando ejecutable...
pyinstaller --name="Biomedical-DSP" ^
            --onefile ^
            --windowed ^
            --icon=icon.ico ^
            --add-data="Unidad 01 Muestreo-reconstrucción-cuantiación;Unidad 01 Muestreo-reconstrucción-cuantiación/" ^
            --add-data="Unidad 02 Sistemas de tiempo discreto;Unidad 02 Sistemas de tiempo discreto/" ^
            --add-data="Unidad 03 Transformadas de Fourier;Unidad 03 Transformadas de Fourier/" ^
            --add-data="Unidad 04 Diseño de filtros digitales;Unidad 04 Diseño de filtros digitales/" ^
            --add-data="Unidad 05 Técnicas avanzadas;Unidad 05 Técnicas avanzadas/" ^
            --add-data="icon.ico;." ^
            --hidden-import=tkinter ^
            --hidden-import=customtkinter ^
            --hidden-import=PIL ^
            --hidden-import=matplotlib ^
            --hidden-import=numpy ^
            --hidden-import=scipy ^
            main.py

echo.
echo ========================================
echo  Ejecutable generado en: dist/Biomedical-DSP.exe
echo ========================================
echo.

if exist "dist\Biomedical-DSP.exe" (
    echo ✅ Ejecutable creado exitosamente!
    echo.
    echo Para distribuir:
    echo 1. Copia el archivo dist/Biomedical-DSP.exe
    echo 2. Copia todas las carpetas de Unidades
    echo 3. Copia el archivo icon.ico
    echo.
    echo ¿Deseas abrir la carpeta dist?
    set /p choice="(S/N): "
    if /i "%choice%"=="S" (
        explorer dist
    )
) else (
    echo ❌ Error al generar el ejecutable
    echo Revisa los mensajes anteriores para mas detalles
)

echo.
pause
