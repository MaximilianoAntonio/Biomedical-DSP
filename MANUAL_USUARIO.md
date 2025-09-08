# Biomedical Digital Signal Processing - Guía de Usuario

## 🚀 Funcionalidades Principales

### Visor de PDF Integrado
- **Visualización directa**: Los PDFs se muestran directamente en la aplicación, no necesitas un visor externo
- **Navegación por páginas**: Usa los botones ◀️ y ▶️ o los atajos de teclado
- **Zoom inteligente**: Sistema de zoom mejorado con ajuste automático
  - **Zoom manual**: Botones 🔍+ y 🔍- para control preciso
  - **Ajuste automático**: Botón 📐 para ajustar a la ventana
  - **Zoom al ancho**: Ajusta automáticamente al ancho de la ventana
- **Scroll avanzado**: Navegación fluida con mouse y teclado
- **Centrado automático**: Las páginas se centran automáticamente en la ventana

### Editor de Código Python
- **Edición directa**: Modifica el código Python directamente en la aplicación
- **Guardado automático**: Los cambios se guardan antes de ejecutar
- **Syntax highlighting**: Colores que facilitan la lectura del código

### Ejecución de Código
- **Ejecución integrada**: Ejecuta el código Python sin salir de la aplicación
- **Salida en tiempo real**: Ve los resultados y errores directamente
- **Control de ejecución**: Detén procesos largos si es necesario

## ⌨️ Atajos de Teclado

### Navegación del PDF
- **←** (Flecha izquierda): Página anterior
- **→** (Flecha derecha): Página siguiente
- **Page Up**: Página anterior
- **Page Down**: Página siguiente

### Zoom del PDF
- **↑** (Flecha arriba): Aumentar zoom
- **↓** (Flecha abajo): Disminuir zoom
- **Ctrl + +**: Aumentar zoom
- **Ctrl + -**: Disminuir zoom
- **Ctrl + 0**: Resetear zoom al 100%
- **Ctrl + F**: Ajustar PDF a la ventana
- **Ctrl + W**: Ajustar PDF al ancho de la ventana

### Control del mouse en PDF
- **Click izquierdo (mitad izquierda)**: Página anterior
- **Click izquierdo (mitad derecha)**: Página siguiente
- **Ctrl + Scroll**: Zoom in/out
- **Shift + Scroll**: Desplazamiento horizontal
- **Scroll normal**: Desplazamiento vertical

### Acciones generales
- **Ctrl + O**: Abrir PDF en aplicación externa
- **Ctrl + S**: Guardar cambios en el código
- **F5**: Ejecutar código Python

## 📚 Estructura del Curso

La aplicación organiza automáticamente el contenido por:
1. **Unidades**: Agrupaciones temáticas del curso
2. **Clases**: Cada clase incluye material PDF y código Python asociado
3. **Navegación intuitiva**: Panel izquierdo para selección rápida

## 🔧 Funcionalidades Avanzadas

### Visor de PDF
- **Renderizado de alta calidad**: Usa PyMuPDF para renderizado profesional
- **Zoom adaptativo**: Desde 40% hasta 300%
- **Navegación fluida**: Sin parpadeos entre páginas
- **Memoria optimizada**: Carga eficiente de documentos grandes

### Editor de Código
- **Sintaxis Python**: Optimizado para código científico
- **Scrollbars automáticos**: Para archivos grandes
- **Preservación de formato**: Mantiene indentación y formato original

### Sistema de Ejecución
- **Entorno aislado**: Cada script se ejecuta en su directorio
- **Timeout de seguridad**: Evita procesos infinitos (60 segundos)
- **Captura completa**: Stdout, stderr y códigos de salida

## 🐛 Solución de Problemas

### PDF no se carga
- Verifica que el archivo PDF no esté dañado
- Asegúrate de que tienes permisos de lectura
- Reinicia la aplicación si persiste el problema

### Código no se ejecuta
- Verifica que tengas Python instalado correctamente
- Comprueba que todas las librerías necesarias estén instaladas
- Revisa la salida de errores en la pestaña de ejecución

### Rendimiento lento
- Cierra PDFs grandes cuando no los uses
- Ajusta el zoom a niveles moderados (50%-150%)
- Reinicia la aplicación si has cargado muchos documentos

## 📞 Soporte

Para reportar problemas o sugerir mejoras:
1. Verifica que todas las dependencias estén instaladas (`pip install -r requirements.txt`)
2. Ejecuta `test_imports.py` para verificar la instalación
3. Revisa los logs en la consola para errores específicos

---

**Versión**: 2.0 con Visor PDF Integrado  
**Dependencias**: CustomTkinter, PyMuPDF, Pillow, NumPy, Matplotlib
