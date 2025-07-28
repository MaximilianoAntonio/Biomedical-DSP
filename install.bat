@echo off
title Biomedical DSP - Instalador Automatico

echo.
echo  ╔══════════════════════════════════════╗
echo  ║     Biomedical DSP Learning Platform ║
echo  ║           Instalador Automatico     ║
echo  ╚══════════════════════════════════════╝
echo.

:: Verificar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no esta instalado o no esta en el PATH
    echo.
    echo Por favor instala Python desde: https://python.org
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

echo ✅ Python detectado:
python --version

echo.
echo 📦 Instalando dependencias requeridas...
echo.

:: Instalar pip si no esta disponible
python -m ensurepip --default-pip >nul 2>&1

:: Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip

:: Instalar dependencias
echo Instalando CustomTkinter...
pip install customtkinter>=5.2.0

echo Instalando librerias de procesamiento...
pip install numpy scipy matplotlib

echo Instalando utilidades...
pip install Pillow PyPDF2

echo Instalando PyInstaller para generar ejecutables...
pip install pyinstaller

echo.
echo ✅ Instalacion completada!
echo.
echo ========================================
echo           OPCIONES DISPONIBLES
echo ========================================
echo.
echo 1. Ejecutar aplicacion (modo desarrollo)
echo 2. Generar ejecutable portable
echo 3. Ejecutar aplicacion desde ejecutable
echo 4. Salir
echo.

:menu
set /p choice="Selecciona una opcion (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Ejecutando aplicacion...
    python main.py
    echo.
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo 🔨 Generando ejecutable...
    call build_advanced.bat
    echo.
    goto menu
)

if "%choice%"=="3" (
    if exist "dist\Biomedical-DSP.exe" (
        echo.
        echo 🚀 Ejecutando desde ejecutable...
        "dist\Biomedical-DSP.exe"
        echo.
        goto menu
    ) else (
        echo.
        echo ❌ Ejecutable no encontrado. Genera el ejecutable primero (opcion 2)
        echo.
        goto menu
    )
)

if "%choice%"=="4" (
    echo.
    echo ¡Gracias por usar Biomedical DSP Learning Platform! 👋
    echo.
    pause
    exit /b 0
)

echo.
echo ❌ Opcion invalida. Por favor selecciona 1-4.
echo.
goto menu
