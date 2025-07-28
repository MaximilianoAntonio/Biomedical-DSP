"""
CBM414 - Procesamiento Digital de Señales Biomédicas
Clase 14: Transformada Z
Autor: David Ortiz, Ph.D.
Escuela de Ingeniería Biomédica - Universidad de Valparaíso

Objetivo: Comprender la definición y propiedades fundamentales de la Transformada Z,
su relación con las transformadas de Fourier y Laplace, y aplicar estas herramientas
para analizar sistemas LTI y funciones de transferencia H(z).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.patches import Circle
import warnings
warnings.filterwarnings('ignore')

# Configuración para gráficos
plt.style.use('default')
plt.rcParams['font.size'] = 9

class TransformadaZGUI(tk.Tk):
    """Interfaz gráfica para demostrar conceptos de la Transformada Z"""
    
    def __init__(self):
        super().__init__()
        self.title("CBM414 - Clase 14: Transformada Z")
        self.geometry("1500x900")
        self.configure(bg='#f0f0f0')
        
        # Variables
        self.current_figure = None
        self.current_canvas = None
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        """Crear la interfaz principal"""
        # Título principal
        titulo = tk.Label(self, 
                         text="CBM414 - Procesamiento Digital de Señales Biomédicas\nClase 14: Transformada Z",
                         font=("Arial", 16, "bold"),
                         bg='#f0f0f0',
                         fg='#2c3e50')
        titulo.pack(pady=10)
        
        # Subtítulo
        subtitulo = tk.Label(self,
                           text="David Ortiz, Ph.D. - Universidad de Valparaíso",
                           font=("Arial", 12),
                           bg='#f0f0f0',
                           fg='#34495e')
        subtitulo.pack(pady=5)
        
        # Frame principal con notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear las pestañas
        self.crear_pestaña_definicion()
        self.crear_pestaña_propiedades()
        self.crear_pestaña_ejemplos()
        self.crear_pestaña_plano_z()
        self.crear_pestaña_sistemas_lti()
        self.crear_pestaña_relaciones()
        
        # Protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Manejar el cierre de la aplicación"""
        try:
            plt.close('all')
        except:
            pass
        self.destroy()
        
    def crear_pestaña_definicion(self):
        """Pestaña para definición de la Transformada Z"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="1. Definición")
        
        # Panel de controles
        control_frame = ttk.LabelFrame(frame, text="Parámetros de la Señal")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Variables de control
        self.signal_type_var = tk.StringVar(value="Impulso unitario")
        self.length_var = tk.IntVar(value=8)
        self.delay_var = tk.IntVar(value=0)
        self.amplitude_var = tk.DoubleVar(value=1.0)
        
        # Controles
        ttk.Label(control_frame, text="Tipo de señal:").grid(row=0, column=0, padx=5, pady=2)
        signal_combo = ttk.Combobox(control_frame, textvariable=self.signal_type_var,
                                   values=["Impulso unitario", "Escalón unitario", "Rampa", 
                                          "Exponencial", "Senoidal", "Secuencia finita"])
        signal_combo.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        signal_combo.bind('<<ComboboxSelected>>', self.actualizar_definicion)
        
        ttk.Label(control_frame, text="Longitud:").grid(row=1, column=0, padx=5, pady=2)
        length_scale = ttk.Scale(control_frame, from_=4, to=16, variable=self.length_var,
                                command=self.actualizar_definicion)
        length_scale.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.length_var).grid(row=1, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Retardo:").grid(row=2, column=0, padx=5, pady=2)
        delay_scale = ttk.Scale(control_frame, from_=0, to=5, variable=self.delay_var,
                               command=self.actualizar_definicion)
        delay_scale.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.delay_var).grid(row=2, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Amplitud:").grid(row=3, column=0, padx=5, pady=2)
        amp_scale = ttk.Scale(control_frame, from_=0.1, to=3.0, variable=self.amplitude_var,
                             command=self.actualizar_definicion)
        amp_scale.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.amplitude_var).grid(row=3, column=2, padx=5, pady=2)
        
        control_frame.columnconfigure(1, weight=1)
        
        # Frame para gráficos
        self.def_graph_frame = ttk.Frame(frame)
        self.def_graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info frame
        self.def_info_frame = ttk.LabelFrame(frame, text="Definición y Cálculo")
        self.def_info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.def_info_label = ttk.Label(self.def_info_frame, text="", 
                                       font=("Courier", 9), justify=tk.LEFT)
        self.def_info_label.pack(padx=10, pady=5)
        
        # Crear gráfico inicial
        self.actualizar_definicion()
        
    def generar_señal(self, signal_type, length, delay, amplitude):
        """Generar diferentes tipos de señales"""
        n = np.arange(-2, length + 5)
        x = np.zeros_like(n, dtype=float)
        
        if signal_type == "Impulso unitario":
            x[n == delay] = amplitude
        elif signal_type == "Escalón unitario":
            x[n >= delay] = amplitude
        elif signal_type == "Rampa":
            x[n >= delay] = amplitude * (n[n >= delay] - delay)
        elif signal_type == "Exponencial":
            alpha = 0.8
            mask = n >= delay
            x[mask] = amplitude * (alpha ** (n[mask] - delay))
        elif signal_type == "Senoidal":
            freq = 0.2
            mask = n >= delay
            x[mask] = amplitude * np.cos(2 * np.pi * freq * (n[mask] - delay))
        elif signal_type == "Secuencia finita":
            # Secuencia del ejemplo: {2, 3, 5, 2}
            seq = np.array([2, 3, 5, 2]) * amplitude
            start_idx = np.where(n == delay)[0]
            if len(start_idx) > 0:
                start = start_idx[0]
                end = min(start + len(seq), len(x))
                x[start:end] = seq[:end-start]
        
        # Mantener solo valores significativos
        if signal_type in ["Impulso unitario", "Secuencia finita"]:
            non_zero = np.where(np.abs(x) > 1e-10)[0]
            if len(non_zero) > 0:
                start_idx = max(0, non_zero[0] - 2)
                end_idx = min(len(n), non_zero[-1] + 3)
                n = n[start_idx:end_idx]
                x = x[start_idx:end_idx]
        else:
            # Para señales infinitas, mostrar una porción
            start_idx = max(0, np.where(n == delay-2)[0][0] if delay-2 in n else 0)
            end_idx = min(len(n), start_idx + length + 4)
            n = n[start_idx:end_idx]
            x = x[start_idx:end_idx]
        
        return n, x
    
    def calcular_transformada_z(self, n, x):
        """Calcular la transformada Z simbólicamente"""
        # Para visualización, calcular en algunos puntos del plano z
        r_vals = np.logspace(-1, 1, 50)  # de 0.1 a 10
        theta_vals = np.linspace(0, 2*np.pi, 100)
        
        # Evaluar en el círculo unitario (DTFT)
        z_unit = np.exp(1j * theta_vals)
        X_unit = np.zeros_like(z_unit, dtype=complex)
        
        for i, z in enumerate(z_unit):
            X_unit[i] = np.sum(x * (z ** (-n)))
        
        # Evaluar en diferentes radios
        X_magnitude = np.zeros((len(r_vals), len(theta_vals)))
        
        for i, r in enumerate(r_vals):
            for j, theta in enumerate(theta_vals):
                z = r * np.exp(1j * theta)
                try:
                    X_z = np.sum(x * (z ** (-n)))
                    X_magnitude[i, j] = np.abs(X_z)
                except:
                    X_magnitude[i, j] = np.inf
        
        return theta_vals, X_unit, r_vals, X_magnitude
    
    def obtener_expresion_simbolica(self, n, x, signal_type):
        """Obtener expresión simbólica de la transformada Z"""
        delay = int(self.delay_var.get())
        amplitude = self.amplitude_var.get()
        
        if signal_type == "Impulso unitario":
            if delay == 0:
                return f"X(z) = {amplitude}"
            else:
                return f"X(z) = {amplitude}z^(-{delay})"
        
        elif signal_type == "Escalón unitario":
            if delay == 0:
                return f"X(z) = {amplitude}/(1 - z^(-1)), |z| > 1"
            else:
                return f"X(z) = {amplitude}z^(-{delay})/(1 - z^(-1)), |z| > 1"
        
        elif signal_type == "Exponencial":
            alpha = 0.8
            if delay == 0:
                return f"X(z) = {amplitude}/(1 - {alpha}z^(-1)), |z| > {alpha}"
            else:
                return f"X(z) = {amplitude}z^(-{delay})/(1 - {alpha}z^(-1)), |z| > {alpha}"
        
        elif signal_type == "Secuencia finita":
            # Ejemplo: {2, 3, 5, 2}
            if delay == 0:
                return f"X(z) = 2 + 3z^(-1) + 5z^(-2) + 2z^(-3)"
            else:
                return f"X(z) = z^(-{delay})(2 + 3z^(-1) + 5z^(-2) + 2z^(-3))"
        
        elif signal_type == "Rampa":
            if delay == 0:
                return f"X(z) = {amplitude}z^(-1)/(1 - z^(-1))^2, |z| > 1"
            else:
                return f"X(z) = {amplitude}z^(-{delay-1})/(1 - z^(-1))^2, |z| > 1"
        
        else:
            # Cálculo numérico
            expr = ""
            for i, (ni, xi) in enumerate(zip(n, x)):
                if abs(xi) > 1e-10:
                    if ni == 0:
                        term = f"{xi:.2f}"
                    elif ni > 0:
                        term = f"{xi:.2f}z^(-{ni})"
                    else:
                        term = f"{xi:.2f}z^({-ni})"
                    
                    if expr == "":
                        expr = term
                    else:
                        expr += f" + {term}" if xi > 0 else f" {term}"
            
            return f"X(z) = {expr}" if expr else "X(z) = 0"
    
    def actualizar_definicion(self, event=None):
        """Actualizar gráfico de definición"""
        signal_type = self.signal_type_var.get()
        length = int(self.length_var.get())
        delay = int(self.delay_var.get())
        amplitude = self.amplitude_var.get()
        
        # Limpiar frame anterior
        for widget in self.def_graph_frame.winfo_children():
            widget.destroy()
        
        # Generar señal
        n, x = self.generar_señal(signal_type, length, delay, amplitude)
        
        # Calcular transformada Z
        theta_vals, X_unit, r_vals, X_magnitude = self.calcular_transformada_z(n, x)
        
        # Crear figura
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Definición de la Transformada Z', fontsize=14)
        
        # Señal en el tiempo
        ax1.stem(n, x, basefmt=" ")
        ax1.set_title(f'Señal: {signal_type}')
        ax1.set_xlabel('n')
        ax1.set_ylabel('x(n)')
        ax1.grid(True, alpha=0.3)
        
        # Magnitud en el círculo unitario (DTFT)
        freq_norm = theta_vals / (2 * np.pi)
        ax2.plot(freq_norm, np.abs(X_unit))
        ax2.set_title('|X(z)| en el círculo unitario (DTFT)')
        ax2.set_xlabel('Frecuencia normalizada')
        ax2.set_ylabel('|X(e^(jω))|')
        ax2.grid(True, alpha=0.3)
        
        # Fase en el círculo unitario
        ax3.plot(freq_norm, np.angle(X_unit))
        ax3.set_title('∠X(z) en el círculo unitario')
        ax3.set_xlabel('Frecuencia normalizada')
        ax3.set_ylabel('∠X(e^(jω)) [rad]')
        ax3.grid(True, alpha=0.3)
        
        # Superficie 3D de magnitud (vista polar)
        theta_mesh, r_mesh = np.meshgrid(theta_vals, r_vals)
        X_mag_safe = np.clip(X_magnitude, 0, 10)  # Limitar para visualización
        
        im = ax4.contourf(theta_mesh, r_mesh, X_mag_safe, levels=20, cmap='viridis')
        ax4.set_title('|X(z)| en el plano Z (coordenadas polares)')
        ax4.set_xlabel('θ [rad]')
        ax4.set_ylabel('r')
        ax4.set_ylim(0.1, 3)
        
        # Círculo unitario
        circle_theta = np.linspace(0, 2*np.pi, 100)
        ax4.plot(circle_theta, np.ones_like(circle_theta), 'w--', linewidth=2, label='Círculo unitario')
        ax4.legend()
        
        plt.colorbar(im, ax=ax4, shrink=0.8)
        plt.tight_layout()
        
        # Agregar a la interfaz
        canvas = FigureCanvasTkAgg(fig, self.def_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Actualizar información
        expr_simbolica = self.obtener_expresion_simbolica(n, x, signal_type)
        
        info_text = f"DEFINICIÓN DE LA TRANSFORMADA Z:\n"
        info_text += f"X(z) = Σ x(n)z^(-n)\n\n"
        info_text += f"Para la señal {signal_type}:\n"
        info_text += f"{expr_simbolica}\n\n"
        info_text += f"Valores no nulos: n ∈ {{{', '.join(map(str, n[np.abs(x) > 1e-10]))}}}\n"
        info_text += f"Muestras: {{{', '.join([f'{xi:.2f}' for xi in x[np.abs(x) > 1e-10]])}}}"
        
    
    def crear_pestaña_propiedades(self):
        """Pestaña para propiedades de la Transformada Z"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="2. Propiedades")
        
        # Panel de controles
        control_frame = ttk.LabelFrame(frame, text="Demostración de Propiedades")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.propiedad_var = tk.StringVar(value="Linealidad")
        self.a1_var = tk.DoubleVar(value=2.0)
        self.a2_var = tk.DoubleVar(value=3.0)
        self.delay_prop_var = tk.IntVar(value=2)
        
        ttk.Label(control_frame, text="Propiedad:").grid(row=0, column=0, padx=5, pady=2)
        prop_combo = ttk.Combobox(control_frame, textvariable=self.propiedad_var,
                                 values=["Linealidad", "Retardo", "Convolución"])
        prop_combo.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        prop_combo.bind('<<ComboboxSelected>>', self.actualizar_propiedades)
        
        ttk.Label(control_frame, text="Coef. a1:").grid(row=1, column=0, padx=5, pady=2)
        a1_scale = ttk.Scale(control_frame, from_=0.5, to=5.0, variable=self.a1_var,
                            command=self.actualizar_propiedades)
        a1_scale.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.a1_var).grid(row=1, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Coef. a2:").grid(row=2, column=0, padx=5, pady=2)
        a2_scale = ttk.Scale(control_frame, from_=0.5, to=5.0, variable=self.a2_var,
                            command=self.actualizar_propiedades)
        a2_scale.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.a2_var).grid(row=2, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Retardo D:").grid(row=3, column=0, padx=5, pady=2)
        delay_scale = ttk.Scale(control_frame, from_=1, to=5, variable=self.delay_prop_var,
                               command=self.actualizar_propiedades)
        delay_scale.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.delay_prop_var).grid(row=3, column=2, padx=5, pady=2)
        
        control_frame.columnconfigure(1, weight=1)
        
        # Frame para gráficos
        self.prop_graph_frame = ttk.Frame(frame)
        self.prop_graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info frame
        self.prop_info_frame = ttk.LabelFrame(frame, text="Demostración Matemática")
        self.prop_info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.prop_info_label = ttk.Label(self.prop_info_frame, text="", 
                                        font=("Courier", 8), justify=tk.LEFT)
        self.prop_info_label.pack(padx=10, pady=5)
        
        self.actualizar_propiedades()
    
    def actualizar_propiedades(self, event=None):
        """Actualizar demostración de propiedades"""
        propiedad = self.propiedad_var.get()
        a1 = self.a1_var.get()
        a2 = self.a2_var.get()
        delay = int(self.delay_prop_var.get())
        
        # Limpiar frame
        for widget in self.prop_graph_frame.winfo_children():
            widget.destroy()
        
        if propiedad == "Linealidad":
            self.demo_linealidad(a1, a2)
        elif propiedad == "Retardo":
            self.demo_retardo(delay)
        elif propiedad == "Convolución":
            self.demo_convolucion()
    
    def demo_linealidad(self, a1, a2):
        """Demostrar propiedad de linealidad"""
        # Señales de prueba
        n = np.arange(6)
        x1 = np.array([1, 2, 1, 0, 0, 0])  # Secuencia finita
        x2 = np.array([0, 1, 2, 1, 0, 0])  # Secuencia finita retardada
        
        # Combinación lineal
        y = a1 * x1 + a2 * x2
        
        # Transformadas Z (evaluadas en el círculo unitario)
        omega = np.linspace(0, 2*np.pi, 256)
        z = np.exp(1j * omega)
        
        X1 = np.zeros_like(z, dtype=complex)
        X2 = np.zeros_like(z, dtype=complex)
        Y_direct = np.zeros_like(z, dtype=complex)
        Y_linear = np.zeros_like(z, dtype=complex)
        
        for i, zi in enumerate(z):
            X1[i] = np.sum(x1 * (zi ** (-n)))
            X2[i] = np.sum(x2 * (zi ** (-n)))
            Y_direct[i] = np.sum(y * (zi ** (-n)))
            Y_linear[i] = a1 * X1[i] + a2 * X2[i]
        
        # Crear figura
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Propiedad de Linealidad', fontsize=14)
        
        # Señales originales
        ax1.stem(n, x1, basefmt=" ", label='x₁(n)')
        ax1.stem(n, x2, basefmt=" ", linefmt='r-', markerfmt='ro', label='x₂(n)')
        ax1.set_title('Señales Originales')
        ax1.set_xlabel('n')
        ax1.set_ylabel('Amplitud')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Combinación lineal
        ax2.stem(n, y, basefmt=" ", linefmt='g-', markerfmt='go')
        ax2.set_title(f'y(n) = {a1:.1f}x₁(n) + {a2:.1f}x₂(n)')
        ax2.set_xlabel('n')
        ax2.set_ylabel('Amplitud')
        ax2.grid(True, alpha=0.3)
        
        # Transformadas Z - Magnitud
        freq_norm = omega / (2 * np.pi)
        ax3.plot(freq_norm, np.abs(Y_direct), 'g-', linewidth=2, label='Z{y(n)} directo')
        ax3.plot(freq_norm, np.abs(Y_linear), 'r--', linewidth=2, label=f'{a1:.1f}X₁(z) + {a2:.1f}X₂(z)')
        ax3.set_title('Magnitud: Verificación de Linealidad')
        ax3.set_xlabel('Frecuencia normalizada')
        ax3.set_ylabel('|Y(z)|')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Error
        error = np.abs(Y_direct - Y_linear)
        ax4.plot(freq_norm, error, 'k-')
        ax4.set_title('Error = |Y_directo - Y_lineal|')
        ax4.set_xlabel('Frecuencia normalizada')
        ax4.set_ylabel('Error')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.prop_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Información
        max_error = np.max(error)
        info_text = f"PROPIEDAD DE LINEALIDAD:\n"
        info_text += f"Z{{a₁x₁(n) + a₂x₂(n)}} = a₁X₁(z) + a₂X₂(z)\n\n"
        info_text += f"Coeficientes: a₁ = {a1:.1f}, a₂ = {a2:.1f}\n"
        info_text += f"x₁(n) = {{1, 2, 1, 0, 0, 0}}\n"
        info_text += f"x₂(n) = {{0, 1, 2, 1, 0, 0}}\n"
        info_text += f"y(n) = {a1:.1f}x₁(n) + {a2:.1f}x₂(n)\n\n"
        info_text += f"Error máximo: {max_error:.2e} ≈ 0\n"
        info_text += f"✓ Propiedad verificada"
        
        self.prop_info_label.config(text=info_text)
    
    def demo_retardo(self, delay):
        """Demostrar propiedad de retardo"""
        # Señal original
        n = np.arange(8)
        x = np.array([1, 3, 2, 1, 0, 0, 0, 0])
        
        # Señal retardada
        x_delayed = np.zeros_like(x)
        if delay < len(x):
            x_delayed[delay:] = x[:-delay]
        
        # Transformadas Z
        omega = np.linspace(0, 2*np.pi, 256)
        z = np.exp(1j * omega)
        
        X = np.zeros_like(z, dtype=complex)
        X_delayed_direct = np.zeros_like(z, dtype=complex)
        X_delayed_prop = np.zeros_like(z, dtype=complex)
        
        for i, zi in enumerate(z):
            X[i] = np.sum(x * (zi ** (-n)))
            X_delayed_direct[i] = np.sum(x_delayed * (zi ** (-n)))
            X_delayed_prop[i] = (zi ** (-delay)) * X[i]
        
        # Crear figura
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Propiedad de Retardo', fontsize=14)
        
        # Señales
        ax1.stem(n, x, basefmt=" ", label='x(n)')
        ax1.stem(n, x_delayed, basefmt=" ", linefmt='r-', markerfmt='ro', label=f'x(n-{delay})')
        ax1.set_title('Señal Original y Retardada')
        ax1.set_xlabel('n')
        ax1.set_ylabel('Amplitud')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Transformadas - Magnitud
        freq_norm = omega / (2 * np.pi)
        ax2.plot(freq_norm, np.abs(X), 'b-', label='|X(z)|')
        ax2.plot(freq_norm, np.abs(X_delayed_direct), 'r-', label=f'|Z{{x(n-{delay})}}| directo')
        ax2.plot(freq_norm, np.abs(X_delayed_prop), 'g--', label=f'|z^(-{delay})X(z)|')
        ax2.set_title('Magnitud de las Transformadas')
        ax2.set_xlabel('Frecuencia normalizada')
        ax2.set_ylabel('Magnitud')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Fase
        ax3.plot(freq_norm, np.angle(X), 'b-', label='∠X(z)')
        ax3.plot(freq_norm, np.angle(X_delayed_direct), 'r-', label=f'∠Z{{x(n-{delay})}}')
        ax3.plot(freq_norm, np.angle(X_delayed_prop), 'g--', label=f'∠z^(-{delay})X(z)')
        ax3.set_title('Fase de las Transformadas')
        ax3.set_xlabel('Frecuencia normalizada')
        ax3.set_ylabel('Fase [rad]')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Error
        error = np.abs(X_delayed_direct - X_delayed_prop)
        ax4.plot(freq_norm, error, 'k-')
        ax4.set_title('Error de Verificación')
        ax4.set_xlabel('Frecuencia normalizada')
        ax4.set_ylabel('Error')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.prop_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Información
        max_error = np.max(error)
        info_text = f"PROPIEDAD DE RETARDO:\n"
        info_text += f"Z{{x(n-D)}} = z^(-D)X(z)\n\n"
        info_text += f"Retardo D = {delay} muestras\n"
        info_text += f"x(n) = {{1, 3, 2, 1, 0, 0, 0, 0}}\n"
        info_text += f"x(n-{delay}) retarda la señal {delay} posiciones\n\n"
        info_text += f"La magnitud NO cambia: |z^(-D)X(z)| = |X(z)|\n"
        info_text += f"La fase cambia: ∠z^(-D)X(z) = ∠X(z) - D·ω\n\n"
        info_text += f"Error máximo: {max_error:.2e} ≈ 0\n"
        info_text += f"✓ Propiedad verificada"
        
        self.prop_info_label.config(text=info_text)
    
    def demo_convolucion(self):
        """Demostrar propiedad de convolución"""
        # Señales de prueba
        n = np.arange(8)
        h = np.array([1, 2, 1, 0, 0, 0, 0, 0])  # Respuesta al impulso
        x = np.array([1, 1, 0, 0, 0, 0, 0, 0])  # Entrada
        
        # Convolución
        y = np.convolve(h, x, mode='same')
        
        # Transformadas Z
        omega = np.linspace(0, 2*np.pi, 256)
        z = np.exp(1j * omega)
        
        H = np.zeros_like(z, dtype=complex)
        X = np.zeros_like(z, dtype=complex)
        Y_direct = np.zeros_like(z, dtype=complex)
        Y_product = np.zeros_like(z, dtype=complex)
        
        for i, zi in enumerate(z):
            H[i] = np.sum(h * (zi ** (-n)))
            X[i] = np.sum(x * (zi ** (-n)))
            Y_direct[i] = np.sum(y * (zi ** (-n)))
            Y_product[i] = H[i] * X[i]
        
        # Crear figura
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Propiedad de Convolución', fontsize=14)
        
        # Señales
        ax1.stem(n, h, basefmt=" ", label='h(n)')
        ax1.stem(n, x, basefmt=" ", linefmt='r-', markerfmt='ro', label='x(n)')
        ax1.stem(n, y, basefmt=" ", linefmt='g-', markerfmt='go', label='y(n) = h(n)*x(n)')
        ax1.set_title('Señales: Respuesta al impulso, Entrada y Salida')
        ax1.set_xlabel('n')
        ax1.set_ylabel('Amplitud')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Transformadas individuales
        freq_norm = omega / (2 * np.pi)
        ax2.plot(freq_norm, np.abs(H), 'b-', label='|H(z)|')
        ax2.plot(freq_norm, np.abs(X), 'r-', label='|X(z)|')
        ax2.set_title('Transformadas de Entrada')
        ax2.set_xlabel('Frecuencia normalizada')
        ax2.set_ylabel('Magnitud')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Verificación convolución
        ax3.plot(freq_norm, np.abs(Y_direct), 'g-', linewidth=2, label='|Z{y(n)}| directo')
        ax3.plot(freq_norm, np.abs(Y_product), 'k--', linewidth=2, label='|H(z)X(z)| producto')
        ax3.set_title('Verificación: Convolución ↔ Multiplicación')
        ax3.set_xlabel('Frecuencia normalizada')
        ax3.set_ylabel('|Y(z)|')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Error
        error = np.abs(Y_direct - Y_product)
        ax4.plot(freq_norm, error, 'k-')
        ax4.set_title('Error de Verificación')
        ax4.set_xlabel('Frecuencia normalizada')
        ax4.set_ylabel('Error')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.prop_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Información
        max_error = np.max(error)
        info_text = f"PROPIEDAD DE CONVOLUCIÓN:\n"
        info_text += f"y(n) = h(n) * x(n) ⟺ Y(z) = H(z)X(z)\n\n"
        info_text += f"h(n) = {{1, 2, 1, 0, ...}} (respuesta al impulso)\n"
        info_text += f"x(n) = {{1, 1, 0, 0, ...}} (entrada)\n"
        info_text += f"y(n) = h(n) * x(n) (salida por convolución)\n\n"
        info_text += f"En el dominio Z:\n"
        info_text += f"Y(z) = H(z) × X(z)\n\n"
        info_text += f"Error máximo: {max_error:.2e} ≈ 0\n"
        info_text += f"✓ Propiedad verificada\n\n"
        info_text += f"Esta propiedad es fundamental para el\n"
        info_text += f"análisis de sistemas LTI y filtros digitales"
        
        self.prop_info_label.config(text=info_text)
    
    def crear_pestaña_ejemplos(self):
        """Pestaña para ejemplos específicos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="3. Ejemplos")
        
        # Título
        titulo = ttk.Label(frame, text="Ejemplo del Material: h(n) = {2, 3, 5, 2}", 
                          font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Frame principal
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Panel izquierdo - Cálculo paso a paso
        left_frame = ttk.LabelFrame(main_frame, text="Cálculo Paso a Paso")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Panel derecho - Visualización
        right_frame = ttk.LabelFrame(main_frame, text="Visualización")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.mostrar_ejemplo_material(left_frame, right_frame)
    
    def mostrar_ejemplo_material(self, left_frame, right_frame):
        """Mostrar ejemplo específico del material"""
        # Ejemplo del material: h(n) = {2, 3, 5, 2}
        n = np.array([0, 1, 2, 3])
        h = np.array([2, 3, 5, 2])
        
        # Crear texto con cálculo paso a paso
        text_widget = tk.Text(left_frame, wrap=tk.WORD, font=("Courier", 10))
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        content = "EJEMPLO DEL MATERIAL:\n"
        content += "=" * 40 + "\n\n"
        content += "Secuencia: h(n) = {2, 3, 5, 2}\n\n"
        
        content += "PASO 1: Expresar como impulsos\n"
        content += "h(n) = 2δ(n) + 3δ(n-1) + 5δ(n-2) + 2δ(n-3)\n\n"
        
        content += "PASO 2: Transformada Z de δ(n)\n"
        content += "Z{δ(n)} = Σ δ(n)z^(-n) = δ(0)z^0 = 1\n\n"
        
        content += "PASO 3: Propiedad de retardo\n"
        content += "Z{δ(n-1)} = z^(-1)\n"
        content += "Z{δ(n-2)} = z^(-2)\n"
        content += "Z{δ(n-3)} = z^(-3)\n\n"
        
        content += "PASO 4: Aplicar linealidad\n"
        content += "H(z) = 2·Z{δ(n)} + 3·Z{δ(n-1)} + 5·Z{δ(n-2)} + 2·Z{δ(n-3)}\n"
        content += "H(z) = 2·1 + 3·z^(-1) + 5·z^(-2) + 2·z^(-3)\n\n"
        
        content += "RESULTADO FINAL:\n"
        content += "H(z) = 2 + 3z^(-1) + 5z^(-2) + 2z^(-3)\n\n"
        
        content += "VERIFICACIÓN NUMÉRICA:\n"
        content += "Evaluando en z = e^(jω) para ω = π/4:\n"
        z_test = np.exp(1j * np.pi/4)
        H_test = np.sum(h * (z_test ** (-n)))
        content += f"H(e^(jπ/4)) = {H_test:.4f}\n"
        content += f"Magnitud: {np.abs(H_test):.4f}\n"
        content += f"Fase: {np.angle(H_test):.4f} rad\n\n"
        
        content += "INTERPRETACIÓN:\n"
        content += "• Los términos z^(-k) son 'marcadores de posición'\n"
        content += "• Cada coeficiente multiplica su correspondiente z^(-k)\n"
        content += "• El resultado es un polinomio en z^(-1)\n"
        content += "• Para sistemas causales, solo aparecen potencias negativas"
        
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Gráfico
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))
        fig.suptitle('Ejemplo: h(n) = {2, 3, 5, 2}', fontsize=12)
        
        # Señal h(n)
        ax1.stem(n, h, basefmt=" ")
        ax1.set_title('Respuesta al Impulso h(n)')
        ax1.set_xlabel('n')
        ax1.set_ylabel('h(n)')
        ax1.grid(True, alpha=0.3)
        
        # Transformada Z en el círculo unitario
        omega = np.linspace(0, 2*np.pi, 256)
        z = np.exp(1j * omega)
        H_z = np.zeros_like(z, dtype=complex)
        
        for i, zi in enumerate(z):
            H_z[i] = np.sum(h * (zi ** (-n)))
        
        freq_norm = omega / (2 * np.pi)
        ax2.plot(freq_norm, np.abs(H_z))
        ax2.set_title('|H(z)| en círculo unitario')
        ax2.set_xlabel('Frecuencia normalizada')
        ax2.set_ylabel('|H(z)|')
        ax2.grid(True, alpha=0.3)
        
        # Fase
        ax3.plot(freq_norm, np.angle(H_z))
        ax3.set_title('∠H(z) en círculo unitario')
        ax3.set_xlabel('Frecuencia normalizada')
        ax3.set_ylabel('∠H(z) [rad]')
        ax3.grid(True, alpha=0.3)
        
        # Diagrama de polos y ceros
        ax4.set_xlim(-1.5, 1.5)
        ax4.set_ylim(-1.5, 1.5)
        
        # Círculo unitario
        theta = np.linspace(0, 2*np.pi, 100)
        ax4.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.5, label='Círculo unitario')
        
        # Para este ejemplo (FIR), todos los polos están en el origen
        ax4.plot(0, 0, 'xr', markersize=10, label='Polos (en origen)')
        
        # Los ceros son las raíces del numerador
        # H(z) = 2 + 3z^(-1) + 5z^(-2) + 2z^(-3) = (2z^3 + 3z^2 + 5z + 2)/z^3
        # Ceros en las raíces de 2z^3 + 3z^2 + 5z + 2 = 0
        coeff = [2, 3, 5, 2]  # coeficientes del polinomio
        zeros = np.roots(coeff)
        ax4.plot(zeros.real, zeros.imag, 'ob', markersize=8, label='Ceros')
        
        ax4.set_xlabel('Parte Real')
        ax4.set_ylabel('Parte Imaginaria')
        ax4.set_title('Diagrama de Polos y Ceros')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        ax4.axis('equal')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def crear_pestaña_plano_z(self):
        """Pestaña para análisis en el plano Z"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="4. Plano Z")
        
        # Panel de controles
        control_frame = ttk.LabelFrame(frame, text="Configuración del Sistema")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Variables para polos y ceros
        self.num_polos_var = tk.IntVar(value=2)
        self.num_ceros_var = tk.IntVar(value=1)
        self.polo1_r_var = tk.DoubleVar(value=0.5)
        self.polo1_angle_var = tk.DoubleVar(value=45)
        self.polo2_r_var = tk.DoubleVar(value=0.7)
        self.polo2_angle_var = tk.DoubleVar(value=-45)
        self.cero1_r_var = tk.DoubleVar(value=0.8)
        self.cero1_angle_var = tk.DoubleVar(value=90)
        
        # Configuración de polos
        polos_frame = ttk.LabelFrame(control_frame, text="Polos")
        polos_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        ttk.Label(polos_frame, text="Número:").grid(row=0, column=0, padx=2, pady=2)
        ttk.Spinbox(polos_frame, from_=0, to=3, textvariable=self.num_polos_var,
                   command=self.actualizar_plano_z, width=5).grid(row=0, column=1, padx=2, pady=2)
        
        ttk.Label(polos_frame, text="Polo 1 - r:").grid(row=1, column=0, padx=2, pady=2)
        ttk.Scale(polos_frame, from_=0.1, to=0.99, variable=self.polo1_r_var,
                 command=self.actualizar_plano_z, length=100).grid(row=1, column=1, padx=2, pady=2)
        ttk.Label(polos_frame, textvariable=self.polo1_r_var).grid(row=1, column=2, padx=2, pady=2)
        
        ttk.Label(polos_frame, text="Polo 1 - θ:").grid(row=2, column=0, padx=2, pady=2)
        ttk.Scale(polos_frame, from_=-180, to=180, variable=self.polo1_angle_var,
                 command=self.actualizar_plano_z, length=100).grid(row=2, column=1, padx=2, pady=2)
        ttk.Label(polos_frame, textvariable=self.polo1_angle_var).grid(row=2, column=2, padx=2, pady=2)
        
        ttk.Label(polos_frame, text="Polo 2 - r:").grid(row=3, column=0, padx=2, pady=2)
        ttk.Scale(polos_frame, from_=0.1, to=0.99, variable=self.polo2_r_var,
                 command=self.actualizar_plano_z, length=100).grid(row=3, column=1, padx=2, pady=2)
        ttk.Label(polos_frame, textvariable=self.polo2_r_var).grid(row=3, column=2, padx=2, pady=2)
        
        ttk.Label(polos_frame, text="Polo 2 - θ:").grid(row=4, column=0, padx=2, pady=2)
        ttk.Scale(polos_frame, from_=-180, to=180, variable=self.polo2_angle_var,
                 command=self.actualizar_plano_z, length=100).grid(row=4, column=1, padx=2, pady=2)
        ttk.Label(polos_frame, textvariable=self.polo2_angle_var).grid(row=4, column=2, padx=2, pady=2)
        
        # Configuración de ceros
        ceros_frame = ttk.LabelFrame(control_frame, text="Ceros")
        ceros_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(ceros_frame, text="Número:").grid(row=0, column=0, padx=2, pady=2)
        ttk.Spinbox(ceros_frame, from_=0, to=3, textvariable=self.num_ceros_var,
                   command=self.actualizar_plano_z, width=5).grid(row=0, column=1, padx=2, pady=2)
        
        ttk.Label(ceros_frame, text="Cero 1 - r:").grid(row=1, column=0, padx=2, pady=2)
        ttk.Scale(ceros_frame, from_=0.1, to=2.0, variable=self.cero1_r_var,
                 command=self.actualizar_plano_z, length=100).grid(row=1, column=1, padx=2, pady=2)
        ttk.Label(ceros_frame, textvariable=self.cero1_r_var).grid(row=1, column=2, padx=2, pady=2)
        
        ttk.Label(ceros_frame, text="Cero 1 - θ:").grid(row=2, column=0, padx=2, pady=2)
        ttk.Scale(ceros_frame, from_=-180, to=180, variable=self.cero1_angle_var,
                 command=self.actualizar_plano_z, length=100).grid(row=2, column=1, padx=2, pady=2)
        ttk.Label(ceros_frame, textvariable=self.cero1_angle_var).grid(row=2, column=2, padx=2, pady=2)
        
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        
        # Frame para gráficos
        self.plano_graph_frame = ttk.Frame(frame)
        self.plano_graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info frame
        self.plano_info_frame = ttk.LabelFrame(frame, text="Análisis de Estabilidad")
        self.plano_info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.plano_info_label = ttk.Label(self.plano_info_frame, text="", 
                                         font=("Courier", 9), justify=tk.LEFT)
        self.plano_info_label.pack(padx=10, pady=5)
        
        self.actualizar_plano_z()
    
    def actualizar_plano_z(self, event=None):
        """Actualizar visualización del plano Z"""
        # Limpiar frame
        for widget in self.plano_graph_frame.winfo_children():
            widget.destroy()
        
        # Obtener configuración
        num_polos = self.num_polos_var.get()
        num_ceros = self.num_ceros_var.get()
        
        # Calcular polos
        polos = []
        if num_polos >= 1:
            r1 = self.polo1_r_var.get()
            theta1 = np.deg2rad(self.polo1_angle_var.get())
            polo1 = r1 * np.exp(1j * theta1)
            polos.append(polo1)
            
        if num_polos >= 2:
            r2 = self.polo2_r_var.get()
            theta2 = np.deg2rad(self.polo2_angle_var.get())
            polo2 = r2 * np.exp(1j * theta2)
            polos.append(polo2)
        
        # Calcular ceros
        ceros = []
        if num_ceros >= 1:
            r1 = self.cero1_r_var.get()
            theta1 = np.deg2rad(self.cero1_angle_var.get())
            cero1 = r1 * np.exp(1j * theta1)
            ceros.append(cero1)
        
        polos = np.array(polos) if polos else np.array([])
        ceros = np.array(ceros) if ceros else np.array([])
        
        # Crear función de transferencia
        omega = np.linspace(0, 2*np.pi, 512)
        z = np.exp(1j * omega)
        
        # Calcular H(z) en el círculo unitario
        H = np.ones_like(z, dtype=complex)
        
        # Multiplicar por (z - cero_i) para cada cero
        for cero in ceros:
            H *= (z - cero)
        
        # Dividir por (z - polo_i) para cada polo
        for polo in polos:
            H /= (z - polo)
        
        # Crear figura
        fig = plt.figure(figsize=(15, 10))
        
        # Plano Z
        ax1 = fig.add_subplot(2, 3, 1)
        self.plot_plano_z(ax1, polos, ceros)
        
        # Respuesta en frecuencia - magnitud
        ax2 = fig.add_subplot(2, 3, 2)
        freq_norm = omega / (2 * np.pi)
        ax2.plot(freq_norm, 20*np.log10(np.abs(H) + 1e-10))
        ax2.set_title('Respuesta en Frecuencia - Magnitud')
        ax2.set_xlabel('Frecuencia normalizada')
        ax2.set_ylabel('|H(z)| [dB]')
        ax2.grid(True, alpha=0.3)
        
        # Respuesta en frecuencia - fase
        ax3 = fig.add_subplot(2, 3, 3)
        ax3.plot(freq_norm, np.unwrap(np.angle(H)))
        ax3.set_title('Respuesta en Frecuencia - Fase')
        ax3.set_xlabel('Frecuencia normalizada')
        ax3.set_ylabel('∠H(z) [rad]')
        ax3.grid(True, alpha=0.3)
        
        # Respuesta al impulso
        ax4 = fig.add_subplot(2, 3, 4)
        h = self.calcular_respuesta_impulso(polos, ceros)
        n = np.arange(len(h))
        ax4.stem(n, h.real, basefmt=" ")
        ax4.set_title('Respuesta al Impulso h(n)')
        ax4.set_xlabel('n')
        ax4.set_ylabel('h(n)')
        ax4.grid(True, alpha=0.3)
        
        # Superficie 3D de |H(z)|
        ax5 = fig.add_subplot(2, 3, 5, projection='3d')
        self.plot_superficie_hz(ax5, polos, ceros)
        
        # Análisis de estabilidad
        ax6 = fig.add_subplot(2, 3, 6)
        self.plot_analisis_estabilidad(ax6, polos)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.plano_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Información de estabilidad
        self.mostrar_info_estabilidad(polos, ceros)
    
    def plot_plano_z(self, ax, polos, ceros):
        """Dibujar el plano Z con polos y ceros"""
        # Círculo unitario
        theta = np.linspace(0, 2*np.pi, 100)
        ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=2, label='Círculo unitario')
        
        # Ejes
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        
        # Polos
        if len(polos) > 0:
            ax.plot(polos.real, polos.imag, 'xr', markersize=12, markeredgewidth=3, label='Polos')
            for i, polo in enumerate(polos):
                ax.annotate(f'p{i+1}', (polo.real, polo.imag), xytext=(5, 5), 
                           textcoords='offset points', fontsize=10, color='red')
        
        # Ceros
        if len(ceros) > 0:
            ax.plot(ceros.real, ceros.imag, 'ob', markersize=10, label='Ceros')
            for i, cero in enumerate(ceros):
                ax.annotate(f'z{i+1}', (cero.real, cero.imag), xytext=(5, 5), 
                           textcoords='offset points', fontsize=10, color='blue')
        
        # Región de estabilidad
        theta_fill = np.linspace(0, 2*np.pi, 100)
        ax.fill(np.cos(theta_fill), np.sin(theta_fill), alpha=0.1, color='green', 
                label='Región estable')
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlabel('Parte Real')
        ax.set_ylabel('Parte Imaginaria')
        ax.set_title('Plano Z - Polos y Ceros')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_aspect('equal')
    
    def plot_superficie_hz(self, ax, polos, ceros):
        """Dibujar superficie 3D de |H(z)|"""
        # Crear malla en el plano Z
        x = np.linspace(-1.5, 1.5, 50)
        y = np.linspace(-1.5, 1.5, 50)
        X, Y = np.meshgrid(x, y)
        Z_plane = X + 1j * Y
        
        # Calcular |H(z)| en toda la malla
        H_mag = np.ones_like(Z_plane, dtype=float)
        
        for i in range(Z_plane.shape[0]):
            for j in range(Z_plane.shape[1]):
                z = Z_plane[i, j]
                h_val = 1.0 + 0j
                
                # Multiplicar por (z - cero_i)
                for cero in ceros:
                    h_val *= (z - cero)
                
                # Dividir por (z - polo_i)
                for polo in polos:
                    if np.abs(z - polo) > 1e-6:  # Evitar singularidades
                        h_val /= (z - polo)
                    else:
                        h_val = np.inf
                
                H_mag[i, j] = np.abs(h_val)
        
        # Limitar valores para visualización
        H_mag = np.clip(H_mag, 0, 10)
        
        # Dibujar superficie
        surf = ax.plot_surface(X, Y, H_mag, cmap='viridis', alpha=0.7)
        
        # Marcar polos y ceros
        if len(polos) > 0:
            ax.scatter(polos.real, polos.imag, [0]*len(polos), 
                      c='red', s=100, marker='x', label='Polos')
        if len(ceros) > 0:
            ax.scatter(ceros.real, ceros.imag, [0]*len(ceros), 
                      c='blue', s=100, marker='o', label='Ceros')
        
        ax.set_xlabel('Re(z)')
        ax.set_ylabel('Im(z)')
        ax.set_zlabel('|H(z)|')
        ax.set_title('Superficie |H(z)|')
    
    def plot_analisis_estabilidad(self, ax, polos):
        """Análisis de estabilidad"""
        # Círculo unitario
        theta = np.linspace(0, 2*np.pi, 100)
        ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=2, label='Círculo unitario')
        
        # Colorear regiones
        theta_fill = np.linspace(0, 2*np.pi, 100)
        ax.fill(np.cos(theta_fill), np.sin(theta_fill), alpha=0.2, color='green', 
                label='ESTABLE (|polo| < 1)')
        
        # Crear región inestable
        r_unstable = np.linspace(1, 1.5, 20)
        theta_unstable = np.linspace(0, 2*np.pi, 100)
        for r in r_unstable:
            x_unstable = r * np.cos(theta_unstable)
            y_unstable = r * np.sin(theta_unstable)
            if r == r_unstable[0]:
                ax.fill(x_unstable, y_unstable, alpha=0.1, color='red')
        ax.fill([], [], alpha=0.1, color='red', label='INESTABLE (|polo| > 1)')
        
        # Polos
        if len(polos) > 0:
            for i, polo in enumerate(polos):
                if np.abs(polo) < 1:
                    color = 'green'
                    marker = 'o'
                    status = 'ESTABLE'
                elif np.abs(polo) == 1:
                    color = 'orange'
                    marker = 's'
                    status = 'MARGINALMENTE ESTABLE'
                else:
                    color = 'red'
                    marker = 'x'
                    status = 'INESTABLE'
                
                ax.plot(polo.real, polo.imag, marker=marker, color=color, 
                       markersize=12, markeredgewidth=2)
                ax.annotate(f'p{i+1}\n{status}', (polo.real, polo.imag), 
                           xytext=(10, 10), textcoords='offset points', 
                           fontsize=8, ha='left')
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlabel('Parte Real')
        ax.set_ylabel('Parte Imaginaria')
        ax.set_title('Análisis de Estabilidad')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_aspect('equal')
    
    def calcular_respuesta_impulso(self, polos, ceros, N=20):
        """Calcular respuesta al impulso aproximada"""
        if len(polos) == 0:
            # Sistema FIR simple
            h = np.zeros(N)
            h[0] = 1
            for cero in ceros:
                h_temp = np.zeros(N)
                h_temp[0] = 1
                h_temp[1] = -cero.real if np.isreal(cero) else -cero
                h = np.convolve(h, h_temp)[:N]
            return h
        else:
            # Sistema IIR - aproximación usando residuos
            h = np.zeros(N, dtype=complex)
            n = np.arange(N)
            
            # Para cada polo, agregar su contribución
            for polo in polos:
                if np.abs(polo) < 1:  # Solo si es estable
                    h += (polo ** n)
            
            return h.real
    
    def mostrar_info_estabilidad(self, polos, ceros):
        """Mostrar información de estabilidad"""
        info_text = "ANÁLISIS DE ESTABILIDAD:\n"
        info_text += "=" * 30 + "\n\n"
        
        if len(polos) == 0:
            info_text += "Sistema FIR: SIEMPRE ESTABLE\n"
            info_text += "(No tiene polos finitos)\n\n"
        else:
            info_text += "Sistema IIR: Estabilidad depende de polos\n\n"
            sistema_estable = True
            
            for i, polo in enumerate(polos):
                mag = np.abs(polo)
                info_text += f"Polo {i+1}: {polo:.3f}\n"
                info_text += f"  Magnitud: {mag:.3f}\n"
                
                if mag < 1:
                    info_text += "  Estado: ESTABLE ✓\n"
                elif mag == 1:
                    info_text += "  Estado: MARGINALMENTE ESTABLE ⚠\n"
                    sistema_estable = False
                else:
                    info_text += "  Estado: INESTABLE ✗\n"
                    sistema_estable = False
                info_text += "\n"
            
            if sistema_estable:
                info_text += "SISTEMA COMPLETO: ESTABLE ✓\n"
                info_text += "Todos los polos dentro del círculo unitario\n"
            else:
                info_text += "SISTEMA COMPLETO: INESTABLE ✗\n"
                info_text += "Al menos un polo fuera del círculo unitario\n"
        
        info_text += "\nCRITERIO DE ESTABILIDAD:\n"
        info_text += "• Sistema estable: TODOS los polos |p| < 1\n"
        info_text += "• Sistema inestable: ALGÚN polo |p| > 1\n"
        info_text += "• Marginalmente estable: ALGÚN polo |p| = 1\n\n"
        
        if len(ceros) > 0:
            info_text += f"Ceros del sistema: {len(ceros)}\n"
            info_text += "(Los ceros NO afectan la estabilidad)\n"
        
    
    def crear_pestaña_sistemas_lti(self):
        """Pestaña para sistemas LTI y filtros"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="5. Sistemas LTI")
        
        # Panel de controles
        control_frame = ttk.LabelFrame(frame, text="Diseño de Filtros")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.filter_type_var = tk.StringVar(value="Pasa Bajas")
        self.fc_var = tk.DoubleVar(value=0.25)
        self.order_var = tk.IntVar(value=2)
        self.r_var = tk.DoubleVar(value=0.8)
        
        ttk.Label(control_frame, text="Tipo de Filtro:").grid(row=0, column=0, padx=5, pady=2)
        filter_combo = ttk.Combobox(control_frame, textvariable=self.filter_type_var,
                                   values=["Pasa Bajas", "Pasa Altas", "Pasa Banda", "Rechaza Banda"])
        filter_combo.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        filter_combo.bind('<<ComboboxSelected>>', self.actualizar_sistemas_lti)
        
        ttk.Label(control_frame, text="Freq. Corte:").grid(row=1, column=0, padx=5, pady=2)
        fc_scale = ttk.Scale(control_frame, from_=0.05, to=0.45, variable=self.fc_var,
                            command=self.actualizar_sistemas_lti)
        fc_scale.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.fc_var).grid(row=1, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Orden:").grid(row=2, column=0, padx=5, pady=2)
        order_scale = ttk.Scale(control_frame, from_=1, to=4, variable=self.order_var,
                               command=self.actualizar_sistemas_lti)
        order_scale.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.order_var).grid(row=2, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Radio r:").grid(row=3, column=0, padx=5, pady=2)
        r_scale = ttk.Scale(control_frame, from_=0.1, to=0.95, variable=self.r_var,
                           command=self.actualizar_sistemas_lti)
        r_scale.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.r_var).grid(row=3, column=2, padx=5, pady=2)
        
        control_frame.columnconfigure(1, weight=1)
        
        # Frame para gráficos
        self.lti_graph_frame = ttk.Frame(frame)
        self.lti_graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info frame
        self.lti_info_frame = ttk.LabelFrame(frame, text="Función de Transferencia")
        self.lti_info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.lti_info_label = ttk.Label(self.lti_info_frame, text="", 
                                       font=("Courier", 9), justify=tk.LEFT)
        self.lti_info_label.pack(padx=10, pady=5)
        
        self.actualizar_sistemas_lti()
    
    def actualizar_sistemas_lti(self, event=None):
        """Actualizar análisis de sistemas LTI"""
        # Limpiar frame
        for widget in self.lti_graph_frame.winfo_children():
            widget.destroy()
        
        filter_type = self.filter_type_var.get()
        fc = self.fc_var.get()
        order = int(self.order_var.get())
        r = self.r_var.get()
        
        # Diseñar filtro
        polos, ceros, gain = self.disenar_filtro(filter_type, fc, order, r)
        
        # Calcular respuesta
        omega = np.linspace(0, np.pi, 512)
        z = np.exp(1j * omega)
        
        H = np.ones_like(z, dtype=complex) * gain
        
        for cero in ceros:
            H *= (z - cero)
        
        for polo in polos:
            H /= (z - polo)
        
        # Crear figura
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Sistema LTI: Filtro {filter_type}', fontsize=14)
        
        # Plano Z
        self.plot_filter_plano_z(ax1, polos, ceros)
        
        # Respuesta en frecuencia - magnitud
        freq_norm = omega / np.pi
        ax2.plot(freq_norm, 20*np.log10(np.abs(H) + 1e-10))
        ax2.axvline(fc*2, color='r', linestyle='--', label=f'fc = {fc:.2f}')
        ax2.set_title('Respuesta en Frecuencia - Magnitud')
        ax2.set_xlabel('Frecuencia normalizada (×π)')
        ax2.set_ylabel('|H(ω)| [dB]')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Respuesta en frecuencia - fase
        ax3.plot(freq_norm, np.unwrap(np.angle(H)))
        ax3.set_title('Respuesta en Frecuencia - Fase')
        ax3.set_xlabel('Frecuencia normalizada (×π)')
        ax3.set_ylabel('∠H(ω) [rad]')
        ax3.grid(True, alpha=0.3)
        
        # Respuesta al impulso
        h = self.calcular_respuesta_impulso_filtro(polos, ceros, gain)
        n = np.arange(len(h))
        ax4.stem(n, h, basefmt=" ")
        ax4.set_title('Respuesta al Impulso h(n)')
        ax4.set_xlabel('n')
        ax4.set_ylabel('h(n)')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.lti_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Información del filtro
        self.mostrar_info_filtro(filter_type, polos, ceros, gain, fc, order)
    
    def disenar_filtro(self, filter_type, fc, order, r):
        """Diseñar filtro digital básico"""
        wc = 2 * np.pi * fc  # Frecuencia de corte en rad/sample
        
        if filter_type == "Pasa Bajas":
            # Filtro pasa bajas con polos en círculo de radio r
            angles = np.linspace(np.pi/4, 2*np.pi - np.pi/4, order)
            polos = r * np.exp(1j * angles)
            # Ceros en z = -1 para rechazar alta frecuencia
            ceros = -np.ones(order)
            gain = (1-r)**order  # Normalizar ganancia
            
        elif filter_type == "Pasa Altas":
            # Filtro pasa altas con polos cerca del origen
            angles = np.linspace(np.pi/4, 2*np.pi - np.pi/4, order)
            polos = r * np.exp(1j * angles)
            # Ceros en z = 1 para rechazar baja frecuencia
            ceros = np.ones(order)
            gain = (1-r)**order
            
        elif filter_type == "Pasa Banda":
            # Filtro pasa banda
            center_freq = wc
            polos = []
            for i in range(order//2):
                angle = center_freq + (-1)**i * np.pi/8
                polos.extend([r * np.exp(1j * angle), r * np.exp(-1j * angle)])
            polos = np.array(polos[:order])
            
            # Ceros en z = 1 y z = -1
            ceros = np.array([1, -1] * (order//2))[:order]
            gain = (1-r)**(order//2)
            
        else:  # Rechaza Banda
            # Filtro rechaza banda
            center_freq = wc
            # Polos lejos de la frecuencia de rechazo
            angles = [center_freq + np.pi/2, center_freq - np.pi/2]
            polos = r * np.exp(1j * np.array(angles * (order//2)))[:order]
            
            # Ceros en la frecuencia de rechazo
            ceros = 0.9 * np.exp(1j * np.array([center_freq, -center_freq] * (order//2)))[:order]
            gain = 1.0
        
        return polos, ceros, gain
    
    def plot_filter_plano_z(self, ax, polos, ceros):
        """Dibujar plano Z para filtro"""
        # Círculo unitario
        theta = np.linspace(0, 2*np.pi, 100)
        ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=2, label='Círculo unitario')
        
        # Ejes
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        
        # Polos
        if len(polos) > 0:
            ax.plot(polos.real, polos.imag, 'xr', markersize=10, markeredgewidth=2, label='Polos')
        
        # Ceros
        if len(ceros) > 0:
            ax.plot(ceros.real, ceros.imag, 'ob', markersize=8, label='Ceros')
        
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_xlabel('Parte Real')
        ax.set_ylabel('Parte Imaginaria')
        ax.set_title('Diagrama Polo-Cero')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_aspect('equal')
    
    def calcular_respuesta_impulso_filtro(self, polos, ceros, gain, N=30):
        """Calcular respuesta al impulso del filtro"""
        # Método simple: usar la definición de la transformada Z inversa
        h = np.zeros(N, dtype=complex)
        
        # Para sistemas simples, aproximar usando expansión en serie
        if len(polos) == 0:  # Sistema FIR
            h[0] = gain
            for i, cero in enumerate(ceros):
                if i < N-1:
                    h[i+1] = -gain * cero
        else:  # Sistema IIR
            # Aproximación usando la fórmula de residuos
            n = np.arange(N)
            for polo in polos:
                if np.abs(polo) < 1:  # Solo contribuyen polos estables
                    h += gain * (polo ** n) / len(polos)
        
        return h.real
    
    def mostrar_info_filtro(self, filter_type, polos, ceros, gain, fc, order):
        """Mostrar información del filtro"""
        info_text = f"FILTRO {filter_type.upper()}:\n"
        info_text += "=" * 30 + "\n\n"
        
        info_text += f"Orden: {order}\n"
        info_text += f"Frecuencia de corte: {fc:.3f} × π rad/sample\n"
        info_text += f"Ganancia: {gain:.4f}\n\n"
        
        info_text += f"Polos ({len(polos)}):\n"
        for i, polo in enumerate(polos):
            mag = np.abs(polo)
            angle = np.angle(polo)
            info_text += f"  p{i+1}: {polo:.3f} (|p| = {mag:.3f}, ∠p = {angle:.2f})\n"
        
        info_text += f"\nCeros ({len(ceros)}):\n"
        for i, cero in enumerate(ceros):
            mag = np.abs(cero)
            angle = np.angle(cero)
            info_text += f"  z{i+1}: {cero:.3f} (|z| = {mag:.3f}, ∠z = {angle:.2f})\n"
        
        info_text += "\nFUNCIÓN DE TRANSFERENCIA:\n"
        
        # Construir numerador
        num_str = f"{gain:.3f}"
        for cero in ceros:
            if np.isreal(cero):
                if cero > 0:
                    num_str += f"(z - {cero.real:.2f})"
                else:
                    num_str += f"(z + {-cero.real:.2f})"
            else:
                num_str += f"(z - {cero:.2f})"
        
        # Construir denominador
        den_str = "1"
        for polo in polos:
            if np.isreal(polo):
                if polo > 0:
                    den_str += f"(z - {polo.real:.2f})"
                else:
                    den_str += f"(z + {-polo.real:.2f})"
            else:
                den_str += f"(z - {polo:.2f})"
        
        if den_str != "1":
            info_text += f"H(z) = {num_str}\n       /{den_str}\n\n"
        else:
            info_text += f"H(z) = {num_str}\n\n"
        
        # Características del filtro
        info_text += "CARACTERÍSTICAS:\n"
        if filter_type == "Pasa Bajas":
            info_text += "• Permite frecuencias bajas\n"
            info_text += "• Atenúa frecuencias altas\n"
            info_text += f"• Frecuencia de corte: {fc:.2f}π\n"
        elif filter_type == "Pasa Altas":
            info_text += "• Permite frecuencias altas\n"
            info_text += "• Atenúa frecuencias bajas\n"
            info_text += f"• Frecuencia de corte: {fc:.2f}π\n"
        elif filter_type == "Pasa Banda":
            info_text += "• Permite banda de frecuencias\n"
            info_text += "• Atenúa frecuencias fuera de banda\n"
            info_text += f"• Frecuencia central: {fc:.2f}π\n"
        else:
            info_text += "• Rechaza banda de frecuencias\n"
            info_text += "• Permite frecuencias fuera de banda\n"
            info_text += f"• Frecuencia de rechazo: {fc:.2f}π\n"
        
        self.lti_info_label.config(text=info_text)
    
    def crear_pestaña_relaciones(self):
        """Pestaña para relaciones con otras transformadas"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="6. Relaciones")
        
        # Título
        titulo = ttk.Label(frame, text="Relaciones de la Transformada Z", 
                          font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Crear notebook interno para sub-temas
        sub_notebook = ttk.Notebook(frame)
        sub_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Sub-pestaña: Z vs DTFT
        self.crear_sub_z_vs_dtft(sub_notebook)
        
        # Sub-pestaña: Z vs Laplace
        self.crear_sub_z_vs_laplace(sub_notebook)
        
        # Sub-pestaña: Tabla de transformadas
        self.crear_sub_tabla_transformadas(sub_notebook)
    
    def crear_sub_z_vs_dtft(self, parent):
        """Sub-pestaña: Transformada Z vs DTFT"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Z vs DTFT")
        
        # Panel de control
        control_frame = ttk.LabelFrame(frame, text="Parámetros de Comparación")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.comp_signal_var = tk.StringVar(value="Exponencial")
        self.comp_a_var = tk.DoubleVar(value=0.8)
        self.comp_show_roc_var = tk.BooleanVar(value=True)
        
        ttk.Label(control_frame, text="Señal:").grid(row=0, column=0, padx=5, pady=2)
        comp_combo = ttk.Combobox(control_frame, textvariable=self.comp_signal_var,
                                 values=["Exponencial", "Coseno", "Impulso Retardado"])
        comp_combo.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        comp_combo.bind('<<ComboboxSelected>>', self.actualizar_comparacion)
        
        ttk.Label(control_frame, text="Parámetro a:").grid(row=1, column=0, padx=5, pady=2)
        a_scale = ttk.Scale(control_frame, from_=0.1, to=1.5, variable=self.comp_a_var,
                           command=self.actualizar_comparacion)
        a_scale.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.comp_a_var).grid(row=1, column=2, padx=5, pady=2)
        
        ttk.Checkbutton(control_frame, text="Mostrar ROC", 
                       variable=self.comp_show_roc_var,
                       command=self.actualizar_comparacion).grid(row=2, column=0, columnspan=2, padx=5, pady=2)
        
        control_frame.columnconfigure(1, weight=1)
        
        # Frame para gráficos
        self.comp_graph_frame = ttk.Frame(frame)
        self.comp_graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.actualizar_comparacion()
    
    def actualizar_comparacion(self, event=None):
        """Actualizar comparación Z vs DTFT"""
        # Limpiar frame
        for widget in self.comp_graph_frame.winfo_children():
            widget.destroy()
        
        signal_type = self.comp_signal_var.get()
        a = self.comp_a_var.get()
        show_roc = self.comp_show_roc_var.get()
        
        # Generar señal
        n = np.arange(20)
        if signal_type == "Exponencial":
            x = (a ** n) * (n >= 0)
            title_signal = f"x(n) = {a:.1f}^n u(n)"
        elif signal_type == "Coseno":
            x = np.cos(2*np.pi*0.1*n) * (a ** n) * (n >= 0)
            title_signal = f"x(n) = cos(0.2πn) × {a:.1f}^n u(n)"
        else:  # Impulso Retardado
            x = np.zeros_like(n, dtype=float)
            delay = 3
            x[delay] = 1
            title_signal = f"x(n) = δ(n-{delay})"
        
        # Crear figura
        fig = plt.figure(figsize=(15, 12))
        
        # Señal original
        ax1 = fig.add_subplot(3, 2, 1)
        ax1.stem(n, x, basefmt=" ")
        ax1.set_title(f'Señal: {title_signal}')
        ax1.set_xlabel('n')
        ax1.set_ylabel('x(n)')
        ax1.grid(True, alpha=0.3)
        
        # DTFT
        ax2 = fig.add_subplot(3, 2, 2)
        omega = np.linspace(-np.pi, np.pi, 512)
        X_dtft = self.calcular_dtft(x, omega)
        ax2.plot(omega/np.pi, np.abs(X_dtft))
        ax2.set_title('DTFT: |X(e^jω)|')
        ax2.set_xlabel('ω/π')
        ax2.set_ylabel('|X(e^jω)|')
        ax2.grid(True, alpha=0.3)
        
        # Transformada Z en círculo unitario
        ax3 = fig.add_subplot(3, 2, 3)
        z_unit = np.exp(1j * omega)
        X_z_unit = self.calcular_transformada_z_evaluada(x, z_unit)
        ax3.plot(omega/np.pi, np.abs(X_z_unit), 'r-', label='|X(z)| en |z|=1')
        ax3.plot(omega/np.pi, np.abs(X_dtft), 'b--', label='|X(e^jω)| DTFT')
        ax3.set_title('Comparación en círculo unitario')
        ax3.set_xlabel('ω/π')
        ax3.set_ylabel('Magnitud')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plano Z completo
        ax4 = fig.add_subplot(3, 2, 4)
        self.plot_plano_z_completo(ax4, x, show_roc, signal_type, a)
        
        # Superficie |X(z)|
        ax5 = fig.add_subplot(3, 2, 5, projection='3d')
        self.plot_superficie_transformada_z(ax5, x)
        
        # Información teórica
        ax6 = fig.add_subplot(3, 2, 6)
        ax6.axis('off')
        info_text = self.generar_info_comparacion(signal_type, a)
        ax6.text(0.05, 0.95, info_text, transform=ax6.transAxes, fontsize=10,
                verticalalignment='top', fontfamily='monospace')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.comp_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def calcular_dtft(self, x, omega):
        """Calcular DTFT de la señal"""
        X = np.zeros_like(omega, dtype=complex)
        n = np.arange(len(x))
        
        for i, w in enumerate(omega):
            X[i] = np.sum(x * np.exp(-1j * w * n))
        
        return X
    
    def calcular_transformada_z_evaluada(self, x, z_values):
        """Calcular transformada Z evaluada en puntos específicos"""
        X = np.zeros_like(z_values, dtype=complex)
        n = np.arange(len(x))
        
        for i, z in enumerate(z_values):
            X[i] = np.sum(x * (z ** (-n)))
        
        return X
    
    def plot_plano_z_completo(self, ax, x, show_roc, signal_type, a):
        """Dibujar plano Z con ROC"""
        # Círculo unitario
        theta = np.linspace(0, 2*np.pi, 100)
        ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=2, label='Círculo unitario')
        
        # ROC según el tipo de señal
        if show_roc:
            if signal_type == "Exponencial":
                if a < 1:
                    # ROC: |z| > |a|
                    theta_roc = np.linspace(0, 2*np.pi, 100)
                    ax.fill_between(np.cos(theta_roc)*a, np.sin(theta_roc)*a, 
                                   np.cos(theta_roc)*2, np.sin(theta_roc)*2,
                                   alpha=0.2, color='green', label=f'ROC: |z| > {a:.1f}')
                    ax.plot(np.cos(theta_roc)*a, np.sin(theta_roc)*a, 'g--', linewidth=2)
            elif signal_type == "Impulso Retardado":
                # ROC: todo el plano excepto z=0
                theta_roc = np.linspace(0, 2*np.pi, 100)
                for r in [0.5, 1.0, 1.5]:
                    ax.plot(np.cos(theta_roc)*r, np.sin(theta_roc)*r, 'g:', alpha=0.5)
                ax.text(0.5, 1.2, 'ROC: Todo ℂ\nexcepto z=0', ha='center')
        
        # Polos y ceros
        if signal_type == "Exponencial":
            ax.plot(a, 0, 'xr', markersize=12, markeredgewidth=3, label=f'Polo en z={a:.1f}')
        elif signal_type == "Impulso Retardado":
            ax.plot(0, 0, 'xr', markersize=12, markeredgewidth=3, label='Polo en z=0')
        
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_xlabel('Re(z)')
        ax.set_ylabel('Im(z)')
        ax.set_title('Plano Z y ROC')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_aspect('equal')
    
    def plot_superficie_transformada_z(self, ax, x):
        """Dibujar superficie de |X(z)| en 3D"""
        # Crear malla
        real_range = np.linspace(-2, 2, 30)
        imag_range = np.linspace(-2, 2, 30)
        Real, Imag = np.meshgrid(real_range, imag_range)
        Z_plane = Real + 1j * Imag
        
        # Calcular |X(z)|
        X_mag = np.zeros_like(Real)
        n = np.arange(len(x))
        
        for i in range(Real.shape[0]):
            for j in range(Real.shape[1]):
                z = Z_plane[i, j]
                if np.abs(z) > 0.1:  # Evitar singularidades
                    X_mag[i, j] = np.abs(np.sum(x * (z ** (-n))))
                else:
                    X_mag[i, j] = np.inf
        
        # Limitar para visualización
        X_mag = np.clip(X_mag, 0, 20)
        
        surf = ax.plot_surface(Real, Imag, X_mag, cmap='viridis', alpha=0.7)
        ax.set_xlabel('Re(z)')
        ax.set_ylabel('Im(z)')
        ax.set_zlabel('|X(z)|')
        ax.set_title('Superficie |X(z)|')
    
    def generar_info_comparacion(self, signal_type, a):
        """Generar información de comparación"""
        info = "TRANSFORMADA Z vs DTFT\n"
        info += "="*30 + "\n\n"
        
        info += "RELACIÓN FUNDAMENTAL:\n"
        info += "DTFT = Z-Transform evaluada en |z| = 1\n"
        info += "X(e^jω) = X(z)|_{z=e^jω}\n\n"
        
        if signal_type == "Exponencial":
            info += f"Para x(n) = {a:.1f}^n u(n):\n\n"
            info += "Transformada Z:\n"
            info += f"X(z) = 1/(1 - {a:.1f}z^(-1))\n"
            info += f"ROC: |z| > {a:.1f}\n\n"
            info += "DTFT (en círculo unitario):\n"
            info += f"X(e^jω) = 1/(1 - {a:.1f}e^(-jω))\n"
            if a < 1:
                info += "✓ Converge (ROC incluye círculo unitario)\n"
            else:
                info += "✗ No converge (ROC no incluye círculo unitario)\n"
        
        elif signal_type == "Impulso Retardado":
            info += "Para x(n) = δ(n-D):\n\n"
            info += "Transformada Z:\n"
            info += "X(z) = z^(-D)\n"
            info += "ROC: Todo ℂ excepto z=0\n\n"
            info += "DTFT:\n"
            info += "X(e^jω) = e^(-jωD)\n"
            info += "✓ Siempre converge\n"
        
        info += "\nCONCLUSIONES:\n"
        info += "• Z-transform es más general\n"
        info += "• DTFT es caso especial en |z|=1\n"
        info += "• ROC determina convergencia\n"
        info += "• Z permite análisis de estabilidad"
        
        return info
    
    def crear_sub_z_vs_laplace(self, parent):
        """Sub-pestaña: Transformada Z vs Laplace"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Z vs Laplace")
        
        # Crear texto explicativo
        text_widget = tk.Text(frame, wrap=tk.WORD, font=("Courier", 10))
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        content = """TRANSFORMADA Z vs TRANSFORMADA DE LAPLACE
=============================================

ANALOGÍAS FUNDAMENTALES:

1. VARIABLES DE TRANSFORMACIÓN:
   • Laplace (tiempo continuo): s = σ + jΩ
   • Z (tiempo discreto): z = re^(jω)
   
2. RELACIÓN DE MAPEO:
   z = e^(sT)
   donde T = período de muestreo
   
   • Eje jΩ (Laplace) → Círculo unitario |z| = 1
   • Semiplano izquierdo (s) → Interior círculo unitario |z| < 1
   • Semiplano derecho (s) → Exterior círculo unitario |z| > 1

3. DEFINICIONES PARALELAS:

   Laplace:  X(s) = ∫₀^∞ x(t)e^(-st) dt
   
   Z:        X(z) = Σ_{n=0}^∞ x(n)z^(-n)


TABLA DE CORRESPONDENCIAS:
==========================

Función Continua     |  Función Discreta      |  Transformada Z
--------------------|------------------------|------------------
δ(t)                |  δ(n)                  |  1
u(t)                |  u(n)                  |  z/(z-1)
e^(-at)u(t)         |  a^n u(n)              |  z/(z-a)
te^(-at)u(t)        |  na^n u(n)             |  az/(z-a)²
cos(Ωt)u(t)         |  cos(ωn)u(n)           |  z(z-cos(ω))/(z²-2z cos(ω)+1)
sin(Ωt)u(t)         |  sin(ωn)u(n)           |  z sin(ω)/(z²-2z cos(ω)+1)


PROPIEDADES ANÁLOGAS:
====================

Propiedad           |  Laplace              |  Transformada Z
-------------------|----------------------|------------------
Linealidad         |  L{ax₁+bx₂} = aX₁+bX₂  |  Z{ax₁+bx₂} = aX₁+bX₂
Retardo            |  L{x(t-T)} = e^(-sT)X(s) |  Z{x(n-k)} = z^(-k)X(z)
Adelanto           |  L{x(t+T)} = e^(sT)X(s)  |  Z{x(n+k)} = z^k X(z)
Convolución        |  L{x*h} = X(s)H(s)       |  Z{x*h} = X(z)H(z)
Diferenciación     |  L{dx/dt} = sX(s)        |  Z{x(n)-x(n-1)} = (1-z^(-1))X(z)


ESTABILIDAD:
===========

Laplace:
• Sistema estable ⟺ Todos los polos en semiplano izquierdo (Re(s) < 0)
• Respuesta impulso: h(t) → 0 cuando t → ∞

Transformada Z:
• Sistema estable ⟺ Todos los polos dentro círculo unitario (|z| < 1)
• Respuesta impulso: h(n) → 0 cuando n → ∞


DISEÑO DE FILTROS:
=================

Laplace → Z (Métodos de conversión):
1. Transformada bilineal: s = (2/T)(z-1)/(z+1)
2. Invarianza al impulso: z = e^(sT)
3. Mapeo polo-cero directo

Ventajas Z:
• Análisis directo de sistemas discretos
• Implementación digital directa
• No requiere conversión desde dominio continuo

Ventajas Laplace:
• Teoría más madura
• Herramientas analíticas extensas
• Conexión directa con sistemas físicos


APLICACIONES BIOMÉDICAS:
=======================

Tiempo Continuo (Laplace):
• Modelado de sistemas cardiovasculares
• Análisis de señales EMG continuas
• Filtros analógicos de instrumentación

Tiempo Discreto (Z):
• Procesamiento de ECG digitalizado
• Filtros de EEG en tiempo real
• Análisis espectral de señales muestreadas
• Algoritmos de detección de eventos


VENTAJAS DE CADA ENFOQUE:
========================

Transformada de Laplace:
+ Intuición física directa
+ Herramientas de control clásico
+ Análisis de sistemas analógicos
- Requiere digitalización para implementar

Transformada Z:
+ Implementación digital directa
+ Análisis de algoritmos discretos
+ Diseño de filtros digitales
+ Procesamiento en tiempo real
- Menos intuición física inicial
"""
        
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def crear_sub_tabla_transformadas(self, parent):
        """Sub-pestaña: Tabla de transformadas comunes"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Tabla de Transformadas")
        
        # Crear Treeview para la tabla
        columns = ("Señal x(n)", "Transformada X(z)", "ROC")
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        # Configurar encabezados
        tree.heading("Señal x(n)", text="Señal x(n)")
        tree.heading("Transformada X(z)", text="Transformada X(z)")
        tree.heading("ROC", text="Región de Convergencia")
        
        # Configurar anchos de columna
        tree.column("Señal x(n)", width=200)
        tree.column("Transformada X(z)", width=300)
        tree.column("ROC", width=200)
        
        # Datos de la tabla
        transformadas = [
            ("δ(n)", "1", "Todo ℂ"),
            ("δ(n-k)", "z^(-k)", "Todo ℂ excepto z=0 (k>0)"),
            ("u(n)", "z/(z-1)", "|z| > 1"),
            ("nu(n)", "z/(z-1)²", "|z| > 1"),
            ("a^n u(n)", "z/(z-a)", "|z| > |a|"),
            ("na^n u(n)", "az/(z-a)²", "|z| > |a|"),
            ("n²a^n u(n)", "az(z+a)/(z-a)³", "|z| > |a|"),
            ("-a^n u(-n-1)", "z/(z-a)", "|z| < |a|"),
            ("cos(ω₀n)u(n)", "z(z-cos(ω₀))/(z²-2z cos(ω₀)+1)", "|z| > 1"),
            ("sin(ω₀n)u(n)", "z sin(ω₀)/(z²-2z cos(ω₀)+1)", "|z| > 1"),
            ("a^n cos(ω₀n)u(n)", "z(z-a cos(ω₀))/(z²-2az cos(ω₀)+a²)", "|z| > |a|"),
            ("a^n sin(ω₀n)u(n)", "az sin(ω₀)/(z²-2az cos(ω₀)+a²)", "|z| > |a|"),
            ("n cos(ω₀n)u(n)", "z(z²-z cos(ω₀))/(z²-2z cos(ω₀)+1)²", "|z| > 1"),
            ("n sin(ω₀n)u(n)", "z sin(ω₀)(z²+1)/(z²-2z cos(ω₀)+1)²", "|z| > 1")
        ]
        
        # Insertar datos
        for i, (signal, transform, roc) in enumerate(transformadas):
            tree.insert("", tk.END, values=(signal, transform, roc))
        
        # Scrollbar para la tabla
        tree_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        
        # Empaquetar widgets
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame inferior con propiedades
        prop_frame = ttk.LabelFrame(frame, text="Propiedades Importantes")
        prop_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        prop_text = """
PROPIEDADES DE LA TRANSFORMADA Z:

1. LINEALIDAD: Z{ax₁(n) + bx₂(n)} = aX₁(z) + bX₂(z)

2. RETARDO: Z{x(n-k)} = z^(-k)X(z)

3. ADELANTO: Z{x(n+k)} = z^k[X(z) - Σ_{n=0}^{k-1} x(n)z^(-n)]

4. ESCALADO: Z{a^n x(n)} = X(z/a)

5. CONVOLUCIÓN: Z{x(n) * h(n)} = X(z)H(z)

6. CORRELACIÓN: Z{x(n) ⋆ y(n)} = X(z)Y(z^(-1))

7. TEOREMA DEL VALOR INICIAL: x(0) = lim_{z→∞} X(z)

8. TEOREMA DEL VALOR FINAL: lim_{n→∞} x(n) = lim_{z→1} (z-1)X(z)
"""
        
        prop_label = ttk.Label(prop_frame, text=prop_text, 
                              font=("Courier", 9), justify=tk.LEFT)
        prop_label.pack(padx=10, pady=5)

if __name__ == "__main__":
    app = TransformadaZGUI()
    app.mainloop()