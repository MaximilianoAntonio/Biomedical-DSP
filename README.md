# Procesamiento Digital de Señales Biomédicas

Una aplicación de escritorio para estudiar Procesamiento Digital de Señales Biomédicas con materiales de curso integrados, visor PDF integrado y ejecución de código interactiva.

## 🚀 Descarga Rápida

### Opción 1: Descargar Release (Recomendado)
1. Ve a la página de [Releases](https://github.com/MaximilianoAntonio/Biomedical-DSP/releases)
2. Descarga la versión más reciente: `Biomedical-DSP.exe`
3. Ejecuta el archivo directamente - **¡No requiere instalación!**

### Opción 2: Para Desarrolladores
```bash
git clone https://github.com/MaximilianoAntonio/Biomedical-DSP.git
cd Biomedical-DSP
install.bat
python main.py
```

## ✨ Características 

- 📚 **Navegación Intuitiva**: Unidades de curso organizadas jerárquicamente
- 📄 **Visor PDF Integrado**: PDFs directamente en la aplicación con zoom y navegación
- 💻 **Editor Python**: Resaltado de sintaxis y ejecución en tiempo real
- 🎨 **Interfaz Moderna**: Tema oscuro optimizado para estudio prolongado
- 📦 **Ejecutable Portátil**: Sin instalación requerida
- ⚡ **Multi-hilo**: Ejecución no bloqueante
- ⌨️ **Atajos de Teclado**: Navegación rápida y eficiente

## 🎯 Uso Rápido

1. **Navegación**: Panel izquierdo para explorar unidades y clases
2. **PDFs**: Pestaña "Material PDF" - ¡Ahora con visor integrado!
   - Navegación con botones o flechas del teclado
   - Zoom con botones o Ctrl + scroll
   - Click para avanzar/retroceder páginas
3. **Código**: Pestaña "Código Python" para ejemplos editables
4. **Ejecución**: Pestaña "Ejecutar Código" para ver resultados

## ⌨️ Atajos de Teclado

- **← →**: Navegar páginas del PDF
- **↑ ↓**: Zoom del PDF
- **Ctrl + O**: Abrir PDF en aplicación externa
- **Ctrl + S**: Guardar código
- **F5**: Ejecutar código
- **Ctrl + 0**: Resetear zoom

## 📋 Requisitos

- Windows 10 o posterior
- 4GB RAM mínimo
- 200MB espacio libre

## 🛠️ Para Desarrolladores

### Dependencias
- `customtkinter`, `PyMuPDF`, `Pillow`, `matplotlib`, `numpy`, `scipy`

### Construcción
```bash
pip install -r requirements.txt
python -m PyInstaller biomedical_dsp.spec
```

### Pruebas
```bash
python test_app.py
```

## Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

## Autor

**Maximiliano Antonio** - [@MaximilianoAntonio](https://github.com/MaximilianoAntonio)
