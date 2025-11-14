# JCGT-SJK001
This repo will contain all the code and info related to the laboratory fort the subject SJK001

# ¿Qué es follow line en robótica?

Follow line es una técnica en la que un robot es capaz de detectar una línea en el suelo y seguirla automáticamente mientras se mueve. Esa línea suele tener un color o contraste diferente del resto del entorno, en este caso una linea roja.



### **¿Qué hace un robot que sigue una línea?**

- Ve la línea con su cámara o sensores

- Calcula dónde está la línea dentro de la imagen

- Corrige su movimiento

- Se mueve continuamente siguiendo el camino marcado por esa línea

Para comprender cómo funciona el robot en la práctica, es importante observar tanto el circuito físico como la visión que obtiene la cámara del robot. A continuación se muestran dos imágenes:

El circuito real, donde se aprecia el trazado que el robot debe seguir.

La vista del entorno desde la cámara del robot, que muestra cómo la línea es percibida por el sistema de visión que utiliza el método follow line.

<img width="385" height="379" alt="imagen" src="https://github.com/user-attachments/assets/9e105370-c024-4641-b63f-d91446db78d5" />

<img width="378" height="382" alt="imagen" src="https://github.com/user-attachments/assets/367e7856-0e97-4ae2-9626-b90713ea99c8" />


# Control proporcional para el seguimiento de línea

Para que un robot sea capaz de seguir una línea de forma autónoma, no basta con detectar la posición de esa línea en la imagen: también necesita una forma de corregir su movimiento de manera continua y suave.
Aquí es donde entra en juego el control proporcional (P-control), una técnica sencilla pero muy efectiva en robótica móvil.

El objetivo del control proporcional es ajustar el giro del robot en función del error visual, es decir, la distancia entre la posición de la línea y el centro de la imagen.
Cuanto más desviada esté la línea, mayor será la corrección; y cuanto más centrada esté, más suave será el movimiento.

Con este método, el robot:

- gira más fuerte cuando la línea está lejos del centro,

- gira suavemente cuando la línea está cerca,

 -avanza recto cuando la línea está alineada.

Este comportamiento hace posible que el robot siga el recorrido de forma estable, reactiva y continua, adaptándose en tiempo real a curvas, cambios de dirección y pequeñas imperfecciones



Dentro del código del controlador proporcional, tenemos la variable KP,V_MAX y V_MIN a destacar

- KP: constante proporcional que define cuánto gira el robot por cada pixel de error.
- V_MAX / V_MIN: límites de la velocidad lineal.
- w_dyn = KP * err(Si el error es grande giro grande, si no suave, y si es 0 sigue recto)
- v_dyn = V_MAX - ((abs(err) / IMG_CENTER) * (V_MAX - V_MIN)) (Cuanto mayor sea el error menor será la velocidad)
del circuito.


