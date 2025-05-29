## Descripción

Este repositorio contiene una colección de Jupyter Notebooks relacionados con el Procesamiento Digital de Señales Biomédicas (Biomedical Digital Signal Processing - DSP). Los notebooks cubren diversos temas fundamentales y avanzados en el análisis y procesamiento de señales en el contexto biomédico.

## Contenido

El repositorio está organizado en torno a una serie de clases o módulos en formato Jupyter Notebook, que se encuentran en el directorio `Clases/`. Los temas cubiertos incluyen:

### Fundamentos de Señales y Sistemas
* Conceptos básicos de señales y sistemas discretos.
* Muestreo, aliasing y reconstrucción de señales (`Muestreo__aliasing_y_reconstrucción__1.3.1__1.4_.ipynb`, `Prefiltros_antialias__1.5.3_.ipynb`, `Reconstrucciones_ideales_y_tipo_escalera__1.6_.ipynb`).
* Cuantización (`Cuantización (2.1).ipynb`).
* Sistemas discretos lineales e invariantes en el tiempo (LTI) (`Sistemas discretos lineales e invariantes en el tiempo (3.2).ipynb`).
* Respuesta al impulso y tipos de sistemas (FIR, IIR) (`Respuesta al impulso (3.3) respuesta al impulso finita e infinita FIR IIR (3.4).ipynb`).
* Convolución (`Convolución (4.1.1) (4.1.3).ipynb`).
* Causalidad y estabilidad (`Causalidad y estabilidad (3.5).ipynb`).

### Análisis en Frecuencia
* Espectro de señales muestreadas y la Transformada de Fourier de Tiempo Discreto (DTFT) (`Espectro_de_señales_muestreadas__DTFT___1.5_.ipynb`, `Recordatorio__DTFT__y_resolución_en_frecuencia_y_ventaneo__9.1_.ipynb`).
* Transformada Discreta de Fourier (DFT) y su inversa (`DFT (10.1) y DFT inversa (10.6).ipynb`).
* Resolución en frecuencia, ventaneo y zero padding (`Resolución en frecuencia y ventaneo (9.1).ipynb`, `Zero padding (10.2) y Resolución fisica Vs. computacional (10.3).ipynb`).
* Densidad Espectral de Potencia (PSD) (`PSD__filtros_de_corrección_de_fase.ipynb`).

### Transformada Z
* Introducción y propiedades de la Transformada Z (`Transformada Z (5.1-5.3).ipynb`).

### Diseño de Filtros Digitales
* **Filtros FIR:**
    * Diseño de filtros FIR por el método de ventanas (`Diseño de filtros FIR por ventanas (11.1).ipynb`).
* **Filtros IIR:**
    * Diseño de filtros IIR pasa-bajas y pasa-altas mediante transformada bilineal (`Diseño_de_filtros_IIR_pasa-bajas_altas__por_transformada_bilineal__12.2_.ipynb`).
    * Diseño de filtros IIR pasa-banda y rechaza-banda mediante transformada bilineal (`Diseño de filtros IIR pasa rechazo banda por ransformada bilineal (12.3).ipynb`).
    * Diseño de filtros IIR de orden superior (`Diseño_filtros_IIR_de_orden_superior__12.6-12.7_.ipynb`).
* Filtros de corrección de fase (`PSD__filtros_de_corrección_de_fase.ipynb`).

### Tópicos Avanzados y Aplicaciones Biomédicas
* Análisis temporal de señales, Transformada de Hilbert y PCA (`Análisis temporal de señales y transformada de Hilbert PCA... y métricas de filtrado.ipynb`).
* Filtros Adaptativos (`Filtros_adaptativos.ipynb`).
* Filtros de Kalman (`Filtros_de_Kalman.ipynb`).
* Transformada Wavelet (`Transformada Wavelet.ipynb`).

## Requisitos Previos

Para ejecutar estos notebooks, necesitarás tener instalado Python y Jupyter Notebook/JupyterLab. Además, las siguientes bibliotecas de Python son comúnmente utilizadas:

* NumPy
* SciPy
* Matplotlib
* Pandas (posiblemente, verificar en los notebooks)
* `scikit-learn` (para PCA, si se usa)
* `pywavelets` (para Transformada Wavelet, si se usa)
* [Menciona cualquier otra biblioteca específica que sea crucial]

Se recomienda crear un entorno virtual para manejar las dependencias:

```bash
python -m venv dsp_env
# En Linux/macOS:
source dsp_env/bin/activate
# En Windows:
# dsp_env\Scripts\activate
pip install jupyter numpy scipy matplotlib pandas scikit-learn pywavelets # [añade otras bibliotecas aquí]
```

## Uso

1.  Clona este repositorio:
    ```bash
    git clone [https://github.com/](https://github.com/)[TU_USUARIO_DE_GITHUB]/Biomedical-DSP.git
    ```
2.  Navega al directorio del repositorio:
    ```bash
    cd Biomedical-DSP
    ```
3.  Activa tu entorno virtual (si creaste uno).
4.  Inicia Jupyter Notebook o JupyterLab:
    ```bash
    jupyter notebook
    # o
    jupyter lab
    ```
5.  Abre los notebooks desde el directorio `Clases/`.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor:
1.  Haz un Fork del repositorio.
2.  Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3.  Realiza tus cambios y haz commit (`git commit -am 'Añade nueva funcionalidad'`).
4.  Haz un Push a la rama (`git push origin feature/nueva-funcionalidad`).
5.  Abre un Pull Request.

## Autor

* [Tu Nombre/Nombre del Grupo]
* [Tu email o link a tu perfil de GitHub/GitLab] (Opcional)

