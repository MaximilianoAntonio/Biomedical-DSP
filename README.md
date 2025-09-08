# 🧠 Biomedical Digital Signal Processing

Una aplicación de escritorio completa para estudiar Procesamiento Digital de Señales Biomédicas con interfaz unificada, visor PDF integrado, ejecución de código Python y visualización de gráficos en tiempo real.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Descarga Rápida

### ⚡ Opción 1: Ejecutable Portable (Recomendado)
```
📦 Descarga: Biomedical-DSP-Portable.zip (125 MB)
🖥️ Compatibilidad: Windows 10/11 (64-bit)
🚫 Sin instalación requerida - Sin dependencias
✅ Listo para usar inmediatamente
```

1. **Descarga** el archivo `Biomedical-DSP-Portable.zip`
2. **Extrae** en cualquier carpeta de tu preferencia
3. **Ejecuta** `INSTALAR.bat` (opcional - crea acceso directo)
4. **Usa** `Biomedical-DSP.exe` directamente

### 🛠️ Opción 2: Para Desarrolladores
```bash
git clone https://github.com/MaximilianoAntonio/Biomedical-DSP.git
cd Biomedical-DSP
pip install -r requirements.txt
python main.py
```

## ✨ Características Principales

### 🎨 **Interfaz Unificada Moderna**
- **Panel Horizontal Optimizado**: 40% código, 60% gráficos
- **Tema Oscuro** optimizado para estudio prolongado
- **Navegación Intuitiva** por unidades y clases del curso
- **Responsive Design** que se adapta a diferentes tamaños de pantalla

### 📄 **Visor PDF Integrado Avanzado**
- **Visualización en aplicación** - Sin programas externos
- **Zoom dinámico** con ajuste automático a ventana
- **Modo pantalla completa** con controles integrados
- **Navegación fluida** con botones y atajos de teclado
- **Cache inteligente** para navegación rápida

### 💻 **Editor y Ejecutor Python Integrado**
- **Editor con resaltado de sintaxis** (Consolas font)
- **Ejecución en tiempo real** con captura de output
- **Integración matplotlib** - Gráficos aparecen automáticamente
- **Namespace persistente** - Variables se mantienen entre ejecuciones
- **Manejo de errores** con mensajes claros

### 📊 **Visualización de Gráficos Prominente**
- **Panel dedicado de gráficos** con scroll automático
- **Captura automática** de plt.show() y matplotlib figures
- **Múltiples gráficos** organizados verticalmente
- **Exportación** de gráficos individuales o en lote
- **Compatibilidad completa** con seaborn, pandas plotting, scipy

### 📚 **Contenido Académico Completo**
- **5 Unidades temáticas** con materiales completos
- **PDFs teóricos** y **códigos prácticos** para cada clase
- **Navegación jerárquica** por unidad → clase → material
- **Sincronización automática** entre PDF y código correspondiente

## 🎯 Guía de Uso

### 🔹 **Navegación Principal**
1. **Panel Izquierdo**: Explora las 5 unidades del curso
2. **Selecciona una clase**: Carga automáticamente PDF + código
3. **Interface unificada**: Todo visible simultáneamente

### 🔹 **Trabajando con PDFs**
- **Navegación**: Botones ◀️▶️ o flechas del teclado
- **Zoom**: Botones 🔍+/🔍- o Ctrl + scroll del mouse
- **Ajuste automático**: Botón 📐 ajusta a ventana
- **Pantalla completa**: Botón 🖥️ para modo inmersivo
- **Abrir externo**: Botón 🔗 para visor externo

### 🔹 **Ejecutando Código Python**
- **Botón EJECUTAR**: ▶️ Ejecuta todo el código
- **Salida en tiempo real**: Aparece en panel inferior izquierdo
- **Gráficos automáticos**: Se muestran en panel derecho principal
- **Guardar cambios**: 💾 Para persistir modificaciones

### 🔹 **Gestión de Gráficos**
- **Visualización automática**: Los gráficos aparecen al ejecutar
- **Scroll vertical**: Para múltiples gráficos
- **Guardar todo**: 💾 Exporta todos los gráficos
- **Limpiar**: 🗑️ Limpia el área de visualización

## ⌨️ Atajos de Teclado

### 📄 **Control de PDF**
- `←` `→` - Navegar páginas
- `Ctrl + ↑` `Ctrl + ↓` - Zoom in/out
- `Ctrl + 0` - Ajustar a ventana
- `F11` - Pantalla completa
- `Escape` - Salir de pantalla completa

