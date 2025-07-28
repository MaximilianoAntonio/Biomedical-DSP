# Biomedical Digital Signal Processing

Una aplicación de escritorio moderna para estudiar Procesamiento Digital de Señales Biomédicas.

## 🚀 Características

- **Navegación intuitiva** por unidades y clases del curso
- **Indicador de clase activa** con destacado visual
- **Visualización de PDFs** con opción de pantalla completa
- **Editor de código Python** integrado con resaltado de sintaxis
- **Ejecución de código** en tiempo real con salida en vivo
- **Interfaz moderna** con tema oscuro
- **Ejecutable portátil** - no requiere instalación

## 📦 Instalación Rápida

### Para Usuarios (Solo ejecutar)

1. Descarga el archivo `Biomedical-DSP.exe` desde releases
2. Ejecuta `Biomedical-DSP.exe` (no requiere instalación)
3. ¡Disfruta aprendiendo DSP!

### Para Desarrolladores

1. Clona este repositorio
2. Ejecuta `install.bat` para instalación automática
3. Ejecuta `python main.py` para probar
4. Ejecuta `python -m PyInstaller biomedical_dsp.spec` para generar el ejecutable

## 🎯 Cómo Usar

1. **Navegar**: Usa el panel izquierdo para seleccionar unidades y clases
2. **Clase Seleccionada**: El indicador superior muestra qué clase está activa
3. **Ver PDFs**: En la pestaña "📄 Material PDF", haz clic en "Pantalla Completa" para mejor vista
4. **Código**: En la pestaña "💻 Código Python", puedes ver y editar el código
5. **Ejecutar**: En la pestaña "▶️ Ejecutar Código", ejecuta el código y ve los resultados

## 📋 Requisitos del Sistema

- Windows 10 o superior
- Visor de PDF instalado (para visualización de documentos)
- **No requiere Python** para el ejecutable

## 🛠️ Dependencias (Solo para desarrollo)

- `customtkinter` - Interfaz moderna
- `tkinter` - GUI base
- `PyPDF2` - Manejo de PDFs
- `matplotlib`, `numpy`, `scipy` - Para los ejemplos de DSP
- `pyinstaller` - Para generar ejecutables

## 📁 Estructura del Proyecto

```
Biomedical-DSP/
├── main.py                    # Aplicación principal
├── requirements.txt           # Dependencias Python
├── setup.bat                 # Script de instalación
├── build_exe.bat            # Script para generar ejecutable
├── icon.ico                 # Icono de la aplicación
├── Unidad 01 Muestreo-reconstrucción-cuantiación/
│   ├── Clase 01 Analógico-muestreo.pdf
│   ├── Clase 01- Señales analógicas y muestreo.py
│   └── ...
├── Unidad 02 Sistemas de tiempo discreto/
├── Unidad 03 Transformadas de Fourier/
├── Unidad 04 Diseño de filtros digitales/
└── Unidad 05 Técnicas avanzadas/
```

## 🎨 Capturas de Pantalla

La aplicación cuenta con:
- **Panel de navegación** organizado por unidades
- **Visor de PDFs** integrado con controles
- **Editor de código** con sintaxis destacada
- **Consola de ejecución** con salida en tiempo real

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Maximiliano Antonio**
- GitHub: [@MaximilianoAntonio](https://github.com/MaximilianoAntonio)

## 📞 Soporte

Si tienes problemas o sugerencias:
1. Revisa la sección de [Issues](https://github.com/MaximilianoAntonio/Biomedical-DSP/issues)
2. Crea un nuevo issue si no encuentras tu problema
3. Proporciona detalles sobre tu sistema y el error

---

**¡Feliz aprendizaje de DSP! 🧠📊**
