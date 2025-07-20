import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve, freqz
from scipy.fft import fft, fftfreq, fftshift
from matplotlib.widgets import Slider, Button

# Señal de prueba: suma de dos senoidales
def generar_senal(t, A1, f1, A2, f2):
    return A1 * np.cos(2 * np.pi * f1 * t) + A2 * np.cos(2 * np.pi * f2 * t)

# Filtro pasa bajas simple (respuesta al impulso)
def filtro_pasabajas(fc, fs, N=101):
    t = np.arange(-N//2, N//2+1)
    h = 2 * fc / fs * np.sinc(2 * fc * t / fs)
    window = np.hamming(N+1)
    return h * window

# Visualización interactiva
def ejercicio_filtrado():
    fs = 1000  # Hz
    t = np.linspace(0, 1, fs, endpoint=False)
    f1_init, f2_init = 50, 200
    A1_init, A2_init = 1, 0.5
    fc_init = 100

    fig, axs = plt.subplots(3, 2, figsize=(10, 8))
    plt.subplots_adjust(left=0.1, bottom=0.35, hspace=0.5)  # aumenta separación vertical

    # Señal original
    x = generar_senal(t, A1_init, f1_init, A2_init, f2_init)
    axs[0,0].set_title("Señal original x(t)")
    l_x, = axs[0,0].plot(t, x)
    axs[0,0].set_xlim(0, 0.1)

    # Espectro de la señal original
    X = fft(x)
    f = fftfreq(len(x), 1/fs)
    axs[0,1].set_title("Espectro |X(f)|")
    l_X, = axs[0,1].plot(fftshift(f), fftshift(np.abs(X)))
    axs[0,1].set_xlim(0, 500)

    # Respuesta al impulso del filtro
    h = filtro_pasabajas(fc_init, fs)
    t_h = np.arange(len(h)) / fs  
    axs[1,0].set_title("Filtro h(t)")
    l_h, = axs[1,0].plot(t_h, h)

    # Espectro del filtro
    w, H = freqz(h, worN=fs, fs=fs)
    axs[1,1].set_title("Respuesta en frecuencia |H(f)|")
    l_H, = axs[1,1].plot(w, np.abs(H))
    axs[1,1].set_xlim(0, 500)

    # Señal filtrada
    y = convolve(x, h, mode='same')
    axs[2,0].set_title("Señal filtrada y(t)")
    l_y, = axs[2,0].plot(t, y)
    axs[2,0].set_xlim(0, 0.1)

    # Espectro de la señal filtrada
    Y = fft(y)
    l_Y, = axs[2,1].plot(fftshift(f), fftshift(np.abs(Y)))
    axs[2,1].set_title("Espectro |Y(f)|")
    axs[2,1].set_xlim(0, 500)

    # Sliders
    axcolor = 'lightgoldenrodyellow'
    ax_A1 = plt.axes([0.1, 0.25, 0.3, 0.03], facecolor=axcolor)
    ax_A2 = plt.axes([0.1, 0.2, 0.3, 0.03], facecolor=axcolor)
    ax_f1 = plt.axes([0.6, 0.25, 0.3, 0.03], facecolor=axcolor)
    ax_f2 = plt.axes([0.6, 0.2, 0.3, 0.03], facecolor=axcolor)
    ax_fc = plt.axes([0.35, 0.15, 0.3, 0.03], facecolor=axcolor)

    s_A1 = Slider(ax_A1, 'A1', 0, 2, valinit=A1_init)
    s_A2 = Slider(ax_A2, 'A2', 0, 2, valinit=A2_init)
    s_f1 = Slider(ax_f1, 'f1 [Hz]', 10, 400, valinit=f1_init)
    s_f2 = Slider(ax_f2, 'f2 [Hz]', 10, 400, valinit=f2_init)
    s_fc = Slider(ax_fc, 'fc [Hz]', 10, 400, valinit=fc_init)

    def update(_):
        A1 = s_A1.val
        A2 = s_A2.val
        f1 = s_f1.val
        f2 = s_f2.val
        fc = s_fc.val

        x = generar_senal(t, A1, f1, A2, f2)
        l_x.set_ydata(x)
        X = fft(x)
        l_X.set_ydata(fftshift(np.abs(X)))

        h = filtro_pasabajas(fc, fs)
        l_h.set_ydata(h)
        w, H = freqz(h, worN=fs, fs=fs)
        l_H.set_data(w, np.abs(H))

        y = convolve(x, h, mode='same')
        l_y.set_ydata(y)
        Y = fft(y)
        l_Y.set_ydata(fftshift(np.abs(Y)))

        fig.canvas.draw_idle()

    s_A1.on_changed(update)
    s_A2.on_changed(update)
    s_f1.on_changed(update)
    s_f2.on_changed(update)
    s_fc.on_changed(update)

    # Botón de reset
    resetax = plt.axes([0.8, 0.05, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    def reset(_):
        s_A1.reset()
        s_A2.reset()
        s_f1.reset()
        s_f2.reset()
        s_fc.reset()
    button.on_clicked(reset)

    plt.show()

if __name__ == "__main__":
    ejercicio_filtrado()
