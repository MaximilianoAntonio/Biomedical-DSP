import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy.signal import lfilter, firwin, butter

def crear_fir(numtaps, cutoff, fs):
    # Filtro FIR pasa bajas
    return firwin(numtaps, cutoff, fs=fs)

def crear_iir(order, cutoff, fs):
    # Filtro IIR pasa bajas Butterworth
    b, a = butter(order, cutoff, fs=fs)
    return b, a

def plot_fir_iir_comparacion():
    fs = 8000
    t = np.linspace(0, 0.04, int(fs*0.04), endpoint=False)
    # Señal: suma de dos senoidales
    f1, f2 = 440, 2000
    x = np.sin(2*np.pi*f1*t) + 0.5*np.sin(2*np.pi*f2*t)

    # Título general con la función original y su composición
    titulo = (
        "Función original: x(t) = sin(2π·440·t) + 0.5·sin(2π·2000·t)\n"
        "Composición: suma de una senoidal de 440 Hz y otra de 2000 Hz (amplitud 0.5)"
    )

    fig, axs = plt.subplots(2, 2, figsize=(13, 7))
    fig.suptitle(titulo, fontsize=13, y=0.97)
    plt.subplots_adjust(left=0.08, bottom=0.28, hspace=0.35, wspace=0.25)

    # Filtros iniciales
    fir_order_init = 100
    iir_order_init = 2
    cutoff_init = 1000
    fir_coef = crear_fir(fir_order_init+1, cutoff_init, fs)
    iir_b, iir_a = crear_iir(iir_order_init, cutoff_init, fs)
    y_fir = lfilter(fir_coef, 1, x)
    y_iir = lfilter(iir_b, iir_a, x)

    # Señal original y FIR
    axs[0,0].set_title("Original y salida FIR (pasa bajas)")
    l_x0, = axs[0,0].plot(t*1e3, x, 'b', label="Original")
    l_yfir, = axs[0,0].plot(t*1e3, y_fir, 'r', label="FIR")
    axs[0,0].set_xlim(0, 40)
    axs[0,0].set_xlabel("Tiempo [ms]")
    axs[0,0].set_ylabel("Amplitud")
    axs[0,0].legend()
    axs[0,0].grid(True)

    # Señal original y IIR
    axs[0,1].set_title("Original y salida IIR (pasa bajas)")
    l_x1, = axs[0,1].plot(t*1e3, x, 'b', label="Original")
    l_yiir, = axs[0,1].plot(t*1e3, y_iir, 'g', label="IIR")
    axs[0,1].set_xlim(0, 40)
    axs[0,1].set_xlabel("Tiempo [ms]")
    axs[0,1].set_ylabel("Amplitud")
    axs[0,1].legend()
    axs[0,1].grid(True)

    # Respuesta al impulso FIR
    axs[1,0].set_title("Respuesta al impulso FIR")
    h_fir = fir_coef
    n_fir = np.arange(len(h_fir))
    l_hfir = axs[1,0].stem(n_fir, h_fir, linefmt='C1-', markerfmt='C1o', basefmt=" ")
    axs[1,0].set_xlabel("n")
    axs[1,0].set_ylabel("h[n]")
    axs[1,0].grid(True)

    # Respuesta al impulso IIR
    axs[1,1].set_title("Respuesta al impulso IIR")
    impulse = np.zeros(100)
    impulse[0] = 1
    h_iir = lfilter(iir_b, iir_a, impulse)
    n_iir = np.arange(len(h_iir))
    l_hiir = axs[1,1].stem(n_iir, h_iir, linefmt='C2-', markerfmt='C2o', basefmt=" ")
    axs[1,1].set_xlabel("n")
    axs[1,1].set_ylabel("h[n]")
    axs[1,1].grid(True)

    # Sliders
    axcolor = 'lightgoldenrodyellow'
    ax_fir = plt.axes([0.12, 0.18, 0.3, 0.03], facecolor=axcolor)
    ax_iir = plt.axes([0.57, 0.18, 0.3, 0.03], facecolor=axcolor)
    ax_cut = plt.axes([0.12, 0.13, 0.75, 0.03], facecolor=axcolor)
    s_fir = Slider(ax_fir, 'Orden FIR', 10, 200, valinit=fir_order_init, valstep=1)
    s_iir = Slider(ax_iir, 'Orden IIR', 1, 8, valinit=iir_order_init, valstep=1)
    s_cut = Slider(ax_cut, 'Frecuencia de corte [Hz]', 200, 3000, valinit=cutoff_init, valstep=10)

    def update(_):
        nonlocal l_hfir, l_hiir
        fir_order = int(s_fir.val)
        iir_order = int(s_iir.val)
        cutoff = s_cut.val
        fir_coef = crear_fir(fir_order+1, cutoff, fs)
        iir_b, iir_a = crear_iir(iir_order, cutoff, fs)
        y_fir = lfilter(fir_coef, 1, x)
        y_iir = lfilter(iir_b, iir_a, x)
        # Señal filtrada
        l_yfir.set_ydata(y_fir)
        l_yiir.set_ydata(y_iir)
        # Respuesta al impulso FIR
        for artist in l_hfir:
            try:
                artist.remove()
            except Exception:
                pass
        h_fir = fir_coef
        n_fir = np.arange(len(h_fir))
        l_hfir_new = axs[1,0].stem(n_fir, h_fir, linefmt='C1-', markerfmt='C1o', basefmt=" ")
        l_hfir = l_hfir_new
        # Respuesta al impulso IIR
        for artist in l_hiir:
            try:
                artist.remove()
            except Exception:
                pass
        impulse = np.zeros(100)
        impulse[0] = 1
        h_iir = lfilter(iir_b, iir_a, impulse)
        n_iir = np.arange(len(h_iir))
        l_hiir_new = axs[1,1].stem(n_iir, h_iir, linefmt='C2-', markerfmt='C2o', basefmt=" ")
        l_hiir = l_hiir_new
        fig.canvas.draw_idle()

    s_fir.on_changed(update)
    s_iir.on_changed(update)
    s_cut.on_changed(update)

    # Botón de reset
    resetax = plt.axes([0.85, 0.05, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    def reset(_):
        s_fir.reset()
        s_iir.reset()
        s_cut.reset()
    button.on_clicked(reset)

    plt.show()

if __name__ == "__main__":
    plot_fir_iir_comparacion()