### 💻 **Control de Código**
- `F5` - Ejecutar código
- `Ctrl + S` - Guardar código
- `Ctrl + L` - Limpiar salida
- `Ctrl + Shift + C` - Limpiar gráficos

## 📋 Requisitos del Sistema

### 🖥️ **Para Ejecutable (Usuarios)**
```
Sistema: Windows 10/11 (64-bit)
RAM: 4GB mínimo, 8GB recomendado
Espacio: 200MB libres
Dependencias: ❌ Ninguna (todo incluido)
```

### 🛠️ **Para Desarrollo**
```
Python: 3.10+ (testado con 3.13)
RAM: 8GB recomendado
Dependencias: Ver requirements.txt
```

## 🏗️ Construcción y Desarrollo

### 📦 **Construir Ejecutable**
```bash
# Build completo con optimización
.\build_master.bat

# Build rápido para testing
.\build_exe.bat

# Solo optimización (requiere dist/)
python optimize_build.py
```

### 🔧 **Dependencias Principales**
```python
customtkinter>=5.2.0    # Interface moderna
PyMuPDF>=1.23.0         # Visor PDF integrado  
matplotlib>=3.10.0      # Gráficos y visualización
numpy>=2.2.0           # Cálculos numéricos
Pillow>=11.3.0         # Procesamiento imágenes
pyinstaller>=6.15.0    # Generación ejecutables
```

### 🧪 **Testing y Validación**
```bash
# Verificar imports y dependencias
python -c "import main; print('✅ OK')"

# Ejecutar aplicación en modo desarrollo  
python main.py

# Verificar ejecutable generado
.\dist\Biomedical-DSP.exe
```

## 📁 Estructura del Proyecto

```
📂 Biomedical-DSP/
├── 📄 main.py                    # Aplicación principal
├── 📄 utils.py                   # Utilidades auxiliares
├── 📄 requirements.txt           # Dependencias Python
├── 📄 biomedical_dsp.spec        # Configuración PyInstaller
├── 🔨 build_master.bat           # Script build completo
├── 🔧 optimize_build.py          # Optimización post-build
├── 📁 dist/                      # Ejecutable generado
│   └── Biomedical-DSP.exe
├── 📁 distribution/              # Paquete distribución
│   ├── Biomedical-DSP.exe
│   ├── INSTALAR.bat
│   └── materiales...
├── 📦 Biomedical-DSP-Portable.zip # Archivo distribución
└── 📚 Unidad XX/                 # Materiales curso
    ├── *.pdf                     # Clases teóricas  
    └── *.py                      # Códigos prácticos
```

## 🎓 Contenido Académico

### 📚 **Unidades del Curso**
1. **Unidad 01**: Muestreo, Reconstrucción y Cuantización
2. **Unidad 02**: Sistemas de Tiempo Discreto  
3. **Unidad 03**: Transformadas de Fourier
4. **Unidad 04**: Diseño de Filtros Digitales
5. **Unidad 05**: Técnicas Avanzadas

### 🎯 **Por Cada Clase**
- **PDF teórico** con conceptos y fórmulas
- **Código Python** con ejemplos prácticos
- **Ejercicios interactivos** para experimentar
- **Visualizaciones** de señales y transformadas

## 🤝 Contribuir

### 🐛 **Reportar Bugs**
1. Verifica que no exista el issue
2. Incluye pasos para reproducir
3. Especifica versión de Windows
4. Adjunta screenshots si es relevante

### ✨ **Nuevas Características**
1. Fork del repositorio
2. Crea branch feature/nueva-funcionalidad
3. Commit con mensajes descriptivos
4. Pull request con descripción detallada

### 🔧 **Desarrollo Local**
```bash
git clone https://github.com/MaximilianoAntonio/Biomedical-DSP.git
cd Biomedical-DSP
pip install -r requirements.txt
python main.py
```

## 📄 Licencia

```
MIT License - Uso libre para fines educativos y comerciales
Ver LICENSE para detalles completos
```

## 👤 Autor

**Maximiliano Antonio**
- 🐱 GitHub: [@MaximilianoAntonio](https://github.com/MaximilianoAntonio)
- 📧 Email: [maximiliano.antonio@ejemplo.com]
- 🌐 LinkedIn: [Maximiliano Antonio]

## 🙏 Agradecimientos

- 🎓 Universidad por el contenido académico
- 🐍 Comunidad Python por las excelentes librerías
- 🎨 CustomTkinter por la interfaz moderna
- 📄 PyMuPDF por el visor PDF integrado

---

⭐ **¡Si te resulta útil, dale una estrella al repositorio!** ⭐

🚀 **¿Encontraste un bug o tienes una idea? ¡Abre un issue!** 🚀
