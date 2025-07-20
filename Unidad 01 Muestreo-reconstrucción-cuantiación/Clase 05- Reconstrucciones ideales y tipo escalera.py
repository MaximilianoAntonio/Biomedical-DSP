import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def h_ideal(t, fs):
    # Reconstr. ideal: sinc(pi*fs*t)/(pi*t) = fs * sinc(fs*t)
    return np.sinc(fs * t)

def h_escalera(t, T):
    # Reconstr. en escalera: 1 para 0 <= t <= T, 0 en otro caso
    return np.where((t >= 0) & (t <= T), 1.0, 0.0)

def reconstruccion(xn, n, t, h_func, *h_args):
    # Suma de convoluciones desplazadas: sum_n x[n] * h(t - nT)
    y = np.zeros_like(t)
    for i, ni in enumerate(n):
        y += xn[i] * h_func(t - ni, *h_args)
    return y

def plot_reconstruccion():
    # Parámetros de la señal y muestreo
    fs = 10  # Hz
    T = 1/fs
    t = np.linspace(-1, 2, 2000)
    n = np.arange(0, 2, T)
    f0 = 2  # Hz
    xn = np.cos(2 * np.pi * f0 * n)  # señal muestreada

    # Reconstrucción ideal y escalera
    y_ideal = reconstruccion(xn, n, t, h_ideal, fs)
    y_stair = reconstruccion(xn, n, t, h_escalera, T)

    fig, axs = plt.subplots(2, 1, figsize=(10, 7))
    plt.subplots_adjust(left=0.1, bottom=0.25, hspace=0.4)

    # Señal original y muestras
    axs[0].set_title("Reconstrucción ideal vs escalera")
    axs[0].plot(t, np.cos(2 * np.pi * f0 * t), 'k--', label="Señal original")
    # Guardar el stem inicial para poder actualizarlo correctamente
    stem_container = axs[0].stem(n, xn, linefmt='C2-', markerfmt='C2o', basefmt=" ", label="Muestras")
    axs[0].set_xlim(-0.2, 2)
    axs[0].set_ylim(-1.5, 1.5)
    l_ideal, = axs[0].plot(t, y_ideal, 'b', label="Reconstrucción ideal")
    l_stair, = axs[0].plot(t, y_stair, 'r', label="Reconstrucción escalera")
    axs[0].legend()
    axs[0].grid(True)

    # Respuestas al impulso
    t_h = np.linspace(-1, 1, 1000)
    axs[1].set_title("Respuestas al impulso $h(t)$")
    l_hi, = axs[1].plot(t_h, h_ideal(t_h, fs), 'b', label="Ideal")
    l_hs, = axs[1].plot(t_h, h_escalera(t_h, T), 'r', label="Escalera")
    axs[1].set_xlim(-0.5, 0.5)
    axs[1].legend()
    axs[1].grid(True)

    # Sliders
    axcolor = 'lightgoldenrodyellow'
    ax_f0 = plt.axes([0.15, 0.15, 0.7, 0.03], facecolor=axcolor)
    ax_fs = plt.axes([0.15, 0.1, 0.7, 0.03], facecolor=axcolor)
    s_f0 = Slider(ax_f0, 'Frecuencia señal $f_0$ [Hz]', 0.5, 4, valinit=f0)
    s_fs = Slider(ax_fs, 'Frecuencia muestreo $f_s$ [Hz]', 6, 30, valinit=fs)

    def update(_):
        nonlocal stem_container  # <-- Mueve esto al inicio de la función
        f0 = s_f0.val
        fs = s_fs.val
        T = 1/fs
        n = np.arange(0, 2, T)
        xn = np.cos(2 * np.pi * f0 * n)
        y_ideal = reconstruccion(xn, n, t, h_ideal, fs)
        y_stair = reconstruccion(xn, n, t, h_escalera, T)
        l_ideal.set_ydata(y_ideal)
        l_stair.set_ydata(y_stair)
        axs[0].lines[0].set_ydata(np.cos(2 * np.pi * f0 * t))
        # Eliminar el stem anterior (líneas, marcadores y base)
        for artist in stem_container:
            try:
                artist.remove()
            except Exception:
                pass
        # Crear nuevo stem y guardar sus artistas
        new_stem = axs[0].stem(n, xn, linefmt='C2-', markerfmt='C2o', basefmt=" ")
        stem_container = new_stem
        l_hi.set_ydata(h_ideal(t_h, fs))
        l_hs.set_ydata(h_escalera(t_h, T))
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
    plot_reconstruccion()
    plot_reconstruccion()
