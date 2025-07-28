# Procesamiento Digital de Señales Biomédicas

Una aplicación de escritorio para estudiar Procesamiento Digital de Señales Biomédicas con materiales de curso integrados y ejecución de código interactiva.

##  Descarga Rápida

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

##  Características 

-  **Navegación Intuitiva**: Unidades de curso organizadas jerárquicamente
- **Visor PDF**: Documentos en pantalla completa
-  **Editor Python**: Resaltado de sintaxis y ejecución en tiempo real
- **Interfaz**: Tema oscuro optimizado para estudio
- **Ejecutable Portátil**: Sin instalación requerida
- **Multi-hilo**: Ejecución no bloqueante

## Uso Rápido

1. **Navegación**: Panel izquierdo para explorar unidades y clases
2. **PDFs**: Pestaña "Material PDF" para documentos del curso
3. **Código**: Pestaña "Código Python" para ejemplos editables
4. **Ejecución**: Pestaña "Ejecutar Código" para ver resultados

## Requisitos

- Windows 10 o posterior
- 4GB RAM mínimo
- 100MB espacio libre

## 🛠️ Para Desarrolladores

### Dependencias
- `customtkinter`, `matplotlib`, `numpy`, `scipy`, `PyPDF2`

### Construcción
```bash
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
