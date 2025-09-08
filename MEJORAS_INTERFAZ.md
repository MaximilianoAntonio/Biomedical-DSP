# 🎨 Mejoras de Interfaz y Temas - Biomedical DSP

## ✨ Nuevas Características

### 🌗 Sistema de Temas Dinámico
- **Detección automática del tema del sistema** (Windows/macOS/Linux)
- **Cambio en vivo** entre modo claro y oscuro
- **Persistencia de preferencias** - recuerda tu tema favorito
- **3 esquemas de color**: Azul, Verde, Azul Oscuro

### 🔤 Sistema de Fuentes Mejorado
- **Fuentes específicas por OS**:
  - Windows: Segoe UI + Consolas
  - macOS: SF Pro Display + Monaco  
  - Linux: Ubuntu + Ubuntu Mono
- **Fallback automático** si las fuentes no están disponibles
- **Diferentes tamaños** optimizados para cada elemento de la UI

### 🎯 Mejoras de Usabilidad
- **Controles de tema en la interfaz**: Botón toggle y menú de colores
- **Mejor organización visual**: Espaciado y bordes redondeados
- **Scrollbars mejoradas**: Más anchas y visibles
- **Colores dinámicos**: Se adaptan automáticamente al tema

## 🚀 Cómo Usar las Nuevas Características

### Cambiar Tema Claro/Oscuro
1. Usa el botón **"☀️ Modo Claro"** / **"🌙 Modo Oscuro"** en la parte superior
2. El cambio es inmediato y se guarda automáticamente

### Cambiar Esquema de Color
1. Usa el menú desplegable **"Color"** junto al botón de tema
2. Selecciona entre: `blue`, `green`, `dark-blue`
3. Se aplicará al reiniciar (la app pregunta si quieres reiniciar)

### Preferencias Guardadas
- Las preferencias se guardan en `config/theme_config.txt`
- Se cargan automáticamente al iniciar la aplicación
- Compatible con ejecutables empaquetados

## 🔧 Requisitos Actualizados

### Dependencias Principales
```
customtkinter>=5.2.2    # Versión más reciente
Pillow>=10.0.0          # Mejor soporte de imágenes
matplotlib>=3.7.0       # Mejor integración con temas
```

### Dependencias Opcionales
```
darkdetect>=0.8.0       # Detección automática de tema del sistema
```

## 🎨 Personalización Avanzada

### Colores por Tema
- **Modo Oscuro**: Fondos grises oscuros, texto claro
- **Modo Claro**: Fondos blancos/grises claros, texto oscuro
- **Canvas**: Se adapta dinámicamente al tema actual

### Fuentes Configurables
```python
self.fonts = {
    'title': ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
    'subtitle': ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
    'header': ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
    'body': ctk.CTkFont(family="Segoe UI", size=14),
    'code': ctk.CTkFont(family="Consolas", size=12),
    # ... más fuentes
}
```

## 🛠️ Compatibilidad

### Sistemas Operativos
- ✅ Windows 10/11 (Segoe UI + Consolas)
- ✅ macOS (SF Pro Display + Monaco)
- ✅ Linux (Ubuntu + Ubuntu Mono)

### Resoluciones
- ✅ 1920x1080 y superiores (recomendado)
- ✅ 1366x768 (mínimo soportado)
- ✅ Pantallas HiDPI/Retina

## 🔍 Solución de Problemas

### Si las fuentes no se cargan correctamente:
- La aplicación usa fuentes de fallback automáticamente
- Verifica que las fuentes del sistema estén instaladas

### Si el tema no se detecta automáticamente:
- Instala `darkdetect`: `pip install darkdetect`
- O usa los controles manuales en la interfaz

### Si las preferencias no se guardan:
- Verifica permisos de escritura en la carpeta de la aplicación
- Las preferencias se guardan en `config/theme_config.txt`

## 📸 Capturas de Pantalla

### Modo Oscuro (Tema Azul)
- Fondo gris oscuro con acentos azules
- Texto claro para mejor legibilidad
- Sintaxis highlighting en editor de código

### Modo Claro (Tema Verde)
- Fondo blanco/gris claro con acentos verdes
- Texto oscuro para mejor contraste
- Interfaz limpia y moderna

---

## 🏗️ Arquitectura de Temas

La nueva arquitectura de temas está diseñada para ser:
- **Extensible**: Fácil agregar nuevos temas
- **Mantenible**: Código organizado y documentado
- **Compatible**: Funciona con todas las características existentes
- **Performante**: Cambios de tema instantáneos

¡Disfruta de la nueva experiencia visual mejorada! 🎉
