import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def ventana_rect(L):
    return np.ones(L)

def ventana_hamming(L):
    n = np.arange(L)
    return 0.54 - 0.46 * np.cos(2 * np.pi * n / (L - 1))

def ventana_hann(L):
    n = np.arange(L)
    return 0.5 - 0.5 * np.cos(2 * np.pi * n / (L - 1))

def ventana_blackman(L):
    n = np.arange(L)
    return 0.42 - 0.5 * np.cos(2 * np.pi * n / (L - 1)) + 0.08 * np.cos(4 * np.pi * n / (L - 1))

def senal_cos(L, f0, fs):
    n = np.arange(L)
    w0 = 2 * np.pi * f0 / fs
    return np.cos(w0 * n)

def plot_ventaneo():
    # Parámetros iniciales
    fs = 1000
    f0 = 50
    L_init = 100

    # Señal y ventanas iniciales
    x = senal_cos(L_init, f0, fs)
    w_rect = ventana_rect(L_init)
    w_ham = ventana_hamming(L_init)
    w_hann = ventana_hann(L_init)
    w_black = ventana_blackman(L_init)
    x_rect = x * w_rect
    x_ham = x * w_ham
    x_hann = x * w_hann
    x_black = x * w_black

    # FFT
    Nfft = 2048
    def calc_fft(xw):
        X = np.fft.fft(xw, Nfft)
        w = np.fft.fftfreq(Nfft, 1/fs)
        idx = np.where((w >= 0) & (w <= fs/2))
        return w[idx], np.abs(X[idx])

    w_rect_f, X_rect = calc_fft(x_rect)
    w_ham_f, X_ham = calc_fft(x_ham)
    w_hann_f, X_hann = calc_fft(x_hann)
    w_black_f, X_black = calc_fft(x_black)

    fig, axs = plt.subplots(3, 2, figsize=(14, 10))
    fig.suptitle(
        "Ventaneo: comparación de ventanas\n"
        "x[n] = cos(2π·50·n/fs), fs=1000 Hz, f0=50 Hz",
        fontsize=13, y=0.97
    )
    plt.subplots_adjust(left=0.08, bottom=0.28, hspace=0.35, wspace=0.25)

    # Señal original
    axs[0,0].set_title("Señal original x[n]")
    l_xorig, = axs[0,0].plot(np.arange(L_init), x, 'k', label="x[n]")
    axs[0,0].set_xlabel("n")
    axs[0,0].set_ylabel("Amplitud")
    axs[0,0].grid(True)

    # Ventanas
    axs[0,1].set_title("Ventanas")
    l_rectw, = axs[0,1].plot(np.arange(L_init), w_rect, label="Rectangular")
    l_hamw, = axs[0,1].plot(np.arange(L_init), w_ham, label="Hamming")
    l_hannw, = axs[0,1].plot(np.arange(L_init), w_hann, label="Hann")
    l_blackw, = axs[0,1].plot(np.arange(L_init), w_black, label="Blackman")
    axs[0,1].set_xlabel("n")
    axs[0,1].set_ylabel("Ventana")
    axs[0,1].legend()
    axs[0,1].grid(True)

    # Señal x[n]·ventana rectangular
    axs[1,0].set_title("x[n] · ventana rectangular")
    l_xrect, = axs[1,0].plot(np.arange(L_init), x_rect, label="x[n]·w_rect[n]")
    axs[1,0].set_xlabel("n")
    axs[1,0].set_ylabel("Amplitud")
    axs[1,0].grid(True)

    # Señal x[n]·ventana Hamming
    axs[1,1].set_title("x[n] · ventana Hamming")
    l_xham, = axs[1,1].plot(np.arange(L_init), x_ham, label="x[n]·w_ham[n]")
    axs[1,1].set_xlabel("n")
    axs[1,1].set_ylabel("Amplitud")
    axs[1,1].grid(True)

    # Espectros
    axs[2,0].set_title("Espectro |X_L(ω)| ventanas rect, Hamming, Hann, Blackman")
    l_rect, = axs[2,0].plot(w_rect_f/(fs/2)*np.pi, X_rect, 'r', label="Rectangular")
    l_ham, = axs[2,0].plot(w_ham_f/(fs/2)*np.pi, X_ham, 'b', label="Hamming")
    l_hann, = axs[2,0].plot(w_hann_f/(fs/2)*np.pi, X_hann, 'g', label="Hann")
    l_black, = axs[2,0].plot(w_black_f/(fs/2)*np.pi, X_black, 'm', label="Blackman")
    axs[2,0].set_xlim(0, 0.2*np.pi)
    axs[2,0].set_xlabel("ω/π")
    axs[2,0].set_ylabel("|X_L(ω)|")
    axs[2,0].legend()
    axs[2,0].grid(True)

    # Señal x[n]·ventana Hann y Blackman
    axs[2,1].set_title("x[n] · ventana Hann y Blackman")
    l_xhann, = axs[2,1].plot(np.arange(L_init), x_hann, label="x[n]·w_hann[n]")
    l_xblack, = axs[2,1].plot(np.arange(L_init), x_black, label="x[n]·w_black[n]")
    axs[2,1].set_xlabel("n")
    axs[2,1].set_ylabel("Amplitud")
    axs[2,1].legend()
    axs[2,1].grid(True)

    # Sliders
    axcolor = 'lightgoldenrodyellow'
    ax_L = plt.axes([0.15, 0.18, 0.7, 0.03], facecolor=axcolor)
    s_L = Slider(ax_L, 'L (longitud ventana)', 20, 400, valinit=L_init, valstep=1)

    def update(_):
        L = int(s_L.val)
        x = senal_cos(L, f0, fs)
        w_rect = ventana_rect(L)
        w_ham = ventana_hamming(L)
        w_hann = ventana_hann(L)
        w_black = ventana_blackman(L)
        x_rect = x * w_rect
        x_ham = x * w_ham
        x_hann = x * w_hann
        x_black = x * w_black
        w_rect_f, X_rect = calc_fft(x_rect)
        w_ham_f, X_ham = calc_fft(x_ham)
        w_hann_f, X_hann = calc_fft(x_hann)
        w_black_f, X_black = calc_fft(x_black)
        l_xorig.set_data(np.arange(L), x)
        axs[0,0].set_xlim(0, L)
        l_rectw.set_data(np.arange(L), w_rect)
        l_hamw.set_data(np.arange(L), w_ham)
        l_hannw.set_data(np.arange(L), w_hann)
        l_blackw.set_data(np.arange(L), w_black)
        axs[0,1].set_xlim(0, L)
        l_xrect.set_data(np.arange(L), x_rect)
        axs[1,0].set_xlim(0, L)
        l_xham.set_data(np.arange(L), x_ham)
        axs[1,1].set_xlim(0, L)
        l_xhann.set_data(np.arange(L), x_hann)
        l_xblack.set_data(np.arange(L), x_black)
        axs[2,1].set_xlim(0, L)
        l_rect.set_data(w_rect_f/(fs/2)*np.pi, X_rect)
        l_ham.set_data(w_ham_f/(fs/2)*np.pi, X_ham)
        l_hann.set_data(w_hann_f/(fs/2)*np.pi, X_hann)
        l_black.set_data(w_black_f/(fs/2)*np.pi, X_black)
        fig.canvas.draw_idle()

    s_L.on_changed(update)

    # Botón de reset
    resetax = plt.axes([0.85, 0.05, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    def reset(_):
        s_L.reset()
    button.on_clicked(reset)

    plt.show()

if __name__ == "__main__":
    plot_ventaneo()
