# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# Obtener la ruta base
base_path = Path.cwd()

# Definir archivos de datos
data_files = []

# Agregar carpetas de unidades
unit_folders = [
    "Unidad 01 Muestreo-reconstrucción-cuantiación",
    "Unidad 02 Sistemas de tiempo discreto", 
    "Unidad 03 Transformadas de Fourier",
    "Unidad 04 Diseño de filtros digitales",
    "Unidad 05 Técnicas avanzadas"
]

for folder in unit_folders:
    folder_path = base_path / folder
    if folder_path.exists():
        # Agregar todos los archivos de la carpeta
        for file in folder_path.rglob("*"):
            if file.is_file():
                rel_path = file.relative_to(base_path)
                data_files.append((str(file), str(rel_path.parent)))

# Agregar icono
icon_path = base_path / "icon.ico"
if icon_path.exists():
    data_files.append((str(icon_path), "."))

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=data_files,
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'customtkinter',
        'PIL',
        'PIL._tkinter_finder',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.figure',
        'matplotlib.pyplot',
        'numpy',
        'fitz',
        'PyMuPDF',
        'threading',
        'subprocess',
        'pathlib',
        'io',
        'contextlib',
        're',
        'tempfile',
        'shutil',
        'warnings',
        'darkdetect',  # Nueva dependencia para detección de tema
        'scipy',       # Agregada en requirements
        'typing'       # Para compatibilidad de tipos
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Biomedical-DSP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if icon_path.exists() else None,
)
