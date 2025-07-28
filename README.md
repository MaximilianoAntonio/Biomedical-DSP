# Procesamiento Digital de Señales Biomédicas

Una aplicación de escritorio moderna para estudiar Procesamiento Digital de Señales Biomédicas. Esta herramienta educativa integral proporciona un entorno de aprendizaje intuitivo para conceptos de DSP con materiales de curso integrados, ejemplos de código y características interactivas.

## Características

- **Navegación Intuitiva**: Unidades de curso y clases organizadas con navegación jerárquica
- **Indicador de Clase Activa**: Resaltado visual del material de curso actualmente seleccionado
- **Visor de PDF Integrado**: Visualización de documentos en pantalla completa con controles integrados
- **Editor de Código Python**: Editor con resaltado de sintaxis y manipulación avanzada de texto
- **Ejecución de Código en Tiempo Real**: Ejecución de código en vivo con visualización de salida y manejo de errores
- **Interfaz Oscura Moderna**: Diseño de UI profesional optimizado para sesiones de estudio extendidas
- **Ejecutable Portátil**: Aplicación independiente que no requiere instalación
- **Procesamiento Multi-hilo**: Ejecución de código no bloqueante preservando la capacidad de respuesta de la UI

## Instalación

### Usuarios Finales

1. Descarga `Biomedical-DSP.exe` desde la última versión
2. Ejecuta el archivo directamente (no requiere instalación)
3. Comienza a explorar los materiales del curso inmediatamente

### Desarrolladores

1. Clona este repositorio:
   ```bash
   git clone https://github.com/MaximilianoAntonio/Biomedical-DSP.git
   cd Biomedical-DSP
   ```

2. Instala las dependencias automáticamente:
   ```bash
   install.bat
   ```

3. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

4. Construye el ejecutable (opcional):
   ```bash
   python -m PyInstaller biomedical_dsp.spec
   ```

## Guía de Uso

### Navegación
- Usa el panel izquierdo para navegar por las unidades del curso y clases individuales
- El indicador superior muestra la selección de clase actualmente activa
- Los materiales del curso se agrupan automáticamente por número de clase para fácil acceso

### Visualización de PDF
- Accede a los documentos del curso a través de la pestaña "Material PDF"
- Haz clic en "Pantalla Completa" para una experiencia de lectura sin distracciones
- Controles de PDF integrados para navegación y zoom

### Desarrollo de Código
- Ve y edita ejemplos de Python en la pestaña "Código Python"
- El resaltado de sintaxis soporta el flujo de trabajo de desarrollo Python
- Los ejemplos de código demuestran conceptos e implementaciones clave de DSP

### Ejecución de Código
- Ejecuta código a través de la pestaña "Ejecutar Código"
- Visualización de salida en tiempo real con resultados formateados
- Manejo de errores con información detallada de rastreo
- La ejecución multi-hilo previene el congelamiento de la UI

## Requisitos del Sistema

- **Sistema Operativo**: Windows 10 o posterior
- **Visor de PDF**: Aplicación PDF predeterminada del sistema (para visualización externa de documentos)
- **Runtime de Python**: No requerido para la versión ejecutable
- **Memoria**: Mínimo 4GB RAM recomendado
- **Almacenamiento**: 100MB de espacio libre en disco

## Dependencias de Desarrollo

- **customtkinter**: Marco de UI moderno con soporte de tema oscuro
- **tkinter**: Conjunto de herramientas GUI base para aplicaciones Python
- **PyPDF2**: Procesamiento y manipulación de documentos PDF
- **matplotlib**: Gráficos científicos y visualización
- **numpy**: Fundación de computación numérica
- **scipy**: Algoritmos avanzados de computación científica
- **PyInstaller**: Generación y empaquetado de ejecutables

## Estructura del Proyecto

```
Biomedical-DSP/
├── main.py                     # Punto de entrada principal de la aplicación
├── utils.py                    # Funciones de utilidad y ayudantes
├── requirements.txt            # Dependencias de Python
├── biomedical_dsp.spec        # Configuración de PyInstaller
├── install.bat                # Instalador automático de dependencias
├── test_app.py               # Script de pruebas locales
├── test_app_ci.py            # Pruebas compatibles con CI/CD
├── README.md                 # Documentación del proyecto
├── .github/workflows/        # CI/CD de GitHub Actions
├── dist/                     # Salida de ejecutable generado
└── [Materiales del Curso]/   # Contenido educativo organizado por unidades
```

## Flujo de Trabajo de Desarrollo

### Pruebas Locales
Ejecuta pruebas comprehensivas de la aplicación:
```bash
python test_app.py
```

### Integración Continua
Pruebas compatibles con GitHub Actions:
```bash
python test_app_ci.py
```

### Generación de Ejecutable
Crea paquete de aplicación independiente:
```bash
python -m PyInstaller biomedical_dsp.spec
```

