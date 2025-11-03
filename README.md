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
