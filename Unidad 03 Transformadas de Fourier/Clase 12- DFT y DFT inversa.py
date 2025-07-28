"""
CBM414 - Procesamiento Digital de Señales Biomédicas
Clase 12: DFT y DFT inversa
Autor: David Ortiz, Ph.D.
Escuela de Ingeniería Biomédica - Universidad de Valparaíso

Objetivo: Comprender el funcionamiento de la Transformada Discreta de Fourier (DFT) 
y su inversa, así como su interpretación matricial como proyección sobre bases complejas.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import warnings
warnings.filterwarnings('ignore')

# Configuración para gráficos
plt.style.use('default')
plt.rcParams['font.size'] = 9

class DFTInteractivaGUI:
    """Interfaz gráfica para demostrar conceptos de DFT"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CBM414 - Clase 12: DFT y DFT Inversa")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.current_figure = None
        self.current_canvas = None
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        """Crear la interfaz principal"""
        # Título principal
        titulo = tk.Label(self.root, 
                         text="CBM414 - Procesamiento Digital de Señales Biomédicas\nClase 12: DFT y DFT Inversa",
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
        self.crear_pestaña_exponencial()
        self.crear_pestaña_dft_4_puntos()
        self.crear_pestaña_dft_inversa()
        self.crear_pestaña_bases_dft()
        self.crear_pestaña_dft_interactiva()
        self.crear_pestaña_ejercicio()
        
    def crear_pestaña_exponencial(self):
        """Pestaña para exponencial compleja discreta"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="1. Exponencial Compleja")
        
        # Panel de controles
        control_frame = ttk.LabelFrame(frame, text="Parámetros de la Exponencial Compleja")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Controles
        self.A_var = tk.DoubleVar(value=1.0)
        self.omega_var = tk.DoubleVar(value=0.5)
        self.phi_var = tk.DoubleVar(value=0.0)
        self.N_var = tk.IntVar(value=32)
        
        ttk.Label(control_frame, text="Amplitud A:").grid(row=0, column=0, padx=5, pady=2)
        A_scale = ttk.Scale(control_frame, from_=0.1, to=3.0, variable=self.A_var, 
                           command=self.actualizar_exponencial)
        A_scale.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.A_var).grid(row=0, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Frecuencia ω:").grid(row=1, column=0, padx=5, pady=2)
        omega_scale = ttk.Scale(control_frame, from_=0, to=2*np.pi, variable=self.omega_var,
                               command=self.actualizar_exponencial)
        omega_scale.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.omega_var).grid(row=1, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Fase φ:").grid(row=2, column=0, padx=5, pady=2)
        phi_scale = ttk.Scale(control_frame, from_=0, to=2*np.pi, variable=self.phi_var,
                             command=self.actualizar_exponencial)
        phi_scale.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.phi_var).grid(row=2, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="N puntos:").grid(row=3, column=0, padx=5, pady=2)
        N_scale = ttk.Scale(control_frame, from_=8, to=64, variable=self.N_var,
                           command=self.actualizar_exponencial)
        N_scale.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.N_var).grid(row=3, column=2, padx=5, pady=2)
        
        control_frame.columnconfigure(1, weight=1)
        
        # Frame para el gráfico
        self.exp_graph_frame = ttk.Frame(frame)
        self.exp_graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info frame
        self.exp_info_frame = ttk.LabelFrame(frame, text="Información")
        self.exp_info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.exp_info_label = ttk.Label(self.exp_info_frame, text="", font=("Courier", 9))
        self.exp_info_label.pack(padx=10, pady=5)
        
        # Crear gráfico inicial
        self.actualizar_exponencial()
        
    def actualizar_exponencial(self, event=None):
        """Actualizar gráfico de exponencial compleja"""
        A = self.A_var.get()
        omega = self.omega_var.get()
        phi = self.phi_var.get()
        N = int(self.N_var.get())
        
        # Limpiar frame anterior
        for widget in self.exp_graph_frame.winfo_children():
            widget.destroy()
        
        # Generar señal
        n = np.arange(N)
        x = A * np.exp(1j * (omega * n + phi))
        
        # Crear figura
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Exponencial Compleja Discreta: x(n) = A·e^(j(ωn + φ))', fontsize=14)
        
        # Parte real
        ax1.stem(n, x.real, basefmt=" ")
        ax1.set_title('Parte Real: A·cos(ωn + φ)')
        ax1.set_xlabel('n')
        ax1.set_ylabel('Re{x(n)}')
        ax1.grid(True, alpha=0.3)
        
        # Parte imaginaria
        ax2.stem(n, x.imag, basefmt=" ", linefmt='r-', markerfmt='ro')
        ax2.set_title('Parte Imaginaria: A·sin(ωn + φ)')
        ax2.set_xlabel('n')
        ax2.set_ylabel('Im{x(n)}')
        ax2.grid(True, alpha=0.3)
        
        # Magnitud
        ax3.stem(n, np.abs(x), basefmt=" ", linefmt='g-', markerfmt='go')
        ax3.set_title('Magnitud: |x(n)|')
        ax3.set_xlabel('n')
        ax3.set_ylabel('|x(n)|')
        ax3.grid(True, alpha=0.3)
        
        # Plano complejo
        ax4.plot(x.real, x.imag, 'b.-', markersize=6)
        ax4.set_title('Representación en el Plano Complejo')
        ax4.set_xlabel('Real')
        ax4.set_ylabel('Imaginario')
        ax4.grid(True, alpha=0.3)
        ax4.axis('equal')
        
        # Círculo unitario si A ≈ 1
        if abs(A - 1) < 0.1:
            theta = np.linspace(0, 2*np.pi, 100)
            ax4.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3, label='Círculo unitario')
            ax4.legend()
        
        plt.tight_layout()
        
        # Agregar a la interfaz
        canvas = FigureCanvasTkAgg(fig, self.exp_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Actualizar información
        freq_hz = omega / (2 * np.pi)
        M_N_ratio = omega * N / (2 * np.pi)
        periodica = abs(M_N_ratio - round(M_N_ratio)) < 0.01
        
        info_text = f"A={A:.2f}, ω={omega:.2f} rad, φ={phi:.2f} rad\n"
        info_text += f"Frecuencia: f = {freq_hz:.3f} Hz (fs=1)\n"
        info_text += f"Periodicidad: {'PERIÓDICA' if periodica else 'NO periódica'}"
        if periodica:
            info_text += f" → ω = 2π({round(M_N_ratio)}/{N})"
        
        self.exp_info_label.config(text=info_text)
    
    def crear_pestaña_dft_4_puntos(self):
        """Pestaña para ejemplo DFT de 4 puntos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="2. DFT 4 Puntos")
        
        # Título
        titulo = ttk.Label(frame, text="Ejemplo DFT de 4 Puntos", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Frame principal dividido
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Panel izquierdo - Matrices
        left_frame = ttk.LabelFrame(main_frame, text="Matrices y Cálculos")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Panel derecho - Gráficos
        right_frame = ttk.LabelFrame(main_frame, text="Visualización")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Crear contenido
        self.mostrar_dft_4_puntos(left_frame, right_frame)
        
    def mostrar_dft_4_puntos(self, left_frame, right_frame):
        """Mostrar ejemplo DFT de 4 puntos"""
        N = 4
        W = self.matriz_dft(N)
        
        # Texto con scroll
        text_widget = tk.Text(left_frame, wrap=tk.WORD, font=("Courier", 9))
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Contenido del texto
        content = "MATRIZ W DE LA DFT (N=4):\n"
        content += "=" * 40 + "\n\n"
        content += "Matriz W teórica:\n"
        content += "W = [[  1,   1,   1,   1 ],\n"
        content += "     [  1,  -j,  -1,   j ],\n"
        content += "     [  1,  -1,   1,  -1 ],\n"
        content += "     [  1,   j,  -1,  -j ]]\n\n"
        
        content += "Matriz W calculada:\n"
        for i in range(N):
            if i == 0:
                content += "W = ["
            else:
                content += "    ["
            for j in range(N):
                val = W[i, j]
                if abs(val.real) < 1e-10:
                    real_str = "0"
                else:
                    real_str = f"{val.real:4.1f}"
                
                if abs(val.imag) < 1e-10:
                    imag_str = ""
                elif val.imag > 0:
                    imag_str = f"+{val.imag:3.1f}j"
                else:
                    imag_str = f"{val.imag:4.1f}j"
                
                content += f"{real_str}{imag_str:>6}"
                if j < N-1:
                    content += ", "
            content += " ]\n"
        
        # Ejemplo de transformación
        x = np.array([1, 2, 3, 4])
        X = W @ x
        
        content += f"\nEJEMPLO DE TRANSFORMACIÓN:\n"
        content += "=" * 40 + "\n"
        content += f"Vector de entrada: x = {x}\n"
        content += f"DFT: X = W @ x = {X}\n\n"
        content += "Cálculo paso a paso:\n"
        for k in range(N):
            suma = sum(x[n] * W[k, n] for n in range(N))
            content += f"X[{k}] = {suma:8.2f}\n"
        
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Gráfico
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8, 6))
        fig.suptitle('DFT de 4 Puntos - Ejemplo', fontsize=12)
        
        # Señal original
        n = np.arange(N)
        ax1.stem(n, x, basefmt=" ")
        ax1.set_title('Señal x(n)')
        ax1.set_xlabel('n')
        ax1.set_ylabel('x(n)')
        ax1.grid(True, alpha=0.3)
        
        # Magnitud DFT
        ax2.stem(n, np.abs(X), basefmt=" ", linefmt='r-', markerfmt='ro')
        ax2.set_title('Magnitud |X(k)|')
        ax2.set_xlabel('k')
        ax2.set_ylabel('|X(k)|')
        ax2.grid(True, alpha=0.3)
        
        # Fase DFT
        ax3.stem(n, np.angle(X), basefmt=" ", linefmt='g-', markerfmt='go')
        ax3.set_title('Fase ∠X(k)')
        ax3.set_xlabel('k')
        ax3.set_ylabel('∠X(k) [rad]')
        ax3.grid(True, alpha=0.3)
        
        # Plano complejo
        ax4.plot(X.real, X.imag, 'bo', markersize=8)
        for i in range(len(X)):
            ax4.annotate(f'k={i}', (X[i].real, X[i].imag), 
                        xytext=(5, 5), textcoords='offset points')
        ax4.set_title('DFT en Plano Complejo')
        ax4.set_xlabel('Real')
        ax4.set_ylabel('Imaginario')
        ax4.grid(True, alpha=0.3)
        ax4.axis('equal')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def matriz_dft(self, N):
        """Genera la matriz DFT de N puntos"""
        W = np.zeros((N, N), dtype=complex)
        for k in range(N):
            for n in range(N):
                W[k, n] = np.exp(-2j * np.pi * k * n / N)
        return W
    
    
    def crear_pestaña_dft_inversa(self):
        """Pestaña para DFT inversa"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="3. DFT Inversa")
        
        # Título
        titulo = ttk.Label(frame, text="Ejemplo DFT Inversa", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Frame principal
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Panel izquierdo
        left_frame = ttk.LabelFrame(main_frame, text="Cálculos")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Panel derecho
        right_frame = ttk.LabelFrame(main_frame, text="Visualización")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.mostrar_dft_inversa(left_frame, right_frame)
    
    def mostrar_dft_inversa(self, left_frame, right_frame):
        """Mostrar ejemplo DFT inversa"""
        # Vector X del ejemplo del material
        X = np.array([6, 8+4j, -2, 8-4j])
        N = len(X)
        W = self.matriz_dft(N)
        W_inv = np.conj(W) / N
        x = W_inv @ X
        
        # Texto con scroll
        text_widget = tk.Text(left_frame, wrap=tk.WORD, font=("Courier", 9))
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        content = "EJEMPLO DFT INVERSA:\n"
        content += "=" * 40 + "\n\n"
        content += f"Vector X = {X}\n\n"
        
        content += "Matriz W* (conjugada):\n"
        W_conj = np.conj(W)
        for i in range(N):
            if i == 0:
                content += "W* = ["
            else:
                content += "     ["
            for j in range(N):
                val = W_conj[i, j]
                real_str = f"{val.real:4.1f}" if abs(val.real) > 1e-10 else "0"
                imag_str = f"{val.imag:+4.1f}j" if abs(val.imag) > 1e-10 else ""
                content += f"{real_str}{imag_str:>6}"
                if j < N-1:
                    content += ", "
            content += " ]\n"
        
        content += f"\nIDFT: x = (1/N) * W* @ X\n"
        content += f"x = {x}\n"
        content += f"Parte real: x = {x.real}\n\n"
        
        # Verificación
        X_verificacion = W @ x
        content += f"Verificación: W @ x = {X_verificacion}\n"
        content += "✓ Transformación correcta!" if np.allclose(X, X_verificacion) else "✗ Error"
        
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Gráfico
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8, 6))
        fig.suptitle('DFT Inversa - Ejemplo del Material', fontsize=12)
        
        k = np.arange(N)
        n = np.arange(N)
        
        # X magnitud
        ax1.stem(k, np.abs(X), basefmt=" ", linefmt='r-', markerfmt='ro')
        ax1.set_title('|X(k)| - Entrada')
        ax1.set_xlabel('k')
        ax1.set_ylabel('|X(k)|')
        ax1.grid(True, alpha=0.3)
        
        # X fase
        ax2.stem(k, np.angle(X), basefmt=" ", linefmt='g-', markerfmt='go')
        ax2.set_title('∠X(k) - Entrada')
        ax2.set_xlabel('k')
        ax2.set_ylabel('∠X(k) [rad]')
        ax2.grid(True, alpha=0.3)
        
        # x recuperada
        ax3.stem(n, x.real, basefmt=" ")
        ax3.set_title('x(n) - Salida IDFT')
        ax3.set_xlabel('n')
        ax3.set_ylabel('x(n)')
        ax3.grid(True, alpha=0.3)
        
        # Plano complejo X
        ax4.plot(X.real, X.imag, 'bo', markersize=8)
        for i in range(len(X)):
            ax4.annotate(f'k={i}', (X[i].real, X[i].imag), 
                        xytext=(5, 5), textcoords='offset points')
        ax4.set_title('X(k) en Plano Complejo')
        ax4.set_xlabel('Real')
        ax4.set_ylabel('Imaginario')
        ax4.grid(True, alpha=0.3)
        ax4.axis('equal')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def crear_pestaña_bases_dft(self):
        """Pestaña para vectores base DFT"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="4. Bases DFT")
        
        # Control N
        control_frame = ttk.LabelFrame(frame, text="Parámetros")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.N_bases_var = tk.IntVar(value=8)
        ttk.Label(control_frame, text="N puntos:").pack(side=tk.LEFT, padx=5)
        N_scale = ttk.Scale(control_frame, from_=4, to=16, variable=self.N_bases_var,
                           command=self.actualizar_bases_dft)
        N_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Label(control_frame, textvariable=self.N_bases_var).pack(side=tk.LEFT, padx=5)
        
        # Frame para gráfico
        self.bases_graph_frame = ttk.Frame(frame)
        self.bases_graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info
        info_frame = ttk.LabelFrame(frame, text="Información")
        info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        info_text = "Cada vector base w_k representa una frecuencia ωk = 2πk/N\n"
        info_text += "La DFT proyecta la señal x sobre estas bases complejas ortogonales"
        ttk.Label(info_frame, text=info_text, font=("Arial", 10)).pack(padx=10, pady=5)
        
        self.actualizar_bases_dft()
    
    def actualizar_bases_dft(self, event=None):
        """Actualizar visualización de bases DFT"""
        N = int(self.N_bases_var.get())
        
        # Limpiar frame
        for widget in self.bases_graph_frame.winfo_children():
            widget.destroy()
        
        # Crear figura
        num_plots = min(8, N)
        cols = 4
        rows = 2
        fig, axes = plt.subplots(rows, cols, figsize=(14, 7))
        fig.suptitle(f'Vectores Base de la DFT (N={N})', fontsize=14)
        axes = axes.flatten()
        
        for k in range(num_plots):
            # Vector base w_k
            n = np.arange(N)
            w_k = np.exp(-2j * np.pi * k * n / N)
            
            ax = axes[k]
            ax.plot(w_k.real, w_k.imag, 'bo-', markersize=6)
            
            # Círculo unitario
            theta = np.linspace(0, 2*np.pi, 100)
            ax.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3)
            
            # Numeración de puntos
            for i in range(N):
                ax.annotate(f'{i}', (w_k[i].real, w_k[i].imag), 
                           xytext=(3, 3), textcoords='offset points', 
                           fontsize=8)
            
            ax.set_title(f'Base w_{k} (k={k})')
            ax.set_xlabel('Real')
            ax.set_ylabel('Imaginario')
            ax.grid(True, alpha=0.3)
            ax.axis('equal')
            ax.set_xlim(-1.2, 1.2)
            ax.set_ylim(-1.2, 1.2)
        
        # Ocultar axes no usados
        for k in range(num_plots, len(axes)):
            axes[k].set_visible(False)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.bases_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def crear_pestaña_dft_interactiva(self):
        """Pestaña para DFT interactiva"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="5. DFT Interactiva")
        
        # Controles
        control_frame = ttk.LabelFrame(frame, text="Parámetros")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.N_dft_var = tk.IntVar(value=8)
        self.signal_type_var = tk.StringVar(value="Impulso")
        
        ttk.Label(control_frame, text="N puntos:").grid(row=0, column=0, padx=5, pady=2)
        N_scale = ttk.Scale(control_frame, from_=4, to=16, variable=self.N_dft_var,
                           command=self.actualizar_dft_interactiva)
        N_scale.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        ttk.Label(control_frame, textvariable=self.N_dft_var).grid(row=0, column=2, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Tipo de señal:").grid(row=1, column=0, padx=5, pady=2)
        signal_combo = ttk.Combobox(control_frame, textvariable=self.signal_type_var,
                                   values=["Impulso", "Escalón", "Senoidal", "Exponencial", "Aleatorio"])
        signal_combo.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        signal_combo.bind('<<ComboboxSelected>>', self.actualizar_dft_interactiva)
        
        control_frame.columnconfigure(1, weight=1)
        
        # Frame para gráfico
        self.dft_graph_frame = ttk.Frame(frame)
        self.dft_graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Info frame
        self.dft_info_frame = ttk.LabelFrame(frame, text="Información")
        self.dft_info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.dft_info_label = ttk.Label(self.dft_info_frame, text="", font=("Courier", 9))
        self.dft_info_label.pack(padx=10, pady=5)
        
        self.actualizar_dft_interactiva()
    
    def actualizar_dft_interactiva(self, event=None):
        """Actualizar DFT interactiva"""
        N = int(self.N_dft_var.get())
        signal_type = self.signal_type_var.get()
        
        # Limpiar frame
        for widget in self.dft_graph_frame.winfo_children():
            widget.destroy()
        
        # Generar señal
        n = np.arange(N)
        if signal_type == "Impulso":
            x = np.zeros(N)
            x[0] = 1
        elif signal_type == "Escalón":
            x = np.ones(N)
        elif signal_type == "Senoidal":
            x = np.cos(2 * np.pi * n / N)
        elif signal_type == "Exponencial":
            x = np.exp(-n/N)
        else:  # Aleatorio
            np.random.seed(42)  # Para reproducibilidad
            x = np.random.randn(N)
        
        # Calcular DFT
        W = self.matriz_dft(N)
        X = W @ x
        
        # Crear figura
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f'DFT Interactiva - {signal_type} (N={N})', fontsize=14)
        
        k = np.arange(N)
        
        # Señal original
        ax1.stem(n, x, basefmt=" ")
        ax1.set_title('Señal x(n)')
        ax1.set_xlabel('n')
        ax1.set_ylabel('x(n)')
        ax1.grid(True, alpha=0.3)
        
        # Magnitud DFT
        ax2.stem(k, np.abs(X), basefmt=" ", linefmt='r-', markerfmt='ro')
        ax2.set_title('Magnitud |X(k)|')
        ax2.set_xlabel('k')
        ax2.set_ylabel('|X(k)|')
        ax2.grid(True, alpha=0.3)
        
        # Fase DFT
        ax3.stem(k, np.angle(X), basefmt=" ", linefmt='g-', markerfmt='go')
        ax3.set_title('Fase ∠X(k)')
        ax3.set_xlabel('k')
        ax3.set_ylabel('∠X(k) [rad]')
        ax3.grid(True, alpha=0.3)
        
        # Plano complejo
        ax4.plot(X.real, X.imag, 'bo', markersize=8)
        for i in range(len(X)):
            ax4.annotate(f'k={i}', (X[i].real, X[i].imag), 
                        xytext=(5, 5), textcoords='offset points')
        ax4.set_title('DFT en Plano Complejo')
        ax4.set_xlabel('Real')
        ax4.set_ylabel('Imaginario')
        ax4.grid(True, alpha=0.3)
        ax4.axis('equal')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.dft_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Actualizar información
        info_text = f"Señal: {signal_type}, N = {N}\n"
        info_text += f"Frecuencias DFT: ωk = 2πk/N, k = 0, 1, ..., {N-1}\n\n"
        info_text += "Primeros valores de la DFT:\n"
        for i in range(min(4, N)):
            info_text += f"X[{i}] = {X[i]:8.3f}\n"
        
        self.dft_info_label.config(text=info_text)
    
    def crear_pestaña_ejercicio(self):
        """Pestaña para ejercicio de bonificación"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="6. Ejercicio Bonificación")
        
        # Título
        titulo = ttk.Label(frame, text="Ejercicio Bonificación: x = [5, 0, 4]", 
                          font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Frame principal
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Panel izquierdo
        left_frame = ttk.LabelFrame(main_frame, text="Cálculos Paso a Paso")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Panel derecho
        right_frame = ttk.LabelFrame(main_frame, text="Visualización")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.mostrar_ejercicio_bonificacion(left_frame, right_frame)
    
    def mostrar_ejercicio_bonificacion(self, left_frame, right_frame):
        """Mostrar ejercicio de bonificación"""
        # Vector dado
        x = np.array([5, 0, 4])
        N = len(x)
        
        # Calcular matrices
        W = self.matriz_dft(N)
        X = W @ x
        W_inv = np.conj(W) / N
        x_recuperado = W_inv @ X
        
        # Texto con scroll
        text_widget = tk.Text(left_frame, wrap=tk.WORD, font=("Courier", 8))
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        content = "EJERCICIO BONIFICACIÓN:\n"
        content += "=" * 50 + "\n"
        content += "Para el vector x = [5, 0, 4], obtener:\n"
        content += "1. Matriz W de la DFT\n"
        content += "2. Vector resultante X\n"
        content += "3. Matriz inversa W^(-1)\n"
        content += "4. Recuperar el vector x original\n\n"
        
        content += f"Vector x = {x}\n"
        content += f"N = {N}\n\n"
        
        # 1. Matriz W
        content += "1. MATRIZ W DE LA DFT:\n"
        content += "W = \n"
        for i in range(N):
            content += "    ["
            for j in range(N):
                val = W[i, j]
                real_str = f"{val.real:6.3f}" if abs(val.real) > 1e-10 else "0.000"
                imag_str = f"{val.imag:+6.3f}j" if abs(val.imag) > 1e-10 else "+0.000j"
                content += f"{real_str}{imag_str:>9}"
                if j < N-1:
                    content += ", "
            content += " ]\n"
        content += "\n"
        
        # 2. Vector X
        content += "2. VECTOR X = W @ x:\n"
        content += "Cálculo paso a paso:\n"
        for k in range(N):
            suma_str = " + ".join([f"{x[n]}*{W[k,n]:.3f}" for n in range(N)])
            content += f"X[{k}] = {suma_str} = {X[k]:.6f}\n"
        content += f"\nX = {X}\n\n"
        
        # 3. Matriz inversa
        content += "3. MATRIZ INVERSA W^(-1) = (1/N) * W*:\n"
        content += "W^(-1) = \n"
        for i in range(N):
            content += "         ["
            for j in range(N):
                val = W_inv[i, j]
                real_str = f"{val.real:6.3f}" if abs(val.real) > 1e-10 else "0.000"
                imag_str = f"{val.imag:+6.3f}j" if abs(val.imag) > 1e-10 else "+0.000j"
                content += f"{real_str}{imag_str:>9}"
                if j < N-1:
                    content += ", "
            content += " ]\n"
        content += "\n"
        
        # 4. Recuperar x
        content += "4. RECUPERAR x = W^(-1) @ X:\n"
        content += "Cálculo paso a paso:\n"
        for n in range(N):
            suma_str = " + ".join([f"{X[k]:.3f}*{W_inv[n,k]:.3f}" for k in range(N)])
            content += f"x[{n}] = {suma_str} = {x_recuperado[n]:.6f}\n"
        
        content += f"\nx recuperado = {x_recuperado.real}\n"
        content += f"x original   = {x}\n"
        content += "✓ Verificación exitosa!" if np.allclose(x, x_recuperado.real) else "✗ Error"
        
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Gráfico
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8, 6))
        fig.suptitle('Ejercicio Bonificación: x = [5, 0, 4]', fontsize=12)
        
        n = np.arange(N)
        k = np.arange(N)
        
        # Señal original
        ax1.stem(n, x, basefmt=" ")
        ax1.set_title('Señal Original x(n)')
        ax1.set_xlabel('n')
        ax1.set_ylabel('x(n)')
        ax1.grid(True, alpha=0.3)
        
        # DFT magnitud
        ax2.stem(k, np.abs(X), basefmt=" ", linefmt='r-', markerfmt='ro')
        ax2.set_title('Magnitud |X(k)|')
        ax2.set_xlabel('k')
        ax2.set_ylabel('|X(k)|')
        ax2.grid(True, alpha=0.3)
        
        # DFT fase
        ax3.stem(k, np.angle(X), basefmt=" ", linefmt='g-', markerfmt='go')
        ax3.set_title('Fase ∠X(k)')
        ax3.set_xlabel('k')
        ax3.set_ylabel('∠X(k) [rad]')
        ax3.grid(True, alpha=0.3)
        
        # Señal recuperada
        ax4.stem(n, x_recuperado.real, basefmt=" ", linefmt='purple', markerfmt='mo')
        ax4.set_title('Señal Recuperada (IDFT)')
        ax4.set_xlabel('n')
        ax4.set_ylabel('x(n)')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        app = DFTInteractivaGUI()
        app.ejecutar()
    except Exception as e:
        messagebox.showerror("Error", f"Error al ejecutar la aplicación: {e}")

if __name__ == "__main__":
    main()