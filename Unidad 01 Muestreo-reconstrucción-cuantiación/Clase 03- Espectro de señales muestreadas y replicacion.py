import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def espectro_senoidal(f0, f_axis):
    # Espectro ideal de una senoidal: dos deltas en ±f0 (simulado como picos estrechos)
    return np.exp(-((f_axis-f0)/0.1)**2) + np.exp(-((f_axis+f0)/0.1)**2)

def espectro_muestreado(f0, fs, f_axis, replicas=5):
    # Suma de réplicas desplazadas por múltiplos de fs
    spectrum = np.zeros_like(f_axis)
    for m in range(-replicas, replicas+1):
        spectrum += espectro_senoidal(f0 + m*fs, f_axis)
    return spectrum

def plot_espectro_muestreo():
    # Parámetros iniciales
    f0_init = 5      # Frecuencia de la senoidal [Hz]
    fs_init = 20     # Frecuencia de muestreo [Hz]
    replicas = 5
    fmax = 50
    f_axis = np.linspace(-fmax, fmax, 2000)

    # Figura y ejes
    fig, axs = plt.subplots(2, 1, figsize=(10, 7))
    plt.subplots_adjust(left=0.1, bottom=0.25, hspace=0.4)

    # Espectro original
    axs[0].set_title("Espectro de la señal original")
    l_orig, = axs[0].plot(f_axis, espectro_senoidal(f0_init, f_axis), label="X(f)")
    axs[0].set_xlim(-fmax, fmax)
    axs[0].set_ylim(0, 1.2)
    axs[0].set_xlabel("Frecuencia [Hz]")
    axs[0].set_ylabel("|X(f)|")
    axs[0].grid(True)
    axs[0].legend()

    # Espectro muestreado (réplicas)
    axs[1].set_title("Espectro tras muestreo (réplicas cada $f_s$)")
    l_muest, = axs[1].plot(f_axis, espectro_muestreado(f0_init, fs_init, f_axis, replicas), label="$\\hat{X}(f)$")
    nyq_line1 = axs[1].axvline(fs_init/2, color='k', linestyle='--', alpha=0.7, label='Nyquist')
    nyq_line2 = axs[1].axvline(-fs_init/2, color='k', linestyle='--', alpha=0.7)
    axs[1].set_xlim(-fmax, fmax)
    axs[1].set_ylim(0, 1.2)
    axs[1].set_xlabel("Frecuencia [Hz]")
    axs[1].set_ylabel("|$\\hat{X}(f)$|")
    axs[1].grid(True)
    axs[1].legend()

    # Sliders
    axcolor = 'lightgoldenrodyellow'
    ax_f0 = plt.axes([0.15, 0.15, 0.7, 0.03], facecolor=axcolor)
    ax_fs = plt.axes([0.15, 0.1, 0.7, 0.03], facecolor=axcolor)
    s_f0 = Slider(ax_f0, 'Frecuencia señal $f_0$ [Hz]', 0.5, 20, valinit=f0_init)
    s_fs = Slider(ax_fs, 'Frecuencia muestreo $f_s$ [Hz]', 5, 40, valinit=fs_init)

    # Texto para mostrar si hay aliasing
    ax_alias = plt.axes([0.15, 0.05, 0.7, 0.03])
    ax_alias.axis('off')
    alias_text = ax_alias.text(0.02, 0.5, "", fontsize=13, va='center', color='red')

    def update(_):
        f0 = s_f0.val
        fs = s_fs.val
        # Update espectro original
        l_orig.set_ydata(espectro_senoidal(f0, f_axis))
        # Update espectro muestreado
        l_muest.set_ydata(espectro_muestreado(f0, fs, f_axis, replicas))
        # Update líneas de Nyquist
        nyq_line1.set_xdata([fs/2, fs/2])
        nyq_line2.set_xdata([-fs/2, -fs/2])
        # Aviso de aliasing
        if f0 > fs/2:
            alias_text.set_text("¡Hay aliasing! (f₀ > fₛ/2)")
            alias_text.set_color('red')
        else:
            alias_text.set_text("No hay aliasing (f₀ ≤ fₛ/2)")
            alias_text.set_color('green')
        fig.canvas.draw_idle()

    s_f0.on_changed(update)
    s_fs.on_changed(update)

    # Botón de reset
    resetax = plt.axes([0.85, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    def reset(_):
        s_f0.reset()
        s_fs.reset()
    button.on_clicked(reset)

    plt.show()

if __name__ == "__main__":
    plot_espectro_muestreo()
