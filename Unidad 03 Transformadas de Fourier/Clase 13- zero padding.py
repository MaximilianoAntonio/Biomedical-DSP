"""
CBM414 - Procesamiento Digital de Señales Biomédicas
Clase 13: Zero Padding
Autor: David Ortiz, Ph.D.
Escuela de Ingeniería Biomédica - Universidad de Valparaíso

Objetivo: Comprender el efecto del zero padding sobre el análisis espectral de una señal,
su implementación práctica y sus implicancias en la resolución y precisión de la DFT.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import warnings
warnings.filterwarnings('ignore')

# Configuración para gráficos
plt.style.use('default')
plt.rcParams['font.size'] = 9

class ZeroPaddingGUI:
    """Interfaz gráfica para demostrar conceptos de Zero Padding"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CBM414 - Clase 13: Zero Padding")
        self.root.geometry("1500x900")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.current_figure = None
        self.current_canvas = None
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        """Crear la interfaz principal"""
        # Título principal
        titulo = tk.Label(self.root, 
                         text="CBM414 - Procesamiento Digital de Señales Biomédicas\nClase 13: Zero Padding",
                         font=("Arial", 16, "bold"),
                         bg='#f0f0f0',
                         fg='#2c3e50')
        titulo.pack(pady=10)
        
        # Subtítulo
        subtitulo = tk.Label(self.root,
                           text="David Ortiz, Ph.D. - Universidad de Valparaíso",
                           font=("Arial", 12),
                           bg='#f0f0f0',
                           fg='#34495e')
        subtitulo.pack(pady=5)
        
        # Frame principal con notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear las pestañas
        self.crear_pestaña_conceptos()
        self.crear_pestaña_tipos_zero_padding()
        self.crear_pestaña_comparacion_dtft()
        self.crear_pestaña_resolucion_frecuencia()
        self.crear_pestaña_spectral_leakage()
        self.crear_pestaña_aplicaciones()
        
    def crear_pestaña_conceptos(self):
        """Pestaña para conceptos básicos de zero padding"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="1. Conceptos Básicos")
        
        # Panel de controles
        control_frame = ttk.LabelFrame(frame, text="Parámetros de la Señal")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Variables de control
        self.L_var = tk.IntVar(value=8)  # Longitud original
        self.D_var = tk.IntVar(value=8)  # Zeros a agregar
        self.signal_type_var = tk.StringVar(value="Senoidal")
        self.freq_var = tk.DoubleVar(value=1.0)
        
        # Controles
        ttk.Label(control_frame, text="Longitud L:").grid(row=0, column=0, padx=5, pady=2)
        L_scale = ttk.Scale(control_frame, from_=4, to=16, variable=self.L_var, 
                           command=self.actualizar_conceptos)
        L_scale.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.L_var).grid(row=0, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Zeros D:").grid(row=1, column=0, padx=5, pady=2)
        D_scale = ttk.Scale(control_frame, from_=0, to=24, variable=self.D_var,
                           command=self.actualizar_conceptos)
        D_scale.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.D_var).grid(row=1, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Tipo señal:").grid(row=2, column=0, padx=5, pady=2)
        signal_combo = ttk.Combobox(control_frame, textvariable=self.signal_type_var,
                                   values=["Senoidal", "Pulso rectangular", "Exponencial", "Chirp"])
        signal_combo.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        signal_combo.bind('<<ComboboxSelected>>', self.actualizar_conceptos)
        
        ttk.Label(control_frame, text="Frecuencia:").grid(row=3, column=0, padx=5, pady=2)
        freq_scale = ttk.Scale(control_frame, from_=0.5, to=3.0, variable=self.freq_var,
                              command=self.actualizar_conceptos)
        freq_scale.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.freq_var).grid(row=3, column=2, padx=5, pady=2)
        
        control_frame.columnconfigure(1, weight=1)
        
        # Frame para gráficos
        self.conceptos_graph_frame = ttk.Frame(frame)
        self.conceptos_graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info frame
        self.conceptos_info_frame = ttk.LabelFrame(frame, text="Información")
        self.conceptos_info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.conceptos_info_label = ttk.Label(self.conceptos_info_frame, text="", 
                                             font=("Courier", 9), justify=tk.LEFT)
        self.conceptos_info_label.pack(padx=10, pady=5)
        
        # Crear gráfico inicial
        self.actualizar_conceptos()
        
    def generar_señal(self, L, signal_type, freq):
        """Generar señal de prueba"""
        n = np.arange(L)
        
        if signal_type == "Senoidal":
            x = np.cos(2 * np.pi * freq * n / L)
        elif signal_type == "Pulso rectangular":
            x = np.zeros(L)
            pulse_width = max(1, L // 4)
            x[:pulse_width] = 1
        elif signal_type == "Exponencial":
            x = np.exp(-0.3 * n)
        elif signal_type == "Chirp":
            x = np.cos(2 * np.pi * freq * n**2 / (2 * L))
        else:
            x = np.ones(L)
        
        return x
    
    def aplicar_zero_padding(self, x, D, tipo="asimetrico"):
        """Aplicar zero padding según el tipo"""
        L = len(x)
        
        if tipo == "asimetrico":
            # Zeros al final
            x_padded = np.concatenate([x, np.zeros(D)])
        elif tipo == "simetrico":
            # D/2 zeros al inicio y al final
            D_half = D // 2
            D_remaining = D - D_half
            x_padded = np.concatenate([np.zeros(D_half), x, np.zeros(D_remaining)])
        elif tipo == "inicial":
            # Zeros al inicio
            x_padded = np.concatenate([np.zeros(D), x])
        else:
            x_padded = x
        
        return x_padded
    
    def actualizar_conceptos(self, event=None):
        """Actualizar gráfico de conceptos básicos"""
        L = int(self.L_var.get())
        D = int(self.D_var.get())
        signal_type = self.signal_type_var.get()
        freq = self.freq_var.get()
        
        # Limpiar frame anterior
        for widget in self.conceptos_graph_frame.winfo_children():
            widget.destroy()
        
        # Generar señal original
        x_original = self.generar_señal(L, signal_type, freq)
        
        # Aplicar zero padding
        x_padded = self.aplicar_zero_padding(x_original, D, "asimetrico")
        
        # Calcular DFT
        X_original = np.fft.fft(x_original)
        X_padded = np.fft.fft(x_padded)
        
        # Crear figura
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Conceptos Básicos de Zero Padding', fontsize=14)
        
        # Señal original
        n_orig = np.arange(L)
        ax1.stem(n_orig, x_original, basefmt=" ")
        ax1.set_title(f'Señal Original (L={L})')
        ax1.set_xlabel('n')
        ax1.set_ylabel('x(n)')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(-1, L+D+1)
        
        # Señal con zero padding
        n_padded = np.arange(len(x_padded))
        ax2.stem(n_padded, x_padded, basefmt=" ", linefmt='r-', markerfmt='ro')
        ax2.axvspan(L-0.5, len(x_padded)-0.5, alpha=0.2, color='red', label='Zeros agregados')
        ax2.set_title(f'Señal con Zero Padding (L+D={L+D})')
        ax2.set_xlabel('n')
        ax2.set_ylabel('x_D(n)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_xlim(-1, L+D+1)
        
        # Magnitud DFT original
        freq_orig = np.arange(L) / L
        ax3.plot(freq_orig, np.abs(X_original), 'b.-', label='DFT Original')
        ax3.set_title('|X(k)| - DFT Original')
        ax3.set_xlabel('Frecuencia normalizada (k/L)')
        ax3.set_ylabel('|X(k)|')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # Magnitud DFT con zero padding
        freq_padded = np.arange(len(x_padded)) / len(x_padded)
        ax4.plot(freq_padded, np.abs(X_padded), 'r.-', label='DFT con Zero Padding')
        ax4.set_title('|X_D(k)| - DFT con Zero Padding')
        ax4.set_xlabel('Frecuencia normalizada (k/(L+D))')
        ax4.set_ylabel('|X_D(k)|')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        plt.tight_layout()
        
        # Agregar a la interfaz
        canvas = FigureCanvasTkAgg(fig, self.conceptos_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Actualizar información
        info_text = f"Señal: {signal_type}\n"
        info_text += f"Longitud original (L): {L} muestras\n"
        info_text += f"Zeros agregados (D): {D} muestras\n"
        info_text += f"Longitud total: {L+D} muestras\n\n"
        info_text += f"Resolución original: Δf = 1/L = {1/L:.3f}\n"
        info_text += f"Resolución con padding: Δf = 1/(L+D) = {1/(L+D):.3f}\n"
        info_text += f"Mejora en resolución: {(L+D)/L:.1f}x"
        
        self.conceptos_info_label.config(text=info_text)
    
    def crear_pestaña_tipos_zero_padding(self):
        """Pestaña para tipos de zero padding"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="2. Tipos de Zero Padding")
        
        # Panel de controles
        control_frame = ttk.LabelFrame(frame, text="Parámetros")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.L_tipos_var = tk.IntVar(value=8)
        self.D_tipos_var = tk.IntVar(value=8)
        
        ttk.Label(control_frame, text="Longitud L:").grid(row=0, column=0, padx=5, pady=2)
        L_scale = ttk.Scale(control_frame, from_=6, to=12, variable=self.L_tipos_var, 
                           command=self.actualizar_tipos)
        L_scale.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.L_tipos_var).grid(row=0, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Zeros D:").grid(row=1, column=0, padx=5, pady=2)
        D_scale = ttk.Scale(control_frame, from_=4, to=16, variable=self.D_tipos_var,
                           command=self.actualizar_tipos)
        D_scale.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.D_tipos_var).grid(row=1, column=2, padx=5, pady=2)
        
        control_frame.columnconfigure(1, weight=1)
        
        # Frame para gráficos
        self.tipos_graph_frame = ttk.Frame(frame)
        self.tipos_graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info frame
        info_frame = ttk.LabelFrame(frame, text="Información sobre Tipos de Zero Padding")
        info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        info_text = ("1. Asimétrico (Unidireccional): Zeros al final - Más común, optimiza FFT\n"
                    "2. Simétrico: D/2 zeros al inicio y final - Similar a ventana rectangular\n"
                    "3. Inicial: Zeros al inicio - Equivale a retrasar la señal D muestras")
        ttk.Label(info_frame, text=info_text, font=("Arial", 10), justify=tk.LEFT).pack(padx=10, pady=5)
        
        self.actualizar_tipos()
    
    def actualizar_tipos(self, event=None):
        """Actualizar comparación de tipos de zero padding"""
        L = int(self.L_tipos_var.get())
        D = int(self.D_tipos_var.get())
        
        # Limpiar frame
        for widget in self.tipos_graph_frame.winfo_children():
            widget.destroy()
        
        # Generar señal de prueba (pulso rectangular)
        x_original = np.zeros(L)
        x_original[:L//3] = 1
        
        # Aplicar diferentes tipos de zero padding
        x_asimetrico = self.aplicar_zero_padding(x_original, D, "asimetrico")
        x_simetrico = self.aplicar_zero_padding(x_original, D, "simetrico")
        x_inicial = self.aplicar_zero_padding(x_original, D, "inicial")
        
        # Calcular DFT
        X_asimetrico = np.fft.fft(x_asimetrico)
        X_simetrico = np.fft.fft(x_simetrico)
        X_inicial = np.fft.fft(x_inicial)
        
        # Crear figura
        fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(16, 10))
        fig.suptitle('Comparación de Tipos de Zero Padding', fontsize=14)
        
        # Señales en el tiempo
        n_asim = np.arange(len(x_asimetrico))
        ax1.stem(n_asim, x_asimetrico, basefmt=" ")
        ax1.axvspan(L-0.5, len(x_asimetrico)-0.5, alpha=0.2, color='red')
        ax1.set_title('1. Asimétrico (zeros al final)')
        ax1.set_xlabel('n')
        ax1.set_ylabel('x(n)')
        ax1.grid(True, alpha=0.3)
        
        n_sim = np.arange(len(x_simetrico))
        ax2.stem(n_sim, x_simetrico, basefmt=" ", linefmt='g-', markerfmt='go')
        D_half = D // 2
        ax2.axvspan(-0.5, D_half-0.5, alpha=0.2, color='green')
        ax2.axvspan(D_half+L-0.5, len(x_simetrico)-0.5, alpha=0.2, color='green')
        ax2.set_title('2. Simétrico (zeros inicio y final)')
        ax2.set_xlabel('n')
        ax2.set_ylabel('x(n)')
        ax2.grid(True, alpha=0.3)
        
        n_ini = np.arange(len(x_inicial))
        ax3.stem(n_ini, x_inicial, basefmt=" ", linefmt='m-', markerfmt='mo')
        ax3.axvspan(-0.5, D-0.5, alpha=0.2, color='magenta')
        ax3.set_title('3. Inicial (zeros al inicio)')
        ax3.set_xlabel('n')
        ax3.set_ylabel('x(n)')
        ax3.grid(True, alpha=0.3)
        
        # Magnitud DFT
        freq_asim = np.arange(len(x_asimetrico)) / len(x_asimetrico)
        ax4.plot(freq_asim, np.abs(X_asimetrico), 'b.-')
        ax4.set_title('|X(k)| - Asimétrico')
        ax4.set_xlabel('Frecuencia normalizada')
        ax4.set_ylabel('|X(k)|')
        ax4.grid(True, alpha=0.3)
        
        freq_sim = np.arange(len(x_simetrico)) / len(x_simetrico)
        ax5.plot(freq_sim, np.abs(X_simetrico), 'g.-')
        ax5.set_title('|X(k)| - Simétrico')
        ax5.set_xlabel('Frecuencia normalizada')
        ax5.set_ylabel('|X(k)|')
        ax5.grid(True, alpha=0.3)
        
        freq_ini = np.arange(len(x_inicial)) / len(x_inicial)
        ax6.plot(freq_ini, np.abs(X_inicial), 'm.-')
        ax6.set_title('|X(k)| - Inicial')
        ax6.set_xlabel('Frecuencia normalizada')
        ax6.set_ylabel('|X(k)|')
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.tipos_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def crear_pestaña_comparacion_dtft(self):
        """Pestaña para comparación con DTFT"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="3. DTFT vs DFT")
        
        # Panel de controles
        control_frame = ttk.LabelFrame(frame, text="Parámetros")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.L_dtft_var = tk.IntVar(value=8)
        self.D_dtft_var = tk.IntVar(value=24)
        
        ttk.Label(control_frame, text="Longitud L:").grid(row=0, column=0, padx=5, pady=2)
        L_scale = ttk.Scale(control_frame, from_=4, to=16, variable=self.L_dtft_var, 
                           command=self.actualizar_dtft)
        L_scale.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.L_dtft_var).grid(row=0, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Zeros D:").grid(row=1, column=0, padx=5, pady=2)
        D_scale = ttk.Scale(control_frame, from_=0, to=48, variable=self.D_dtft_var,
                           command=self.actualizar_dtft)
        D_scale.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.D_dtft_var).grid(row=1, column=2, padx=5, pady=2)
        
        control_frame.columnconfigure(1, weight=1)
        
        # Frame para gráficos
        self.dtft_graph_frame = ttk.Frame(frame)
        self.dtft_graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info frame
        info_frame = ttk.LabelFrame(frame, text="Información")
        info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.dtft_info_label = ttk.Label(info_frame, text="", font=("Courier", 9))
        self.dtft_info_label.pack(padx=10, pady=5)
        
        self.actualizar_dtft()
    
    def calcular_dtft(self, x, omega):
        """Calcular DTFT de una señal"""
        n = np.arange(len(x))
        X = np.zeros(len(omega), dtype=complex)
        for i, w in enumerate(omega):
            X[i] = np.sum(x * np.exp(-1j * w * n))
        return X
    
    def actualizar_dtft(self, event=None):
        """Actualizar comparación DTFT vs DFT"""
        L = int(self.L_dtft_var.get())
        D = int(self.D_dtft_var.get())
        
        # Limpiar frame
        for widget in self.dtft_graph_frame.winfo_children():
            widget.destroy()
        
        # Generar señal de prueba
        x_original = np.zeros(L)
        x_original[:L//2] = 1
        
        # Aplicar zero padding
        x_padded = self.aplicar_zero_padding(x_original, D, "asimetrico")
        
        # Calcular DTFT (muestreo fino)
        omega_dtft = np.linspace(0, 2*np.pi, 1024, endpoint=False)
        X_dtft = self.calcular_dtft(x_original, omega_dtft)
        
        # Calcular DFT
        X_original = np.fft.fft(x_original)
        X_padded = np.fft.fft(x_padded)
        
        # Crear figura
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('DTFT vs DFT: Efecto del Zero Padding', fontsize=14)
        
        # Señal original
        n_orig = np.arange(L)
        ax1.stem(n_orig, x_original, basefmt=" ")
        ax1.set_title(f'Señal Original (L={L})')
        ax1.set_xlabel('n')
        ax1.set_ylabel('x(n)')
        ax1.grid(True, alpha=0.3)
        
        # Señal con zero padding
        n_padded = np.arange(len(x_padded))
        ax2.stem(n_padded, x_padded, basefmt=" ", linefmt='r-', markerfmt='ro')
        ax2.axvspan(L-0.5, len(x_padded)-0.5, alpha=0.2, color='red', label='Zeros')
        ax2.set_title(f'Con Zero Padding (L+D={L+D})')
        ax2.set_xlabel('n')
        ax2.set_ylabel('x_D(n)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # DTFT vs DFT original
        freq_dtft = omega_dtft / (2*np.pi)
        ax3.plot(freq_dtft, np.abs(X_dtft), 'k-', linewidth=2, label='DTFT (continua)')
        
        freq_orig = np.arange(L) / L
        ax3.stem(freq_orig, np.abs(X_original), basefmt=" ", linefmt='b-', markerfmt='bo',
                label=f'DFT (L={L})')
        ax3.set_title('Comparación: DTFT vs DFT Original')
        ax3.set_xlabel('Frecuencia normalizada')
        ax3.set_ylabel('|X(k)|')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        ax3.set_xlim(0, 1)
        
        # DTFT vs DFT con zero padding
        ax4.plot(freq_dtft, np.abs(X_dtft), 'k-', linewidth=2, label='DTFT (continua)')
        
        freq_padded = np.arange(len(x_padded)) / len(x_padded)
        ax4.stem(freq_padded, np.abs(X_padded), basefmt=" ", linefmt='r-', markerfmt='ro',
                label=f'DFT con Zero Padding (L+D={L+D})')
        ax4.set_title('Comparación: DTFT vs DFT con Zero Padding')
        ax4.set_xlabel('Frecuencia normalizada')
        ax4.set_ylabel('|X(k)|')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        ax4.set_xlim(0, 1)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.dtft_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Actualizar información
        info_text = f"DEMOSTRACIÓN: XD(ω) = X(ω)\n"
        info_text += f"La DTFT NO cambia con zero padding\n\n"
        info_text += f"DFT original: {L} puntos, Δf = {1/L:.3f}\n"
        info_text += f"DFT con padding: {L+D} puntos, Δf = {1/(L+D):.3f}\n\n"
        info_text += f"El zero padding NO agrega información nueva,\n"
        info_text += f"solo proporciona más muestras de la misma DTFT"
        
    
    def crear_pestaña_resolucion_frecuencia(self):
        """Pestaña para resolución en frecuencia"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="4. Resolución en Frecuencia")
        
        # Panel de controles
        control_frame = ttk.LabelFrame(frame, text="Parámetros")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.L_res_var = tk.IntVar(value=16)
        self.factor_padding_var = tk.IntVar(value=4)
        self.freq1_var = tk.DoubleVar(value=0.2)
        self.freq2_var = tk.DoubleVar(value=0.25)
        
        ttk.Label(control_frame, text="Longitud L:").grid(row=0, column=0, padx=5, pady=2)
        L_scale = ttk.Scale(control_frame, from_=8, to=32, variable=self.L_res_var, 
                           command=self.actualizar_resolucion)
        L_scale.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.L_res_var).grid(row=0, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Factor Padding:").grid(row=1, column=0, padx=5, pady=2)
        factor_scale = ttk.Scale(control_frame, from_=1, to=8, variable=self.factor_padding_var,
                                command=self.actualizar_resolucion)
        factor_scale.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.factor_padding_var).grid(row=1, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Frecuencia 1:").grid(row=2, column=0, padx=5, pady=2)
        freq1_scale = ttk.Scale(control_frame, from_=0.1, to=0.4, variable=self.freq1_var,
                               command=self.actualizar_resolucion)
        freq1_scale.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.freq1_var).grid(row=2, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Frecuencia 2:").grid(row=3, column=0, padx=5, pady=2)
        freq2_scale = ttk.Scale(control_frame, from_=0.1, to=0.4, variable=self.freq2_var,
                               command=self.actualizar_resolucion)
        freq2_scale.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.freq2_var).grid(row=3, column=2, padx=5, pady=2)
        
        control_frame.columnconfigure(1, weight=1)
        
        # Frame para gráficos
        self.res_graph_frame = ttk.Frame(frame)
        self.res_graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info frame
        self.res_info_frame = ttk.LabelFrame(frame, text="Análisis de Resolución")
        self.res_info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.res_info_label = ttk.Label(self.res_info_frame, text="", font=("Courier", 9))
        self.res_info_label.pack(padx=10, pady=5)
        
        self.actualizar_resolucion()
    
    def actualizar_resolucion(self, event=None):
        """Actualizar análisis de resolución"""
        L = int(self.L_res_var.get())
        factor = int(self.factor_padding_var.get())
        freq1 = self.freq1_var.get()
        freq2 = self.freq2_var.get()
        
        # Limpiar frame
        for widget in self.res_graph_frame.winfo_children():
            widget.destroy()
        
        # Generar señal con dos frecuencias cercanas
        n = np.arange(L)
        x = np.cos(2 * np.pi * freq1 * n) + np.cos(2 * np.pi * freq2 * n)
        
        # Sin zero padding
        X_original = np.fft.fft(x)
        
        # Con zero padding
        D = L * (factor - 1)
        x_padded = self.aplicar_zero_padding(x, D, "asimetrico")
        X_padded = np.fft.fft(x_padded)
        
        # Crear figura
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Efecto del Zero Padding en la Resolución en Frecuencia', fontsize=14)
        
        # Señal original
        ax1.plot(n, x, 'b.-')
        ax1.set_title(f'Señal: cos(2πf₁n) + cos(2πf₂n)')
        ax1.set_xlabel('n')
        ax1.set_ylabel('x(n)')
        ax1.grid(True, alpha=0.3)
        
        # Señal con zero padding
        n_padded = np.arange(len(x_padded))
        ax2.plot(n_padded, x_padded, 'r.-')
        ax2.axvspan(L-0.5, len(x_padded)-0.5, alpha=0.2, color='red', label='Zero padding')
        ax2.set_title(f'Con Zero Padding (factor {factor}x)')
        ax2.set_xlabel('n')
        ax2.set_ylabel('x_D(n)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # DFT sin zero padding
        freq_orig = np.arange(L) / L
        ax3.stem(freq_orig[:L//2], np.abs(X_original[:L//2]), basefmt=" ")
        ax3.axvline(freq1, color='g', linestyle='--', alpha=0.7, label=f'f₁={freq1}')
        ax3.axvline(freq2, color='m', linestyle='--', alpha=0.7, label=f'f₂={freq2}')
        ax3.set_title(f'DFT Original (Δf = {1/L:.3f})')
        ax3.set_xlabel('Frecuencia normalizada')
        ax3.set_ylabel('|X(k)|')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        ax3.set_xlim(0, 0.5)
        
        # DFT con zero padding
        freq_padded = np.arange(len(x_padded)) / len(x_padded)
        half_padded = len(x_padded) // 2
        ax4.stem(freq_padded[:half_padded], np.abs(X_padded[:half_padded]), 
                basefmt=" ", linefmt='r-', markerfmt='ro')
        ax4.axvline(freq1, color='g', linestyle='--', alpha=0.7, label=f'f₁={freq1}')
        ax4.axvline(freq2, color='m', linestyle='--', alpha=0.7, label=f'f₂={freq2}')
        ax4.set_title(f'DFT con Zero Padding (Δf = {1/len(x_padded):.4f})')
        ax4.set_xlabel('Frecuencia normalizada')
        ax4.set_ylabel('|X_D(k)|')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        ax4.set_xlim(0, 0.5)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.res_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Actualizar información
        delta_f = abs(freq2 - freq1)
        res_original = 1/L
        res_padded = 1/len(x_padded)
        
        info_text = f"Frecuencias: f₁={freq1:.3f}, f₂={freq2:.3f}\n"
        info_text += f"Separación: Δf = {delta_f:.3f}\n\n"
        info_text += f"Resolución original: {res_original:.4f}\n"
        info_text += f"Resolución con padding: {res_padded:.4f}\n"
        info_text += f"Mejora: {res_original/res_padded:.1f}x\n\n"
        
        if delta_f > res_original:
            info_text += "✓ Frecuencias resolubles sin padding"
        else:
            info_text += "✗ Frecuencias NO resolubles sin padding"
        
        if delta_f > res_padded:
            info_text += "\n✓ Frecuencias resolubles CON padding"
        else:
            info_text += "\n✗ Frecuencias NO resolubles CON padding"
        
        self.res_info_label.config(text=info_text)
    
    def crear_pestaña_spectral_leakage(self):
        """Pestaña para spectral leakage"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="5. Spectral Leakage")
        
        # Panel de controles
        control_frame = ttk.LabelFrame(frame, text="Parámetros")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.L_leak_var = tk.IntVar(value=32)
        self.D_leak_var = tk.IntVar(value=32)
        self.freq_leak_var = tk.DoubleVar(value=5.3)
        self.window_var = tk.StringVar(value="Rectangular")
        
        ttk.Label(control_frame, text="Longitud L:").grid(row=0, column=0, padx=5, pady=2)
        L_scale = ttk.Scale(control_frame, from_=16, to=64, variable=self.L_leak_var, 
                           command=self.actualizar_leakage)
        L_scale.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.L_leak_var).grid(row=0, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Zero Padding D:").grid(row=1, column=0, padx=5, pady=2)
        D_scale = ttk.Scale(control_frame, from_=0, to=128, variable=self.D_leak_var,
                           command=self.actualizar_leakage)
        D_scale.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.D_leak_var).grid(row=1, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Frecuencia:").grid(row=2, column=0, padx=5, pady=2)
        freq_scale = ttk.Scale(control_frame, from_=1.0, to=10.0, variable=self.freq_leak_var,
                              command=self.actualizar_leakage)
        freq_scale.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.freq_leak_var).grid(row=2, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Ventana:").grid(row=3, column=0, padx=5, pady=2)
        window_combo = ttk.Combobox(control_frame, textvariable=self.window_var,
                                   values=["Rectangular", "Hanning", "Hamming", "Blackman"])
        window_combo.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        window_combo.bind('<<ComboboxSelected>>', self.actualizar_leakage)
        
        control_frame.columnconfigure(1, weight=1)
        
        # Frame para gráficos
        self.leak_graph_frame = ttk.Frame(frame)
        self.leak_graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info frame
        info_frame = ttk.LabelFrame(frame, text="Advertencia sobre Spectral Leakage")
        info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        warning_text = ("⚠️  ADVERTENCIA: El zero padding puede generar cortes abruptos\n"
                       "causando 'spectral leakage' (derramamiento de frecuencias).\n"
                       "Solución: Usar ventanas antes del zero padding.")
        ttk.Label(info_frame, text=warning_text, font=("Arial", 10), 
                 foreground='red', justify=tk.LEFT).pack(padx=10, pady=5)
        
        self.actualizar_leakage()
    
    def aplicar_ventana(self, x, window_type):
        """Aplicar ventana a la señal"""
        L = len(x)
        
        if window_type == "Rectangular":
            w = np.ones(L)
        elif window_type == "Hanning":
            w = np.hanning(L)
        elif window_type == "Hamming":
            w = np.hamming(L)
        elif window_type == "Blackman":
            w = np.blackman(L)
        else:
            w = np.ones(L)
        
        return x * w
    
    def actualizar_leakage(self, event=None):
        """Actualizar análisis de spectral leakage"""
        L = int(self.L_leak_var.get())
        D = int(self.D_leak_var.get())
        freq = self.freq_leak_var.get()
        window_type = self.window_var.get()
        
        # Limpiar frame
        for widget in self.leak_graph_frame.winfo_children():
            widget.destroy()
        
        # Generar señal senoidal
        n = np.arange(L)
        x = np.cos(2 * np.pi * freq * n / L)
        
        # Sin ventana
        x_padded_sin_ventana = self.aplicar_zero_padding(x, D, "asimetrico")
        X_sin_ventana = np.fft.fft(x_padded_sin_ventana)
        
        # Con ventana
        x_ventana = self.aplicar_ventana(x, window_type)
        x_padded_con_ventana = self.aplicar_zero_padding(x_ventana, D, "asimetrico")
        X_con_ventana = np.fft.fft(x_padded_con_ventana)
        
        # Crear figura
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Spectral Leakage y el Efecto de las Ventanas', fontsize=14)
        
        # Señal sin ventana
        n_total = np.arange(len(x_padded_sin_ventana))
        ax1.plot(n_total, x_padded_sin_ventana, 'b-')
        ax1.axvspan(L-0.5, len(x_padded_sin_ventana)-0.5, alpha=0.2, color='red', label='Zero padding')
        ax1.set_title('Señal sin Ventana + Zero Padding')
        ax1.set_xlabel('n')
        ax1.set_ylabel('x(n)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Señal con ventana
        ax2.plot(n_total, x_padded_con_ventana, 'g-')
        ax2.axvspan(L-0.5, len(x_padded_con_ventana)-0.5, alpha=0.2, color='red', label='Zero padding')
        ax2.set_title(f'Señal con Ventana {window_type} + Zero Padding')
        ax2.set_xlabel('n')
        ax2.set_ylabel('x(n)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Espectro sin ventana
        freq_axis = np.arange(len(x_padded_sin_ventana)) / len(x_padded_sin_ventana)
        ax3.plot(freq_axis[:len(freq_axis)//2], 
                20*np.log10(np.abs(X_sin_ventana[:len(X_sin_ventana)//2]) + 1e-10), 'b-')
        ax3.axvline(freq/L, color='r', linestyle='--', label=f'Frecuencia teórica')
        ax3.set_title('Espectro SIN Ventana (dB)')
        ax3.set_xlabel('Frecuencia normalizada')
        ax3.set_ylabel('|X(k)| [dB]')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        ax3.set_ylim(-80, 40)
        
        # Espectro con ventana
        ax4.plot(freq_axis[:len(freq_axis)//2], 
                20*np.log10(np.abs(X_con_ventana[:len(X_con_ventana)//2]) + 1e-10), 'g-')
        ax4.axvline(freq/L, color='r', linestyle='--', label=f'Frecuencia teórica')
        ax4.set_title(f'Espectro CON Ventana {window_type} (dB)')
        ax4.set_xlabel('Frecuencia normalizada')
        ax4.set_ylabel('|X(k)| [dB]')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        ax4.set_ylim(-80, 40)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.leak_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def crear_pestaña_aplicaciones(self):
        """Pestaña para aplicaciones prácticas"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="6. Aplicaciones")
        
        # Título
        titulo = ttk.Label(frame, text="Aplicaciones Prácticas del Zero Padding", 
                          font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Frame principal
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Panel izquierdo - Ejemplos
        left_frame = ttk.LabelFrame(main_frame, text="Ejemplos de Aplicación")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Panel derecho - Recomendaciones
        right_frame = ttk.LabelFrame(main_frame, text="Buenas Prácticas")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Contenido ejemplos
        ejemplos_text = """APLICACIONES DEL ZERO PADDING:

1. OPTIMIZACIÓN DE FFT
   • Completar a potencias de 2
   • Ejemplo: L=100 → pad a 128
   • Mejora velocidad de cálculo

2. INTERPOLACIÓN ESPECTRAL
   • Obtener más puntos en frecuencia
   • Útil para visualización
   • NO agrega nueva información

3. ANÁLISIS DE SEÑALES CORTAS
   • Mejorar resolución aparente
   • Análisis de transitorios
   • Detección de picos espectrales

4. PROCESAMIENTO DE AUDIO
   • Análisis espectral detallado
   • Efectos de audio
   • Síntesis por FFT

5. PROCESAMIENTO DE IMÁGENES
   • Filtrado en frecuencia
   • Convolución eficiente
   • Transformadas 2D

6. BIOMEDICINA
   • Análisis ECG/EEG
   • Señales respiratorias
   • Análisis de variabilidad"""
        
        text_ejemplos = tk.Text(left_frame, wrap=tk.WORD, font=("Courier", 9))
        text_ejemplos.insert(tk.END, ejemplos_text)
        text_ejemplos.config(state=tk.DISABLED)
        text_ejemplos.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Contenido recomendaciones
        recomendaciones_text = """BUENAS PRÁCTICAS:

✓ CUÁNDO USAR:
   • Optimizar FFT (potencias de 2)
   • Mejorar visualización espectral
   • Interpolación en frecuencia
   • Análisis de señales cortas

✗ CUÁNDO NO USAR:
   • Para "crear" información nueva
   • Sin considerar spectral leakage
   • En señales con ruido alto
   • Sin analizar la señal original

⚠️ PRECAUCIONES:
   • Usar ventanas apropiadas
   • Considerar discontinuidades
   • No confundir resolución con precisión
   • Validar resultados

🛠️ RECOMENDACIONES:
   1. Analizar DTFT primero
   2. Elegir ventana adecuada
   3. Factor de padding moderado (2-4x)
   4. Verificar contra señal original
   5. Documentar procesamiento

📊 HERRAMIENTAS:
   • MATLAB: fft(x, N)
   • Python: np.fft.fft(x, n=N)
   • Scipy: scipy.fft.fft
   • GNU Octave: fft(x, N)

🔍 VALIDACIÓN:
   • Comparar con DTFT teórica
   • Verificar conservación de energía
   • Analizar artifacts espectrales
   • Probar con señales conocidas"""
        
        text_recomendaciones = tk.Text(right_frame, wrap=tk.WORD, font=("Courier", 9))
        text_recomendaciones.insert(tk.END, recomendaciones_text)
        text_recomendaciones.config(state=tk.DISABLED)
        text_recomendaciones.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame inferior con resumen
        resumen_frame = ttk.LabelFrame(frame, text="Resumen de la Clase")
        resumen_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        resumen_text = ("PUNTOS CLAVE:\n"
                       "• Zero padding NO cambia la DTFT: XD(ω) = X(ω)\n"
                       "• Mejora resolución computacional: Δf = 1/(L+D)\n"
                       "• Tres tipos: asimétrico, simétrico, inicial\n"
                       "• Precaución: puede causar spectral leakage\n"
                       "• Solución: usar ventanas apropiadas\n"
                       "• Aplicaciones: FFT eficiente, interpolación espectral, análisis biomédico")
        
        ttk.Label(resumen_frame, text=resumen_text, font=("Arial", 10), 
                 justify=tk.LEFT).pack(padx=10, pady=5)
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        app = ZeroPaddingGUI()
        app.ejecutar()
    except Exception as e:
        messagebox.showerror("Error", f"Error al ejecutar la aplicación: {e}")

if __name__ == "__main__":
    main()