import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def frecuencia_alias(f, fs):
    # Calcula la frecuencia alias en el intervalo de Nyquist
    fa = ((f + fs/2) % fs) - fs/2
    return fa

def plot_muestreo_aliasing():
    # Parámetros iniciales
    f_init = 10      # Frecuencia señal [Hz]
    fs_init = 12     # Frecuencia de muestreo [Hz]
    tmax = 1         # Duración [s]
    N = 1000         # Puntos para señal continua

    # Figura y ejes
    fig, axs = plt.subplots(2, 2, figsize=(12, 7))
    plt.subplots_adjust(left=0.1, bottom=0.32, hspace=0.5)

    # Tiempo continuo y discreto
    t = np.linspace(0, tmax, N)
    n = np.arange(0, tmax, 1/fs_init)

    # Señal original y muestreada
    x = np.cos(2*np.pi*f_init*t)
    x_n = np.cos(2*np.pi*f_init*n)

    # Señal reconstruida (alias)
    fa_init = frecuencia_alias(f_init, fs_init)
    x_alias = np.cos(2*np.pi*fa_init*t)

    # Gráfico señal continua y muestreada
    axs[0,0].set_title("Señal continua y muestreada")
    l_x, = axs[0,0].plot(t, x, label="Señal original")
    stem_container = axs[0,0].stem(n, x_n, linefmt='C1-', markerfmt='C1o', basefmt=" ", label="Muestras")
    axs[0,0].legend()
    axs[0,0].set_xlim(0, tmax)
    axs[0,0].grid(True)
    # Guardar los artistas del stem para eliminarlos después
    stem_artists = list(stem_container)

    # Gráfico señal reconstruida (alias)
    axs[1,0].set_title("Señal reconstruida (alias)")
    l_alias, = axs[1,0].plot(t, x_alias, 'r', label="Alias")
    axs[1,0].set_xlim(0, tmax)
    axs[1,0].legend()
    axs[1,0].grid(True)

    # Espectro de la señal muestreada (réplicas)
    f_axis = np.linspace(-3*fs_init, 3*fs_init, 1000)
    spectrum = np.zeros_like(f_axis)
    for m in range(-3, 4):
        spectrum += np.exp(-((f_axis-(f_init+m*fs_init))/0.2)**2)
    axs[0,1].set_title("Réplicas en el espectro (Hz)")
    l_spec, = axs[0,1].plot(f_axis, spectrum)
    axs[0,1].axvline(fs_init/2, color='k', linestyle='--', alpha=0.5, label='Nyquist')
    axs[0,1].axvline(-fs_init/2, color='k', linestyle='--', alpha=0.5)
    axs[0,1].set_xlim(-2*fs_init, 2*fs_init)
    axs[0,1].legend(["Espectro", "Nyquist"])
    axs[0,1].grid(True)

    # Frecuencia alias vs frecuencia original
    f_vals = np.linspace(0, 2*fs_init, 500)
    fa_vals = frecuencia_alias(f_vals, fs_init)
    axs[1,1].set_title("Frecuencia alias vs frecuencia original")
    l_fa, = axs[1,1].plot(f_vals, fa_vals)
    axs[1,1].set_xlabel("Frecuencia original (Hz)")
    axs[1,1].set_ylabel("Frecuencia alias (Hz)")
    axs[1,1].axhline(fs_init/2, color='k', linestyle='--', alpha=0.5)
    axs[1,1].axhline(-fs_init/2, color='k', linestyle='--', alpha=0.5)
    axs[1,1].set_ylim(-fs_init, fs_init)
    axs[1,1].set_xlim(0, 2*fs_init)
    axs[1,1].grid(True)

    # Sliders
    axcolor = 'lightgoldenrodyellow'
    ax_f = plt.axes([0.15, 0.22, 0.7, 0.03], facecolor=axcolor)
    ax_fs = plt.axes([0.15, 0.17, 0.7, 0.03], facecolor=axcolor)
    s_f = Slider(ax_f, 'Frecuencia señal [Hz]', 0.1, 40, valinit=f_init)
    s_fs = Slider(ax_fs, 'Frecuencia muestreo [Hz]', 2, 50, valinit=fs_init)

    # Texto para mostrar la frecuencia alias
    txt_alias = plt.axes([0.15, 0.12, 0.7, 0.03])
    txt_alias.axis('off')
    alias_text = txt_alias.text(0.02, 0.5, f"Frecuencia alias: {fa_init:.2f} Hz", fontsize=12, va='center')

    def update(_):
        nonlocal stem_artists
        f = s_f.val
        fs = s_fs.val
        n = np.arange(0, tmax, 1/fs)
        x = np.cos(2*np.pi*f*t)
        x_n = np.cos(2*np.pi*f*n)
        fa = frecuencia_alias(f, fs)
        x_alias = np.cos(2*np.pi*fa*t)

        # Update señal continua
        l_x.set_ydata(x)
        # Eliminar el stem anterior (líneas, marcadores y base)
        for artist in stem_artists:
            try:
                artist.remove()
            except Exception:
                pass
        # Crear nuevo stem y guardar sus artistas
        new_stem = axs[0,0].stem(n, x_n, linefmt='C1-', markerfmt='C1o', basefmt=" ")
        stem_artists = list(new_stem)
        axs[0,0].set_xlim(0, tmax)
        if axs[0,0].get_legend() is not None:
            axs[0,0].get_legend().remove()

        # Update alias
        l_alias.set_ydata(x_alias)

        # Update espectro
        f_axis = np.linspace(-3*fs, 3*fs, 1000)
        spectrum = np.zeros_like(f_axis)
        for m in range(-3, 4):
            spectrum += np.exp(-((f_axis-(f+m*fs))/0.2)**2)
        l_spec.set_data(f_axis, spectrum)
        axs[0,1].set_xlim(-2*fs, 2*fs)
        axs[0,1].lines[1].set_xdata([fs/2, fs/2])
        axs[0,1].lines[2].set_xdata([-fs/2, -fs/2])

        # Update frecuencia alias plot
        f_vals = np.linspace(0, 2*fs, 500)
        fa_vals = frecuencia_alias(f_vals, fs)
        l_fa.set_data(f_vals, fa_vals)
        axs[1,1].set_ylim(-fs, fs)
        axs[1,1].set_xlim(0, 2*fs)
        axs[1,1].lines[1].set_ydata([fs/2]*2)
        axs[1,1].lines[2].set_ydata([-fs/2]*2)

        # Update alias text
        alias_text.set_text(f"Frecuencia alias: {fa:.2f} Hz")

        fig.canvas.draw_idle()

    s_f.on_changed(update)
    s_fs.on_changed(update)

    # Botón de reset
    resetax = plt.axes([0.85, 0.05, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    def reset(_):
        s_f.reset()
        s_fs.reset()
    button.on_clicked(reset)

    plt.show()

if __name__ == "__main__":
    plot_muestreo_aliasing()
