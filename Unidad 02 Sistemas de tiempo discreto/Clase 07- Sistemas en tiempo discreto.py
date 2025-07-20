import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def sistema_lineal(x, a=2, b=3, c=4):
    # y(n) = a*x(n) + b*x(n-1) + c*x(n-2)
    y = np.zeros_like(x)
    for n in range(len(x)):
        y[n] = a*x[n]
        if n-1 >= 0:
            y[n] += b*x[n-1]
        if n-2 >= 0:
            y[n] += c*x[n-2]
    return y

def sistema_escalamiento(x, k=2):
    # y(n) = k*x(n)
    return k*x

def plot_sistemas_lineales():
    N = 20
    n = np.arange(N)
    # Señal de entrada: impulso unitario desplazado
    x = np.zeros(N)
    x[2] = 1
    x[5] = 0.5
    x[10] = 1

    # Parámetros iniciales
    a_init, b_init, c_init = 2, 3, 4
    k_init = 2

    fig, axs = plt.subplots(2, 1, figsize=(10, 7))
    plt.subplots_adjust(left=0.1, bottom=0.25, hspace=0.4)

    # Sistema lineal: suma ponderada de muestras
    y = sistema_lineal(x, a_init, b_init, c_init)
    axs[0].set_title("Sistema lineal: $y(n) = a x(n) + b x(n-1) + c x(n-2)$")
    l_x0 = axs[0].stem(n, x, linefmt='C0-', markerfmt='C0o', basefmt=" ", label="Entrada $x(n)$")
    stem_y0 = axs[0].stem(n, y, linefmt='C1-', markerfmt='C1s', basefmt=" ", label="Salida $y(n)$")
    axs[0].legend()
    axs[0].set_xlabel("n")
    axs[0].set_ylabel("Amplitud")
    axs[0].grid(True)

    # Sistema de escalamiento
    y2 = sistema_escalamiento(x, k_init)
    axs[1].set_title("Sistema de escalamiento: $y(n) = k x(n)$")
    l_x1 = axs[1].stem(n, x, linefmt='C0-', markerfmt='C0o', basefmt=" ", label="Entrada $x(n)$")
    stem_y1 = axs[1].stem(n, y2, linefmt='C2-', markerfmt='C2s', basefmt=" ", label="Salida $y(n)$")
    axs[1].legend()
    axs[1].set_xlabel("n")
    axs[1].set_ylabel("Amplitud")
    axs[1].grid(True)

    # Sliders
    axcolor = 'lightgoldenrodyellow'
    ax_a = plt.axes([0.15, 0.18, 0.2, 0.03], facecolor=axcolor)
    ax_b = plt.axes([0.40, 0.18, 0.2, 0.03], facecolor=axcolor)
    ax_c = plt.axes([0.65, 0.18, 0.2, 0.03], facecolor=axcolor)
    ax_k = plt.axes([0.15, 0.13, 0.7, 0.03], facecolor=axcolor)
    s_a = Slider(ax_a, 'a', 0, 5, valinit=a_init)
    s_b = Slider(ax_b, 'b', 0, 5, valinit=b_init)
    s_c = Slider(ax_c, 'c', 0, 5, valinit=c_init)
    s_k = Slider(ax_k, 'k', 0, 5, valinit=k_init)

    # Guardar referencias a los stems de salida para actualizar
    stems_out = [stem_y0, stem_y1]

    def update(_):
        a = s_a.val
        b = s_b.val
        c = s_c.val
        k = s_k.val
        y = sistema_lineal(x, a, b, c)
        y2 = sistema_escalamiento(x, k)
        # Eliminar stems de salida anteriores
        for stem in stems_out:
            for artist in stem:
                try:
                    artist.remove()
                except Exception:
                    pass
        # Dibujar nuevos stems de salida y actualizar referencias
        new_stem_y0 = axs[0].stem(n, y, linefmt='C1-', markerfmt='C1s', basefmt=" ")
        new_stem_y1 = axs[1].stem(n, y2, linefmt='C2-', markerfmt='C2s', basefmt=" ")
        stems_out[0] = new_stem_y0
        stems_out[1] = new_stem_y1
        fig.canvas.draw_idle()

    s_a.on_changed(update)
    s_b.on_changed(update)
    s_c.on_changed(update)
    s_k.on_changed(update)

    # Botón de reset
    resetax = plt.axes([0.85, 0.05, 0.1, 0.04])
    button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
    def reset(_):
        s_a.reset()
        s_b.reset()
        s_c.reset()
        s_k.reset()
    button.on_clicked(reset)

    plt.show()

if __name__ == "__main__":
    plot_sistemas_lineales()
