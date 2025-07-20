import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def h_ejemplo1(n):
    # h(n) = (0.5)^n * u(n)
    return (0.5)**n * (n >= 0)

def h_ejemplo2(n):
    # h(n) = -(0.5)^n * u(-n-1)
    return -(0.5)**n * (n <= -1)

def h_ejemplo3_causal(n):
    # h(n) = 2^n * u(n)
    return (2.0)**n * (n >= 0)

def h_ejemplo3_anticausal(n):
    # h(n) = -2^n * u(-n-1)
    return -(2.0)**n * (n <= -1)

def plot_causalidad_estabilidad():
    n = np.arange(-20, 20)
    fig, axs = plt.subplots(2, 2, figsize=(12, 7))
    plt.subplots_adjust(left=0.1, bottom=0.25, hspace=0.4, wspace=0.3)
    fig.suptitle("Ejemplos de causalidad y estabilidad de sistemas LTI", fontsize=14, y=0.98)

    # Ejemplo 1: estable y causal
    axs[0,0].set_title("Ejemplo 1: $h(n) = (0.5)^n u(n)$ (estable y causal)")
    h1 = h_ejemplo1(n)
    axs[0,0].stem(n, h1)  # <-- quitar use_line_collection
    axs[0,0].set_xlabel("n")
    axs[0,0].set_ylabel("h(n)")
    axs[0,0].grid(True)

    # Ejemplo 2: inestable y anticausal
    axs[0,1].set_title("Ejemplo 2: $h(n) = -(0.5)^n u(-n-1)$ (inestable y anticausal)")
    h2 = h_ejemplo2(n)
    axs[0,1].stem(n, h2)  # <-- quitar use_line_collection
    axs[0,1].set_xlabel("n")
    axs[0,1].set_ylabel("h(n)")
    axs[0,1].grid(True)

    # Ejemplo 3: causal/anticausal y estable/inestable
    axs[1,0].set_title("Ejemplo 3: $h(n) = 2^n u(n)$ (causal, inestable)")
    h3c = h_ejemplo3_causal(n)
    axs[1,0].stem(n, h3c)  # <-- quitar use_line_collection
    axs[1,0].set_xlabel("n")
    axs[1,0].set_ylabel("h(n)")
    axs[1,0].set_ylim(-1, 1e6)
    axs[1,0].set_yscale('symlog', linthresh=1)
    axs[1,0].grid(True)

    axs[1,1].set_title("Ejemplo 3: $h(n) = -2^n u(-n-1)$ (anticausal, estable)")
    h3a = h_ejemplo3_anticausal(n)
    axs[1,1].stem(n, h3a)  # <-- quitar use_line_collection
    axs[1,1].set_xlabel("n")
    axs[1,1].set_ylabel("h(n)")
    axs[1,1].set_ylim(-1e6, 1)
    axs[1,1].set_yscale('symlog', linthresh=1)
    axs[1,1].grid(True)

    plt.show()

if __name__ == "__main__":
    plot_causalidad_estabilidad()