### Aseguramiento de Calidad de Código
El proyecto incluye pruebas automatizadas para:
- Inicialización de componentes GUI
- Operaciones del sistema de archivos
- Capacidades de procesamiento de PDF
- Funcionalidad de ejecución de código
- Robustez del manejo de errores

## Resumen de Arquitectura

La aplicación sigue un patrón de arquitectura modular:

- **Aplicación Principal** (`main.py`): Implementación GUI principal usando CustomTkinter
- **Capa de Utilidades** (`utils.py`): Operaciones de archivos multiplataforma e integración del sistema
- **Contenido del Curso**: Materiales educativos estructurados con descubrimiento automático
- **Sistema de Construcción**: Generación automática de ejecutables con empaquetado de dependencias

### Componentes Clave

1. **Clase BiomedicaDSPApp**: Controlador principal de la aplicación que gestiona el estado de UI e interacciones del usuario
2. **Descubrimiento de Contenido**: Agrupación inteligente de archivos y organización de materiales del curso
3. **Interfaz Multi-pestaña**: Navegación por pestañas para diferentes funciones de la aplicación
4. **Gestión de Hilos**: Ejecución de código no bloqueante con manejo apropiado de recursos

## Características de la Aplicación

### Gestión de Contenido Educativo
- Detección automática y agrupación de materiales del curso
- Asociación inteligente de archivos entre PDFs y scripts de Python
- Navegación jerárquica soportando estructura de curso multi-nivel

### Entorno de Aprendizaje Interactivo
- Entorno de desarrollo Python integrado
- Ejecución de código en tiempo real con captura de salida
- Manejo de errores con retroalimentación educativa
- Resaltado de sintaxis para mejorar la legibilidad del código

### Diseño de Experiencia de Usuario
- Tema oscuro moderno reduciendo la fatiga visual durante uso extendido
- Diseño responsivo adaptándose a diferentes tamaños de pantalla
- Navegación intuitiva minimizando la curva de aprendizaje
- Interfaz profesional adecuada para entornos académicos

## Contribuciones

Damos la bienvenida a contribuciones de la comunidad. Para contribuir:

1. **Hacer Fork del Repositorio**: Crea tu propia copia del proyecto
2. **Crear Rama de Característica**: 
   ```bash
   git checkout -b feature/NombreDeTuCaracteristica
   ```
3. **Implementar Cambios**: Añade tus mejoras con pruebas apropiadas
4. **Confirmar Cambios**: 
   ```bash
   git commit -m "Añadir descripción comprensiva de la característica"
   ```
5. **Empujar a la Rama**: 
   ```bash
   git push origin feature/NombreDeTuCaracteristica
   ```
6. **Enviar Pull Request**: Abre un pull request detallado con descripción de cambios

### Pautas de Contribución
- Sigue el estilo de código y convenciones existentes
- Incluye pruebas comprensivas para nueva funcionalidad
- Actualiza la documentación para cualquier nueva característica
- Asegura compatibilidad con entornos Windows 10+

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para detalles completos.

La Licencia MIT proporciona:
- Libertad para usar, modificar y distribuir
- Permisos de uso comercial y privado
- Sin obligaciones de responsabilidad o garantía
- Requisito de preservación de atribución

## Autor

**Maximiliano Antonio**
- **GitHub**: [@MaximilianoAntonio](https://github.com/MaximilianoAntonio)
- **Proyecto**: Plataforma Educativa de Procesamiento Digital de Señales Biomédicas

## Soporte y Documentación

### Obtener Ayuda
Para soporte técnico y preguntas:

1. **Revisar Issues Existentes**: Revisa [GitHub Issues](https://github.com/MaximilianoAntonio/Biomedical-DSP/issues) para problemas similares
2. **Crear Nuevo Issue**: Envía reportes de errores detallados o solicitudes de características
3. **Proporcionar Información del Sistema**: Incluye versión del SO, versión de Python y detalles del error
4. **Discusión Comunitaria**: Interactúa con otros usuarios y contribuidores

### Pautas para Reportar Issues
Al reportar problemas, por favor incluye:
- Versión del sistema operativo y arquitectura
- Versión de la aplicación o hash del commit
- Instrucciones de reproducción paso a paso
- Comportamiento esperado vs. real
- Capturas de pantalla o logs de error cuando sea aplicable

### Solicitudes de Características
Alentamos sugerencias de características que mejoren la experiencia educativa:
- Implementaciones adicionales de algoritmos DSP
- Capacidades de visualización mejoradas
- Elementos de interfaz de usuario mejorados
- Soporte extendido de materiales del curso

---

**Plataforma Educativa de Procesamiento Digital de Señales Biomédicas**
*Avanzando la educación en ingeniería biomédica a través de herramientas de aprendizaje interactivas*
