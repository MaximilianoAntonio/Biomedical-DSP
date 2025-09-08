#!/usr/bin/env python3
"""
Script de prueba para verificar que todas las dependencias están instaladas correctamente
"""

print("🔍 Verificando dependencias...")

try:
    import tkinter as tk
    print("✅ tkinter: OK")
except ImportError as e:
    print(f"❌ tkinter: {e}")

try:
    import customtkinter as ctk
    print("✅ customtkinter: OK")
except ImportError as e:
    print(f"❌ customtkinter: {e}")

try:
    import fitz  # PyMuPDF
    print("✅ PyMuPDF: OK")
except ImportError as e:
    print(f"❌ PyMuPDF: {e}")

try:
    from PIL import Image, ImageTk
    print("✅ Pillow (PIL): OK")
except ImportError as e:
    print(f"❌ Pillow (PIL): {e}")

try:
    import numpy as np
    print("✅ numpy: OK")
except ImportError as e:
    print(f"❌ numpy: {e}")

print("\n🧪 Prueba de funcionalidad de PyMuPDF...")

try:
    # Crear un PDF de prueba simple
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((100, 100), "Prueba de PDF", fontsize=20)
    
    # Renderizar como imagen
    pix = page.get_pixmap()
    img_data = pix.tobytes("ppm")
    
    print("✅ PyMuPDF puede crear y renderizar PDFs correctamente")
    doc.close()
    
except Exception as e:
    print(f"❌ Error en PyMuPDF: {e}")

print("\n🎉 Verificación completa!")
