<details>

<summary> Primer lab </summary>

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


# [Control proporcional para el seguimiento de línea](./paroporcional.py)

Para que un robot sea capaz de seguir una línea de forma autónoma, no basta con detectar la posición de esa línea en la imagen: también necesita una forma de corregir su movimiento de manera continua y suave.
Aquí es donde entra en juego el control proporcional (P-control), una técnica sencilla pero muy efectiva en robótica móvil.

El objetivo del control proporcional es ajustar el giro del robot en función del error visual, es decir, la distancia entre la posición de la línea y el centro de la imagen.
Cuanto más desviada esté la línea, mayor será la corrección; y cuanto más centrada esté, más suave será el movimiento.

Con este método, el robot:

- gira más fuerte cuando la línea está lejos del centro,

- gira suavemente cuando la línea está cerca,

- avanza recto cuando la línea está alineada.

Este comportamiento hace posible que el robot siga el recorrido de forma estable, reactiva y continua, adaptándose en tiempo real a curvas, cambios de dirección y pequeñas imperfecciones



Dentro del código del controlador proporcional, tenemos la variable KP,V_MAX y V_MIN a destacar

- **KP**: constante proporcional que define cuánto gira el robot por cada pixel de error.
- **V_MAX / V_MIN**: límites de la velocidad lineal.
- **w_dyn** = KP * err(Si el error es grande giro grande, si no suave, y si es 0 sigue recto)
- **v_dyn** = V_MAX - ((abs(err) / IMG_CENTER) * (V_MAX - V_MIN)) (Cuanto mayor sea el error menor será la velocidad)
del circuito.
- **err**: cuánto se desvía la línea del centro de la imagen,y hacia qué lado.



# [Control PD](./PD.py)

Este programa es una evolución del control proporcional. Además de la corrección proporcional al error (KP * error), incorpora un término derivativo (KD) que permite que el robot anticipe cambios en la línea y reaccione de forma más suave en curvas o giros rápidos.

A parte de las variables previas, destacan:

- **KD**: ganancia derivativa, ajusta la reacción del robot ante cambios rápidos del error.
- **last_err**: almacena el error de la iteración anterior para calcular el término derivativo.
- **derivative** = err - last_err:
- - Se calcula cómo ha cambiado el error respecto a la iteración anterior.
- - Este valor anticipa la tendencia del error: si el error aumenta rápido, el robot necesita girar más agresivamente; si disminuye, gira menos.


- **w_dyn** = KP * err + KD * derivative

- - KP * err: corrección proporcional (como antes).

- - KD * derivative: corrección derivativa, que suaviza la respuesta y reduce oscilaciones.

- - Combinando ambos, el robot gira de manera más estable y rápida ante curvas o cambios bruscos de la línea.




# [Control PID](./PID.py)

Este programa es la versión más avanzada de los anteriores. Incorpora un control PID, que combina tres términos, los dos anteriores y el Integral:

Integral (I): corrige errores acumulados a lo largo del tiempo (ayuda en situaciones donde la línea tiende a desviarse ligeramente de manera constante).

Respecto a las variables:
  -**KI**: ganancia integral, corrige desviaciones acumuladas.
  -**integral**: acumula el error a lo largo del tiempo para el término integral.
  - **integral += err** : Suma acumulativa del error, corrige errores persistenes que el término proporcional por sí solo no puede
  - **w_dyn** = KP * err + KD * derivative + KI * integral
  -  - **KI * integral**: corrige desvíos sostenidos a largo plazo.




# Despegar Proyecto

### 1. Descargar la imagen

Primero, obtén la última imagen de Docker Hub:

> ```bash
> docker pull jderobot/robotics-backend:latest 
> ```

### 2. Lanzar el contenedor

Lanzar el contenedor

Opción A: Sin aceleración gráfica

Esta es la opción recomendada si no necesitas aceleración gráfica o no estás seguro
> ```bash
>docker run --rm -it \-p 6080-6090:6080-6090 -p 7163:7163 \jderobot/robotics-backend:latest 
> ```

Opción B: Con aceleración gráfica (genérica)

Usa esta opción si tienes drivers gráficos (como Intel o AMD) y quieres habilitar la aceleración.

> ```bash
> docker run --rm -it --device /dev/dri \-p 6080-6090:6080-6090 -p 7163:7163 \jderobot/robotics-backend:latest 
> ```

Opción C: Con aceleración gráfica (NVIDIA)
Usa esta opción específica si tienes una tarjeta gráfica NVIDIA y los drivers correspondientes instalados.
> ```bash
> docker run --rm -it --device /dev/dri --gpus all \-p 6080-6090:6080-6090 -p 7163:7163 \jderobot/robotics-backend:latest 
> ```


Una vez arrancado el contenedor, inicias sesión o te registras en unibotics, accedes a follow line, y eliges el universo correspondiente, en nuestro caso, el simple

</details>



<details>


  <summary>  Segundo lab</summary>
  
  # Rescue People Challenge - Unibotics

  
  <img width="500" height="200" alt="imagen" src="https://github.com/user-attachments/assets/ea65f01b-f0d2-4498-a5e3-6872fb740db0" />

