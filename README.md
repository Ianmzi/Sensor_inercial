# Sensor_inercial

Reconocimiento de Actividades de la Vida Diaria mediante sensores inerciales y Machine Learning
Este repositorio contiene el código principal en MATLAB para obtener las características de datos de sensores inerciales (IMU) adquiridos de 5 sujetos que realizaron actividades de subir escaleras, bajar escaleras y descanso.

El script realiza:
1. La lectura recursiva de datos .txt en la estructura de carpetas mediciones/sujeto_*/clase/.
2. Extracción de características: calcula metricas temporales (media, desviación estándar, skewness, kurtosis, etc.) y frecuenciales (energía, frecuencia dominante, etc.).
3. Normalización: estandarización de características usando Z-Score.
4. Filtro de características: se seleccionan las características principales con el método Correlación de Pearson Absoluta con la etiqueta de clase.

Requisitos:
- Instalación actualizada de MATLAB que permita la compatibilidad.
- Los archivos son en formato .txt y deben ser delimitados por un separador ; (punto y coma), con encabezados para las columnas de los sensores ( ax, ay, az, wx, wy, wz, Angle, etc.).

Guía de uso:
1. Clonar el repositorio 'git clone https://github.com/tu-usuario/tu-proyecto.git cd tu-proyecto'
2. Ejecución del script: aparecerá una ventana para seleccionar la carpeta base que contiene todos los datos de los sujetos.

Salidas generadas
El script generará dos archivos .csv de la salida en la carpeta base: el primer archivo contiene todas las características extraídas y normalizadas para todos los sujetos y ventanas, el segundo la tabla maestra que incluye solo las características mejor rankeadas por correlación.

Configuración del procesamiento
Las variables de configuración deben ser ajustadas al inicio del script.

## 🧭 MODO A: Carga y proceso de archivo  

Este proyecto es una aplicación de **Interfaz Gráfica de Usuario (GUI)** desarrollada en **MATLAB App Designer (.mlapp)**.  
Su objetivo principal es **cargar las mediciones de un sensor IMU (Unidad de Medición Inercial)**, procesar las señales para extraer características relevantes y, finalmente, **utilizar un modelo de Machine Learning preentrenado** para clasificar la actividad registrada: **ascenso, descenso de escaleras o estado de reposo**.

---

### ⚙️ Prerrequisitos
- **MATLAB R2025a** o posterior.  
- **Statistics and Machine Learning Toolbox:** para cargar y ejecutar modelos de ML preentrenados.  
- **Signal Processing Toolbox:** para el preprocesamiento y extracción de características.  
- **`ModeloFinal_ArbolDecision.mat`:** modelo de árbol de decisión preentrenado (debe estar en la misma carpeta que la app).  

---

### 🧩 Funcionalidades

#### 1️⃣ Importación de datos
Carga un archivo `.csv` que contiene mediciones registradas por el sensor inercial.  
Estas mediciones incluyen tres canales principales: **acelerómetro, giroscopio y ángulo**.

#### 2️⃣ Preprocesamiento
Se aplica un **filtro digital Butterworth** para eliminar el ruido de alta frecuencia y mejorar la calidad de la señal.

#### 3️⃣ Segmentación de ventanas
La señal se divide en **ventanas de 2 segundos** con un **50 % de solapamiento**, generando una **matriz de características** donde cada fila corresponde a una ventana.

#### 4️⃣ Extracción de características
De cada ventana segmentada se calculan **10 atributos por canal**, obteniendo un total de:  
> 🔹 3 canales × 10 atributos × 3 señales = **90 características extraídas**

##### 📊 Atributos temporales
| Atributo                         | Descripción                                                             |
| -------------------------------- | ----------------------------------------------------------------------- |
| **media (`mean`)**               | Promedio de los valores del canal. Indica tendencia central.            |
| **desviación estándar (`stdv`)** | Mide la variabilidad de la señal.                                       |
| **RMS (`rmsv`)**                 | Raíz cuadrática media, refleja la energía promedio.                     |
| **máximo (`maxv`)**              | Valor pico dentro de la ventana.                                        |
| **mínimo (`minv`)**              | Valor más bajo dentro de la ventana.                                    |
| **asimetría (`skew`)**           | Mide la simetría de la distribución respecto a la media. |
| **curtosis (`kurt`)**            | Indica cuán “afilada” o concentrada está la distribución.               |

##### ⚡ Atributos frecuenciales
| Atributo                           | Descripción                                                                          |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| **energía (`energia`)**            | Suma del cuadrado de las magnitudes espectrales, mide la potencia total de la señal. |
| **frecuencia dominante (`f_dom`)** | Frecuencia donde el espectro tiene su máximo pico.                                   |
| **frecuencia media (`f_media`)**   | Promedio ponderado de las frecuencias según su potencia.                             |

#### 5️⃣ Selección automática de características
Se aplica una **poda por correlación** que reduce la dimensionalidad seleccionando las **10 características más relevantes** de las **90 originales**.

#### 6️⃣ Clasificación
El modelo **Árbol de Decisión** (`ModeloFinal_ArbolDecision.mat`) predice la clase de actividad:  
> **Subir escaleras**, **Bajar escaleras** o **Reposo**.  

Además, la app genera una **matriz de confusión** que permite visualizar el rendimiento del modelo comparando las predicciones con las etiquetas reales del usuario.


📁 **Estructura de salida esperada:**



