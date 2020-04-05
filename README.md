# FrenaLaCurva con DeepLearning
## Victor Rodríguez & Pablo Saucedo

![logo](https://github.com/p-saucedo/FrenaLaCurva/blob/master/logo.jpg)

### Propósito del proyecto
FrenaLaCurva es un proyecto desarrollado por Victor Rodríguez y Pablo Saucedo. Ambos estamos actualmente becados con el programa Talentum de Teléfonica y somos orgullosos miembros del equipo de Ideas Locas, un equipo multidisciplinar que se basa en dos pilares de investigación: ciberseguridad e inteligencia artificial. 

Debido a la grave pandemia en la que nos vemos inmersos de manera global, la Comunidad de Madrid ha organizado un hackaton llamado [VenceAlVirus](https://vencealvirus.org/) los días 4 y 5 de abril de 2020 con el objetivo de buscar soluciones a todos los problemas que se están planteado por la crisis del CoVid-19. FrenaLaCurva es nuestra aportación y también se puede encontrar en [Taiga](https://taiga.vencealvirus.software.imdea.org/project/psaucedo-frenalacurva-con-deeplearning/timeline).

El objetivo primordial es adelantarse a la propagación del virus, conocer cómo se comporta y cómo puede afectar a nuestra sociedad. Por eso es por lo que los estudios sobre la curva de contagios son tan importantes, ya que conseguir una predicción precisa puede evitar multitud de problemas futuros. Esta curva depende de multitud de parámetros, muchos de ellos de índole biológica o sanitaria con los cuáles nos es complicado tratar; pero en la búsqueda de datos que puedan influir en la predicción, nos hemos topado con la **temperatura**.

### Hipótesis inicial
El análisis de los mayores focos de contagio (Europa, Hubei, EEUU), todos situados en una latitud similar, y los pocos datos de contagios en latitudes más cálidas, refleja que las temperatura frías ayuden a la propagación del virus y, por el contrario, el calor provoca que el virus se debilite o muera. 

Además, vamos a utilizar los datos de China y Corea, que ya han conseguido estabilizar la curva, para entrenar nuestro modelo y que nuestra predicción imite sus curvas, ya que todas las curvas de contagio tienen una forma muy similar pero a diferentes escalas, ya que la diferencia de población es abismal.

### FrenaLaCurva
Nuestro proyecto tiene la función de predecir el número de contagiados por cada Comunidad Autónoma de España, atendiendo a su predicción de temperaturas para la próxima semana. Hemos hecho uso de Flask para permitir la interacción con el usuario, múltiples APIs para la recogida de datos, que se detallan más adelante, el servicio de Google Maps para la visualización del mapa y, por último, el *DeepLearning* para el tratamiento de los datos y la predicción.


### Recogida de datos
La recogida de datos es una labor fundamental en este proyecto. Los datos de temperatura mundial y de infectados no se recogen de manera dinámica, ya que no existe API gratuita que realice dicha labor. Por otro lado, el pronóstico se realiza a través de la API weatherbit.io al hacer click en el mapa.

##### Fuentes:
* Spain infected data: (https://github.com/datadista/datasets/tree/master/COVID%2019)
* World Infected data: (https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases)
* Spain weather data: (https://www.weatherbit.io/api)
* World weather data: (https://www.ncdc.noaa.gov/)

### Motor de *DeepLearning*
El motor de *DeepLearning* que hemos desarrollado se compone de dos ramas, una destinada al tratamiento de la temperatura y otra para los datos históricos de contagiados. Cada una de las dos ramas tiene una arquitectura similar, compuesta básicamente por una *LSTM* acompañada de una capa de *Dropout* que evita el overfitting y seguidas de capas *Dense*. Por último, ambas ramas se concatenan para finalmente dar una salida linear.

El proceso que vamos a llevar a cabo con el modelo es un entrenamiento con los datos de China y Corea, con el objetivo de que la red neuronal sea capaz de aprender la forma general de la curva de contagios de estos paises, para continuar con un segundo entrenamiento con los datos de contagiados de la Comunidad Autónoma a consultar, por lo que se verá obligada a aplicar el patrón antes aprendido a los nuevos datos que se introducen. El proceso de predicción es secuencial, se toma como origen el último dato de entrenamiento y se generan tantos datos nuevos de contagios como se soliciten, dadas unas temperaturas previamente consultadas.

La complejidad en este modelo reside en que la curva es una función no estacionaria, por lo que va a ser necesario evitar completamente el *overfitting* para conseguir que no tienda hacia los datos ya conocidos lo que le hara incapaz de particularizar para cada caso concreto. Pero claro, por otro lado es importante que el modelo aprenda el patrón de las curvas ya que por ahora todos los datos de contagios en España siguen una tendencia creciente y, por tanto, si no aprendiese la forma de la curva de los países de entrenamiento, tendería a un crecimiento ilimitado ya que no existe dato que indique lo contrario. 




