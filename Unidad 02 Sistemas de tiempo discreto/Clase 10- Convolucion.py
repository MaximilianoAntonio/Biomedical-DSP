import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def convolucion_directa(x, h):
    L = len(x)
    M = len(h) - 1
    y = np.zeros(L + M)
    for n in range(L + M):
        m_min = max(0, n - L + 1)
        m_max = min(n, M)
        for m in range(m_min, m_max + 1):
            y[n] += h[m] * x[n - m]
    return y

def convolucion_circular(x, h):
    N = max(len(x), len(h))
    x_pad = np.pad(x, (0, N - len(x)), mode='constant')
    h_pad = np.pad(h, (0, N - len(h)), mode='constant')
    y = np.zeros(N)
    for n in range(N):
        for m in range(N):
            y[n] += x_pad[m] * h_pad[(n - m) % N]
    return y

def plot_convolucion():
    # Señales de ejemplo
    x = np.array([1, 2, 3, 4, 5])
    h = np.array([1, -1, 2, 0])
    y_dir = convolucion_directa(x, h)
    y_circ = convolucion_circular(x, h)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    plt.subplots_adjust(left=0.1, bottom=0.25, hspace=0.4, wspace=0.3)
    fig.suptitle(
        "Convolución discreta: directa y circular\n"
        "x = [1, 2, 3, 4, 5], h = [1, -1, 2, 0]",
        fontsize=13, y=0.96
    )

    # Señal x[n]
    axs[0,0].set_title("Señal x[n]")
    axs[0,0].stem(np.arange(len(x)), x, linefmt='C0-', markerfmt='C0o', basefmt=" ")
    axs[0,0].set_xlabel("n")
    axs[0,0].set_ylabel("x[n]")
    axs[0,0].grid(True)

    # Señal h[n]
    axs[0,1].set_title("Señal h[n]")
    axs[0,1].stem(np.arange(len(h)), h, linefmt='C1-', markerfmt='C1s', basefmt=" ")
    axs[0,1].set_xlabel("n")
    axs[0,1].set_ylabel("h[n]")
    axs[0,1].grid(True)

    # Convolución directa
    axs[1,0].set_title("Convolución directa: y[n] = x[n]*h[n] (longitud L+M)")
    axs[1,0].stem(np.arange(len(y_dir)), y_dir, linefmt='C2-', markerfmt='C2^', basefmt=" ")
    axs[1,0].set_xlabel("n")
    axs[1,0].set_ylabel("y[n]")
    axs[1,0].grid(True)

    # Convolución circular
    axs[1,1].set_title("Convolución circular: y_circ[n] (longitud N = max(len(x), len(h)))")
    axs[1,1].stem(np.arange(len(y_circ)), y_circ, linefmt='C3-', markerfmt='C3^', basefmt=" ")
    axs[1,1].set_xlabel("n")
    axs[1,1].set_ylabel("y_circ[n]")
    axs[1,1].grid(True)

    # Sliders para modificar x y h
    axcolor = 'lightgoldenrodyellow'
    ax_x2 = plt.axes([0.15, 0.15, 0.7, 0.03], facecolor=axcolor)
    ax_h1 = plt.axes([0.15, 0.1, 0.7, 0.03], facecolor=axcolor)
    s_x2 = Slider(ax_x2, 'x[2]', 0, 5, valinit=x[2])
    s_h1 = Slider(ax_h1, 'h[1]', -2, 2, valinit=h[1])

    def update(_):
        x[2] = s_x2.val
        h[1] = s_h1.val
        y_dir = convolucion_directa(x, h)
        y_circ = convolucion_circular(x, h)
        # Limpiar cada eje antes de graficar
        for ax in axs.flat:
            ax.cla()
        # x[n]
        axs[0,0].set_title("Señal x[n]")
        axs[0,0].stem(np.arange(len(x)), x, linefmt='C0-', markerfmt='C0o', basefmt=" ")
        axs[0,0].set_xlabel("n")
        axs[0,0].set_ylabel("x[n]")
        axs[0,0].grid(True)
        # h[n]
        axs[0,1].set_title("Señal h[n]")
        axs[0,1].stem(np.arange(len(h)), h, linefmt='C1-', markerfmt='C1s', basefmt=" ")
        axs[0,1].set_xlabel("n")
        axs[0,1].set_ylabel("h[n]")
        axs[0,1].grid(True)
        # y[n] directa
        axs[1,0].set_title("Convolución directa: y[n] = x[n]*h[n] (longitud L+M)")
        axs[1,0].stem(np.arange(len(y_dir)), y_dir, linefmt='C2-', markerfmt='C2^', basefmt=" ")
        axs[1,0].set_xlabel("n")
        axs[1,0].set_ylabel("y[n]")
        axs[1,0].grid(True)
        # y_circ[n] circular
        axs[1,1].set_title("Convolución circular: y_circ[n] (longitud N = max(len(x), len(h)))")
        axs[1,1].stem(np.arange(len(y_circ)), y_circ, linefmt='C3-', markerfmt='C3^', basefmt=" ")
        axs[1,1].set_xlabel("n")
        axs[1,1].set_ylabel("y_circ[n]")
        axs[1,1].grid(True)
        fig.canvas.draw_idle()

    s_x2.on_changed(update)
    s_h1.on_changed(update)

    # Botón de reset
    resetax = plt.axes([0.85, 0.05, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    def reset(_):
        s_x2.reset()
        s_h1.reset()
    button.on_clicked(reset)

    plt.show()

if __name__ == "__main__":
    plot_convolucion()
