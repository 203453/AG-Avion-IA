# Algoritmo genético Avión IA
### Algoritmo genético para encontrar las mejores configuraciones (distribuciones) de pasajeros dentro de un avión en base a centros de masa con parámetros configurables
Algoritmo genético para distribuir pasajeros en un area de pasajeros de un avión con una configuración de n filas * 4 asientos por fila, las salidas son información de las generaciones e individuos, así como gráficas que representan a los mismos.

Un avion posee una cantidad de filas y columnas, las columnas son fijas en 4 (asientos por fila) y la cantidad de filas se puede configurar por el usuario, se configuran datos en la interfaz como la cantidad de pasajeros respetando como cantidad máxima el resultado de la multiplicación de (n filas * 4), dependiendo la cantidad de pasajeros se generara esta cantidad de pasajeros con masa de una media de 70 y una desviación estándar de 15, una vez se generen la cantidad de pasajeros introducida por el usuario, el resto para completar los asientos se crearán con masa = 0 simulando la ausencia de estos pasajeros pero la presencia de los asientos para mantener la configuración de la matriz.

Los pasajeros se distribuyen con distintas configuraciones generadas por el algoritmo genético tomando como mejor individuo o el mas apto a los de menor aptitud, es decir los mas cercanos a 0, pues se calcula la distancia entre el centro de masa del avión vacío y el centro de masa que genera la configuración de pasajeros.

Los pasajeros poseen propiedades de: 'ID', 'MASA', 'X', 'Y'
Los lugares y coordenadas se le asignan a los pasajeros según el orden que tenga la configuración que se le pasa como parámetro.

### Libreria utilizadas
   tkinter
   matplotlib
   customtkinter
   numpy
   random
   math
   string

### Interfaz
![image](https://user-images.githubusercontent.com/77992695/215649659-e06eb936-9c4d-499b-acc4-030ad582c28e.png)

### Salida consola
![image](https://user-images.githubusercontent.com/77992695/215649931-085b05df-09c2-4451-9f7e-ecc93a43b5c6.png)


### Gráfica de la configuración del mejor individuo
![image](https://user-images.githubusercontent.com/77992695/215649891-5a6d6f78-c49b-43ec-b6d1-f146ccd6e0ae.png)


### Diagrama del funcionamiento de un algoritmo genético
![image](https://user-images.githubusercontent.com/77992695/215647466-fcdc5b9b-a886-47cc-acd2-5d2dee4e995f.png)
