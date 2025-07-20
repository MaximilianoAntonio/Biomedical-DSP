import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def cuantizar(x, R, B):
    Q = R / (2**B)
    xq = np.clip(np.round(x / Q) * Q, -R/2, R/2 - Q)
    return xq

def error_rms(R, B):
    Q = R / (2**B)
    return Q / np.sqrt(12)

def snr_db(B):
    return 6 * B

def plot_cuantizacion():
    # Parámetros iniciales
    R_init = 10
    B_init = 4
    fs = 44_000
    t = np.linspace(0, 1e-3, 1000)
    f0 = 1000
    x = (R_init/2) * np.sin(2 * np.pi * f0 * t)

    fig, axs = plt.subplots(2, 2, figsize=(12, 7))
    plt.subplots_adjust(left=0.1, bottom=0.32, hspace=0.5)

    # Señal original y cuantizada
    xq = cuantizar(x, R_init, B_init)
    axs[0,0].set_title("Señal original vs cuantizada")
    l_x, = axs[0,0].plot(t*1e3, x, label="Original")
    l_xq, = axs[0,0].step(t*1e3, xq, where='mid', label="Cuantizada")
    axs[0,0].set_xlabel("Tiempo [ms]")
    axs[0,0].set_ylabel("Amplitud [V]")
    axs[0,0].legend()
    axs[0,0].grid(True)

    # Error de cuantización
    axs[0,1].set_title("Error de cuantización")
    l_err, = axs[0,1].plot(t*1e3, xq-x)
    axs[0,1].set_xlabel("Tiempo [ms]")
    axs[0,1].set_ylabel("Error [V]")
    axs[0,1].grid(True)

    # Error RMS y SNR
    axs[1,0].set_title("Error RMS y SNR vs bits")
    bits = np.arange(2, 21)
    err_rms = error_rms(R_init, bits)
    snr = snr_db(bits)
    l_rms, = axs[1,0].plot(bits, err_rms*1e6, 'b-o', label="Error RMS [$\\mu$V]")
    l_snr, = axs[1,0].plot(bits, snr, 'r-s', label="SNR [dB]")
    axs[1,0].set_xlabel("Bits")
    axs[1,0].set_ylabel("Error RMS [$\\mu$V] / SNR [dB]")
    axs[1,0].legend()
    axs[1,0].grid(True)

    # Niveles de cuantización
    axs[1,1].set_title("Niveles de cuantización")
    Q = R_init / (2**B_init)
    levels = np.arange(-R_init/2, R_init/2, Q)
    axs[1,1].hlines(levels, 0, 1, colors='k', lw=2)
    axs[1,1].set_xlim(0, 1)
    axs[1,1].set_ylim(-R_init/2-0.1, R_init/2+0.1)
    axs[1,1].set_xlabel("Eje ficticio")
    axs[1,1].set_ylabel("Nivel [V]")
    axs[1,1].grid(True)

    # Sliders
    axcolor = 'lightgoldenrodyellow'
    ax_R = plt.axes([0.15, 0.22, 0.7, 0.03], facecolor=axcolor)
    ax_B = plt.axes([0.15, 0.17, 0.7, 0.03], facecolor=axcolor)
    s_R = Slider(ax_R, 'Rango $R$ [V]', 1, 20, valinit=R_init)
    s_B = Slider(ax_B, 'Bits $B$', 2, 20, valinit=B_init, valstep=1)

    # Texto para mostrar valores clave
    ax_text = plt.axes([0.15, 0.12, 0.7, 0.03])
    ax_text.axis('off')
    info_text = ax_text.text(0.02, 0.5, "", fontsize=12, va='center')

    def update(_):
        R = s_R.val
        B = int(s_B.val)
        x = (R/2) * np.sin(2 * np.pi * f0 * t)
        xq = cuantizar(x, R, B)
        l_x.set_ydata(x)
        l_xq.set_ydata(xq)
        l_err.set_ydata(xq-x)
        # Error RMS y SNR
        err_rms = error_rms(R, bits)
        l_rms.set_ydata(err_rms*1e6)
        l_snr.set_ydata(snr_db(bits))
        # Niveles de cuantización
        axs[1,1].cla()
        axs[1,1].set_title("Niveles de cuantización")
        Q = R / (2**B)
        levels = np.arange(-R/2, R/2, Q)
        axs[1,1].hlines(levels, 0, 1, colors='k', lw=2)
        axs[1,1].set_xlim(0, 1)
        axs[1,1].set_ylim(-R/2-0.1, R/2+0.1)
        axs[1,1].set_xlabel("Eje ficticio")
        axs[1,1].set_ylabel("Nivel [V]")
        axs[1,1].grid(True)
        # Info
        info_text.set_text(
            f"Q = {Q:.4f} V, Error RMS = {error_rms(R,B)*1e6:.1f} μV, SNR = {snr_db(B):.1f} dB, Niveles = {2**B}"
        )
        fig.canvas.draw_idle()

    s_R.on_changed(update)
    s_B.on_changed(update)

    # Botón de reset
    resetax = plt.axes([0.85, 0.05, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    def reset(_):
        s_R.reset()
        s_B.reset()
    button.on_clicked(reset)

    plt.show()

if __name__ == "__main__":
    plot_cuantizacion()
