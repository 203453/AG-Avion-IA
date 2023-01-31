# AG-Avion-IA
Algoritmo genético para distribuir pasajeros en un area de pasajeros de un avión con una configuración de n filas * 4 asientos por fila, las salidas son información de las generaciones e individuos, así como gráficas que representan a los mismos.

Un avion posee una cantidad de filas y columnas, las columnas son fijas en 4 (asientos por fila) y la cantidad de filas se puede configurar por el usuario, se configuran datos en la interfaz como la cantidad de pasajeros respetando como cantidad máxima el resultado de la multiplicación de (n filas * 4), dependiendo la cantidad de pasajeros se generara esta cantidad de pasajeros con masa de una media de 70 y una desviación estándar de 15, una vez se generen la cantidad de pasajeros introducida por el usuario, el resto para completar los asientos se crearán con masa = 0 simulando la ausencia de estos pasajeros pero la presencia de los asientos para mantener la configuración de la matriz.

Los pasajeros se distribuyen con distintas configuraciones generadas por el algoritmo genético tomando como mejor individuo o el mas apto a los de menor aptitud, es decir los mas cercanos a 0, pues se calcula la distancia entre el centro de masa del avión vacío y el centro de masa que genera la configuración de pasajeros.

Los pasajeros poseen propiedades de: 'ID', 'MASA', 'X', 'Y'
Los lugares y coordenadas se le asignan a los pasajeros según el orden que tenga la configuración que se le pasa como parámetro.

![image](https://user-images.githubusercontent.com/77992695/215649118-a7a15da1-04e5-4981-9b00-24094a38a0e6.png)


### Diagrama del funcionamiento de un algoritmo genético
![image](https://user-images.githubusercontent.com/77992695/215647466-fcdc5b9b-a886-47cc-acd2-5d2dee4e995f.png)