![Python](https://img.shields.io/badge/Python-3.8-blue)
![Unibotics](https://img.shields.io/badge/Platform-Unibotics-green)
![OpenCV](https://img.shields.io/badge/Library-OpenCV-red)

## Descripción
Este proyecto contiene la solución para el reto **"Rescue People"** de la plataforma Unibotics. El objetivo es programar un dron autónomo capaz de patrullar una zona de marítima, localizar a las víctimas mediante visión artificial y reportar su ubicación antes de regresar a la base.

La solución implementa una estrategia de búsqueda en espiral y un sistema de visión robusto ante la rotación de la cámara.

## 🎯 Objetivos del Reto
1. **Despegue y Posicionamiento:** Elevar el dron y dirigirse al centro de la zona de búsqueda.
2. **Patrullaje Autónomo:** Barrer el área de forma eficiente para no dejar zonas sin revisar.
3. **Detección de Víctimas:** Identificar rostros humanos en el agua usando la cámara ventral.
4. **Geolocalización:** Guardar las coordenadas de cada víctima (evitando duplicados).
5. **Retorno a Casa:** Volver al punto de despegue (0,0) y aterrizar tras completar la misión.

## ⚙️ Estrategia de Solución

### 1. Máquina de Estados (FSM)
El comportamiento del dron se gestiona mediante una máquina de estados finitos para asegurar un flujo lógico:

| Estado | Descripción |
| :--- | :--- |
| `TAKEOFF` | El dron despega hasta alcanzar una altura de seguridad (4m). |
| `MOVE_TO_CENTER` | Desplazamiento rápido hacia el centro del área de búsqueda. |
| `SEARCH` | Ejecución del algoritmo de espiral y detección activa de visión. |
| `RETURN_HOME` | Al encontrar todas las víctimas, el dron regresa al origen. |
| `LAND` | Aterrizaje controlado y reporte final. |




### 2. Implementación Técnica y Algoritmos

  #### Navegación: Espiral 
  Para garantizar un barrido completo del océano sin repetir zonas, implementé una espiral matemática. En lugar de usar `waypoints` fijos, calculo la posición objetivo en tiempo real basándome en el ángulo acumulado.
  
  Esto convierte coordenadas polares (ángulo y radio creciente) a cartesianas (X, Y) para el dron:

  > ```python
  > # El radio crece conforme el dron da vueltas (Espiral de Arquímedes)
  > radius_current = SPIRAL_INCREMENT * angle_accumulated
  > """ Conversión Polar -> Cartesiana"""
  > target_x = TARGET_X + radius_current * math.cos(angle_accumulated)
  > target_y = TARGET_Y + radius_current * math.sin(angle_accumulated)  





Uno de los mayores desafíos técnicos es que el clasificador Haar Cascade solo detecta rostros en posición vertical. Dado que el dron rota sobre su eje Z mientras se desplaza, la orientación de la víctima cambia constantemente en la cámara.

Solución: Implementé una función que rota la imagen capturada en memoria 360º (en pasos de 15º) hasta encontrar una coincidencia.

> ``` python
> # Bucle de detección con rotación dinámica
> for rotation in range(0, 360, 15):
>    # Si es 0 grados usa la original, si no, rota la imagen
>    check_frame = gray_frame if rotation == 0 else rotate_gray(gray_frame, rotation)
>    
>    # Intenta detectar caras en la imagen rotada
>    faces_found = face_detector.detectMultiScale(check_frame, scaleFactor=1.2, minNeighbors=3)
>   
>    if len(faces_found) > 0:
>        detected_face = True
>       break # Si encuentra cara, deja de rotar para ahorrar CPU


Para evitar contar a la misma víctima múltiples veces mientras el drone pasa sobre ella, se calcula la distancia euclidiana. Solo se registra una nueva víctima si está a más de 2 metros de cualquier ubicación ya guardada
> ``` python
>is_new_victim = all(math.hypot(x_pos - vx, y_pos - vy) >= 4.0 for vx, vy in victims_locations)



### Resultado
Como se puede ver en la imagen, el dron ha aterrizado despues de haber detectado a las victimas, que en este caso han sido 6
<img width="850" height="500" alt="lab2ro" src="https://github.com/user-attachments/assets/6213e5b2-1531-454c-9bd3-a01fd9cf11ef" />





# Despegar Proyecto

### 1. Descargar la imagen

Primero, obtén la última imagen de Docker Hub:

> ```bash
> docker pull jderobot/robotics-backend:latest 
> ```

### 2. Lanzar el contenedor

Lanzar el contenedor

Opción A: Sin aceleración gráfica

Esta es la opción recomendada si no necesitas aceleración gráfica o no estás seguro
> ```bash
>docker run --rm -it \-p 6080-6090:6080-6090 -p 7163:7163 \jderobot/robotics-backend:latest 
> ```

Opción B: Con aceleración gráfica (genérica)

Usa esta opción si tienes drivers gráficos (como Intel o AMD) y quieres habilitar la aceleración.

> ```bash
> docker run --rm -it --device /dev/dri \-p 6080-6090:6080-6090 -p 7163:7163 \jderobot/robotics-backend:latest 
> ```

Opción C: Con aceleración gráfica (NVIDIA)
Usa esta opción específica si tienes una tarjeta gráfica NVIDIA y los drivers correspondientes instalados.
> ```bash
> docker run --rm -it --device /dev/dri --gpus all \-p 6080-6090:6080-6090 -p 7163:7163 \jderobot/robotics-backend:latest 
> ```


Una vez arrancado el contenedor, inicias sesión o te registras en unibotics, accedes a follow line, y eliges el universo correspondiente, en nuestro caso, el simple

## ✍️ Autor
* **Jose Cristian Georgescu** - *Trabajo Inicial* - [josecristian](https://github.com/jose2003cg)


</details>




