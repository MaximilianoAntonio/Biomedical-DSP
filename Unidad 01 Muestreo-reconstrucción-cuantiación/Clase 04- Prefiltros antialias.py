import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def X_in(f):
    # f en kHz, devuelve |X_in(f)| según la fórmula de Orfanidis
    return 1 / np.sqrt(1 + (0.1 * f)**8)

def X_in_alias(f, fs):
    # Primera réplica desplazada a fs (fs en kHz)
    return 1 / np.sqrt(1 + (0.1 * (f - fs))**8)

def atenuacion_db(f, fs):
    # Atenuación en dB de la réplica respecto al valor máximo
    num = X_in_alias(f, fs)
    den = X_in(f)
    return -20 * np.log10(num / den)

def plot_antialias_Orfanidis():
    fmax = 20  # kHz
    fs_init = 60  # kHz
    fs_min = 25
    fs_max = 200
    A_req = 60  # dB

    f_axis = np.linspace(0, fs_max, 2000)  # 0 a fs_max kHz (ajuste para ver todo el rango)

    fig, axs = plt.subplots(2, 1, figsize=(10, 7))
    plt.subplots_adjust(left=0.1, bottom=0.25, hspace=0.4)

    # Espectro original y réplica
    axs[0].set_title("Espectro original y réplica desplazada")
    l_orig, = axs[0].plot(f_axis, X_in(f_axis), label="|X_in(f)|", color='C0', lw=2)
    l_alias, = axs[0].plot(f_axis, X_in_alias(f_axis, fs_init), label="|X_in(f - f_s)|", color='C1', lw=2)
    axs[0].axvline(fmax, color='k', linestyle='--', alpha=0.7, label='$f_{max}$')
    fs_line = axs[0].axvline(fs_init, color='r', linestyle=':', alpha=0.7, label='$f_s$')
    axs[0].set_xlabel("Frecuencia [kHz]")
    axs[0].set_ylabel("Amplitud normalizada")
    axs[0].set_xlim(0, fs_max)  # Mostrar todo el rango de fs
    axs[0].set_ylim(-0.05, 1.05)
    axs[0].grid(True)
    axs[0].legend(loc="upper right", fontsize=10)

    # Atenuación en dB de la réplica
    axs[1].set_title("Atenuación de la réplica en $f_{max}$ respecto a $|X_{in}(f_{max})|$")
    l_att, = axs[1].plot([], [], 'r', label="Atenuación (dB)")
    att_point, = axs[1].plot([], [], 'ko', label="Atenuación en $f_{max}$")
    axs[1].axhline(-A_req, color='g', linestyle='--', label=f"-{A_req} dB")
    axs[1].set_xlabel("$f_s$ [kHz]")
    axs[1].set_ylabel("Atenuación (dB)")
    axs[1].set_xlim(fs_min, fs_max)
    axs[1].set_ylim(-100, 0)
    axs[1].grid(True)
    axs[1].legend()

    # Slider para fs
    axcolor = 'lightgoldenrodyellow'
    ax_fs = plt.axes([0.15, 0.13, 0.7, 0.03], facecolor=axcolor)
    s_fs = Slider(ax_fs, 'Frecuencia de muestreo $f_s$ [kHz]', fs_min, fs_max, valinit=fs_init)

    # Texto para mostrar si cumple la condición
    ax_text = plt.axes([0.15, 0.06, 0.7, 0.04])
    ax_text.axis('off')
    cond_text = ax_text.text(0.02, 0.5, "", fontsize=13, va='center')

    def update(_):
        fs = s_fs.val
        # Update espectros
        l_orig.set_ydata(X_in(f_axis))
        l_alias.set_ydata(X_in_alias(f_axis, fs))
        fs_line.set_xdata([fs, fs])
        axs[0].set_xlim(0, fs_max)  # Mantener el mismo límite al actualizar

        # Atenuación en dB para fs en el rango
        fs_range = np.linspace(fs_min, fs_max, 300)
        att_db = -20 * np.log10(X_in_alias(fmax, fs_range) / X_in(fmax))
        l_att.set_data(fs_range, -att_db)
        att_fs = -20 * np.log10(X_in_alias(fmax, fs) / X_in(fmax))
        att_point.set_data([fs], [-att_fs])

        # Mensaje de condición
        if att_fs >= A_req:
            cond_text.set_text(f"¡Cumple! Atenuación = {att_fs:.1f} dB ≥ {A_req} dB")
            cond_text.set_color('green')
        else:
            cond_text.set_text(f"No cumple: Atenuación = {att_fs:.1f} dB < {A_req} dB")
            cond_text.set_color('red')

        fig.canvas.draw_idle()

    s_fs.on_changed(update)

    # Inicializar gráfico de atenuación
    update(None)

    # Botón de reset
    resetax = plt.axes([0.85, 0.02, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    def reset(_):
        s_fs.reset()
    button.on_clicked(reset)

    plt.show()

if __name__ == "__main__":
    plot_antialias_Orfanidis()
