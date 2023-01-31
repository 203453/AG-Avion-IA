import math
import random
import string
from tkinter import *
import tkinter
import customtkinter
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

# Autor: Emilio Jarey Méndez Torres
# 203453

pasajeros = []

# Se genera la población de pasajeros en una lista diccionario con IDs y masas random y coordenadas inicializadas en 0
def generar_pasajeros(cardinalidad, num_pasajeros):
    i = 0
    pasajeros = []
    n_pasajeros = num_pasajeros#random.randint(4, cardinalidad)
    for _ in range(cardinalidad):
        # Genera una nueva letra aleatoria
    
        random_id = random.choice(string.ascii_uppercase) + (str(random.randint(0, 9)))

        if (_ < n_pasajeros):
            random_masa = round(random.normalvariate(70, 15), 1)
        else:
            random_masa = 0


        if len(pasajeros) > 0:
            for aux in range(len(pasajeros)):
                while pasajeros[aux]['id'] == random_id:
                    print('Se repitio un ID:', random_id)
                    random_id = random.choice(string.ascii_uppercase) + (str(random.randint(0, 9)))
        
        pasajeros.append({"id":random_id,"masa":random_masa,"x":0,"y":0})
                

    # print("\nPasajeros:")
    # for pasajero in pasajeros:
    #     i += 1
    #     print('> Pasajero',i,'-> ID:', pasajero['id'],'- Masa:',pasajero['masa'],'- Coor. X:',pasajero['x'],'- Coor. Y:',pasajero['y'])
    return pasajeros

#Se calcula el numero de asientos que tendrá el avión mediante el numero de filas teniendo en cuenta que cada fila tiene 4 asientos
def asientos(filas, asientos):
    #Filas pide este dato desde la interfaz
    
    num_asientos = filas * asientos
    print("Numero de filas:",filas)
    print("Numeros de asientos en el avion:",num_asientos)
    return num_asientos

# Se genera la poblacion de configuraciones inicial, primero se calcula el centro de masa del avion vacio generando un arreglo auxiliar
# que almacena los IDs de los pasajeros formando asi una configuracion auxiliar la cual sera tomada en cuenta para calcular el centro de masa
# del avion vacio, posteriormente dentro de un for de la cantidad total de pasajeros (asientos) se almacenan los IDs en un array para luego hacer
# un shuffle formando asi la primer configuracion inicial, se le asignan lugares (coordenadas (x, y)) a los pasajeros respetando el orden de la configuracion
# formada, posteriormente se calcula el centro de masa de la configuracion o individuo y asi poder calcular su aptitud respecto al CMV, una vez completada una iteracion,
# se agrega a un arreglo de configuraciones la configuracion generada, centro de masa de la conf, y su aptitud.
def generar_poblacion(pasajeros, filas):
    configuraciones = []
    config_aux = []
    i = 0

    for pasajero in pasajeros:
        config_aux.append(pasajero['id'])

    pasajeros_aux = asignar_lugar(pasajeros, filas, config_aux)
    coor_cmv = centro_masa_vacio(pasajeros_aux)
    print('\nCentro de masa del avion vacio (COORDS):')
    print(coor_cmv[0])

    # print("\nPoblacion inicial (Individuos):")
    for aux in pasajeros:
        config = []
        cdm = []
        i += 1
        
        for pasajero in pasajeros:
            config.append(pasajero['id'])

        random.shuffle(config)
        # print("\nConfiguración",i,":",config)
        
        pasajeros = asignar_lugar(pasajeros, filas, config)

        cdm = centro_masa_configuracion(pasajeros)
        
        # print('Pasajeros abordo:')
        # for pasajero in pasajeros:
        #     print('>',pasajero)
        
        # print('Masa total de los individuos ' +str(i)+':')
        # print('->',cdm[0])

        # print('Centro de masa de la configuracion ' +str(i)+':')
        # print('->',cdm[0])

        aptitud = calcular_aptitud(cdm, coor_cmv)
        configuraciones.append([config,cdm,[aptitud]])
        # print('La aptitud de la configuracion ' + str(i) + ' es:')
        # print('->',aptitud)
        
      
    return configuraciones, coor_cmv

# Resetea coordenadas del diccionario de pasajeros cada que se implementa una nueva configuracion
def reset_coordenadas(pasajeros):
    for pasajero in pasajeros:
        if pasajero['x'] != 0 and pasajero['y'] != 0:
            pasajero['x'] = 0
            pasajero['y'] = 0
    return pasajeros

# Se calcula el centro de masa del avion vacio dependiendo la cantidad de asientos
def centro_masa_vacio(pasajeros):
    coor_cmv = []
    cmv_x = 200
    last_pas = pasajeros[len(pasajeros)-1]
    y = last_pas['y']
    y += 40
    cmv_y = int(y/2)
    coor_cmv.append((cmv_x,cmv_y))
    return coor_cmv

# Se calcula el centro de masa de la configuracion de los individuos en el diccionario, se utiliza su masa, y sus coordenadas (x, y)
# para dividir todo entre la suma de las masas, esto se hace tanto para x como para y
def centro_masa_configuracion(pasajeros):
    coor_cdm = []
    sum_x = 0
    sum_div = 0
    sum_y = 0
    for pasajero in pasajeros:
        x = pasajero['x']
        y = pasajero['y']
        m = pasajero['masa']
        sum_div += m
        mult_x = (m*x)
        sum_x += mult_x
        mult_y = (m*y)
        sum_y += mult_y
    res_x = sum_x / sum_div
    res_x = round(res_x, 2)
    res_y = sum_y / sum_div
    res_y = round(res_y, 2)
    coor_cdm.append((res_x, res_y))
    return coor_cdm

# se asignan lugares (coordenadas) a los pasajeros respetando la configuracion pasada como parametro, es decir, el arreglo de IDs el orden en el que,
# se encuentren los IDs ahi, en ese orden asignará lugares a los pasajeros en el diccionario, ademas de esto, se respeta el numero de filas para 
# agregar coordenadas en Y y mediante un IF, se agregan coordenadas a X dentro de una misma iteracion de Y
# siempre y cuando no supera 4 iteraciones pues son 4 asientos por fila, en este caso, se establecio un ancho de pasillo de 80, respetando las medidas
# de los asientos 80 x 80, se inicializa en 40 los valores pues el centro de un asiento es 40, 40 y sus bordes son 80, 80
def asignar_lugar(pasajeros, filas, config):
    pasajeros = reset_coordenadas(pasajeros)
    y = 40
    for i in range(filas):
        x = 40
        aux = 0
        for conf in config:
            for pasajero in pasajeros:
                if pasajero['id'] == conf:
                    if pasajero['x'] == 0 and pasajero['y'] == 0:
                        if aux < 4:
                            if aux == 2:
                                x += 80
                                pasajero['x'] = x
                                pasajero['y'] = y
                            else: 
                                pasajero['x'] = x
                                pasajero['y'] = y
                            aux += 1
                            x += 80
        y += 80

    return pasajeros

# Se calcula la distancia entre coordenada de la configuracion (centro de masa de la configuracion) y el centro de masa vacio (coords)
def calcular_aptitud(cmc, cmv):
        cmc = cmc[0]
        cmv = cmv[0]
        x_centro = cmv[0]
        y_centro = cmv[1]
        x_conf = cmc[0]
        y_conf = cmc[1]
        distancia = math.sqrt((x_conf-x_centro)**2+(y_conf-y_centro)**2)
        return distancia

# Funcion para tomar como indice la aptitud en el arreglo de configuraciones y poder ordenar de menor a mayor mediante sort segun se requiera 
def take_aptitude(list):
    list = list[2]
    return list

# Genera parejas de individuos priorizando a los de aptitud mas baja haciendo que estos tengan mas cantidad de parejas y en decremento
def generar_pares(population):
  pairs = []
  configuraciones_aux = []
  i=0

  for config in population:
    configuraciones_aux.append(config[0])
    
  for i in range(len(configuraciones_aux)):
    for j in range(i+1, len(configuraciones_aux)):
      pairs.append((configuraciones_aux[i], configuraciones_aux[j]))

  return pairs

# Cruza de primer orden
def cruza(parejas):
    descendencia = []
    padre1_aux = []
    padre2_aux = []
    punto_inicio = 0
    punto_final = len(parejas[0][0])-1

    for pareja in parejas:
        padre1_aux.append(pareja[0])
        padre2_aux.append(pareja[1])

    for n in range(2):
        if n == 1:
            # Padres intercambian de posicion en la segunda iteracion para formar los segundos hijos
            parejas.clear()
            for k in range(len(padre1_aux)):
                parejas.append((padre2_aux[k],padre1_aux[k]))

        # Excepcion para cuando el punto de inicio es 0 y el punto final es 7, se generan nuevos random, pues no es posible este parametro
        while(punto_inicio == 0 and punto_final == len(parejas[0][0])-1):
            punto_inicio = random.randint(0,len(parejas[0][0])-2)
            punto_final = random.randint(punto_inicio+1,len(parejas[0][0])-1)

        for pareja in parejas:
            # Se inicializa un arreglo de longitud n con elementos 0 que seran sustituidos
            hijo1 = []
            for aux in range(len(parejas[0][0])):
                hijo1.append(0)
            # Se agrega el pedazo tomado aleatoriamente del padre 0 hacia el hijo en la misma posicion
            hijo1[punto_inicio:punto_final+1] = pareja[0][punto_inicio:punto_final+1]

        # Inicia proceso para agregar elementos del segundo padre al hijo sin repetirlos y respetando el orden

            # Si punto final del corte vale igual al tamaño maximo de una configuracion
            if(punto_final+1 > len(parejas[0][0])-1):
                i = 0
                j = 0
                for aux in range(len(parejas[0][0])):
                    if (pareja[1][j] not in hijo1) and (hijo1[i] == 0):
                        hijo1[i] = pareja[1][j]
                        i += 1
                    j += 1
            # Si punto final del corte NO vale igual al tamaño maximo de una configuracion
            else:
                aux = 0
                i = punto_final+1
                j = punto_final+1
                for aux in range(len(parejas[0][0])):
                    j += 1
                    if j == (len(parejas[0][0])+1):
                        j = 1
                    if i == (len(parejas[0][0])):
                        i = 0
                    if (pareja[1][j-1] not in hijo1) and (hijo1[i] == 0):
                        hijo1[i] = pareja[1][j-1]
                        i += 1
                    elif (pareja[1][j-1] in hijo1) and (hijo1[i] == 0) and (j-1 == len(parejas[0][0])-1):
                        j = 0
                i = 0
                j = 0
                for aux in range(len(parejas[0][0])):
                    if (pareja[1][j] not in hijo1) and (hijo1[i] == 0):
                        hijo1[i] = pareja[1][j]
                        i += 1
                    j += 1

            descendencia.append(hijo1)
    return descendencia

# Mutacion por individuo intercambiando 1 sola vez 2 pasajeros (genes) de su contenido o configuracion
def mutacion(descendencia, p_mut_ind):
    random_gen_position = 0
    random_gen_position2 = 0
    for hijo in descendencia:
        if random.random() < p_mut_ind:
            while random_gen_position == random_gen_position2:
                random_gen_position = random.randint(0, len(descendencia[0])-1)
                random_gen_position2 = random.randint(0, len(descendencia[0])-1)
            pasajero1 = hijo[random_gen_position]
            pasajero2 = hijo[random_gen_position2]
            hijo[random_gen_position] = pasajero2
            hijo[random_gen_position2] = pasajero1
    return descendencia

# Se calcula la aptitud de las nuevas configuraciones generadas (arreglos de IDs)
def calcular_aptitud_nuevos(pasajeros, filas, config, i, coor_cmv):
    i += 1
    pasajeros = asignar_lugar(pasajeros, filas, config)
    cdm = centro_masa_configuracion(pasajeros)
    # print("\nConfiguración",i,":",config)
    # print('Pasajeros abordo:')
    # for pasajero in pasajeros:
    #     print('>',pasajero)
    # print('Centro de masa de la configuracion ' +str(i)+':')
    # print('->',cdm[0])
    aptitud = calcular_aptitud(cdm, coor_cmv)
    # print('La aptitud de la configuracion ' + str(i) + ' es:')
    # print('->',aptitud)
    return [config,cdm,[aptitud]]

# Primero se eliminan repetidos y luego la poblacion se parte a la mitad retornando
# la mitad mas apta y respetando la poblacion maxima definida
def poda(configuraciones, pob_max):
    cut_point = len(configuraciones) // 2
    i=0
    for config in configuraciones:
        while(configuraciones.count(config) > 1):
            configuraciones.remove(config)
        i+=1
    configuraciones = configuraciones[:cut_point]
    return configuraciones[:pob_max]

# Funcion principal del algoritmo
def avion(filas, num_pasajeros, generaciones, pob_max, p_mut_ind):
    best_ind = []
    the_best = []
    num_asientos = asientos(filas, 4)
    pasajeros = generar_pasajeros(num_asientos, num_pasajeros)
    configuraciones, coor_cmv = generar_poblacion(pasajeros, filas)
    for _ in range(generaciones):
        parejas = []
        descendencia = []
        descendencia_mutada = []
        all_ind = []

        # Se ordenan las configuraciones (arreglos de IDs) de menor a mayor por aptitud, pues entre menor sea la aptitud, es mejor
        configuraciones.sort(key=take_aptitude)
        # print('\nPoblacion inicial (configuraciones):')
        # for config in configuraciones:
        #     print('>',config)

        parejas = generar_pares(configuraciones)
        # print('\nParejas:')
        # for pareja in parejas:
        #     print('>',pareja)

        descendencia = cruza(parejas)
        # print('\ndescendencia:')
        # for hijo in descendencia:
        #     print('>',hijo)
        
        descendencia_mutada = mutacion(descendencia,p_mut_ind)
        # print('\ndescendencia mutada:')
        # for hijo in descendencia_mutada:
        #     print('>',hijo)

        # Calcula aptitud de las configuraciones de descendencia mutada y la configuracion no se encuentra en el arreglo principal, se inserta, caso contrario NO se inserta
        i=0
        flag = True
        for config in descendencia_mutada:
            i+=1
            aux = calcular_aptitud_nuevos(pasajeros, filas, config, i, coor_cmv)
            #Se verifica que si la configuracion calculada ya existe en las configuraciones existentes
            for config in configuraciones:
                if config[0] == aux[0]:
                    flag = True
                else:
                    flag = False
            if flag == False:
                configuraciones.append(aux)

        # Se vuelve a ordenar por aptitud de menor a mayor            
        configuraciones.sort(key=take_aptitude)

        # Se poda a las configuraciones (revisar comentarios de la funcion para mayor explicacion)
        configuraciones = poda(configuraciones, pob_max)

        # Arreglo de mejores individuos por generacion, se inserta la primer posicion pues es el menor de todos
        best_ind.append(configuraciones[0])

        print('\nConfiguraciones generacion podada '+str(_+1)+':')
        for config in configuraciones:
            print('>',config)
        
        # Arreglo de generacion, contiene todas las configuraciones o individuos de su generacion (iteracion)
        all_ind = configuraciones.copy()

        # Se ordenan por aptitud de mayor a menor con fines practicos para su uso en la graficacion
        all_ind.sort(key=take_aptitude, reverse=True)

        ################################# DESCOMENTAR LA GRAFICA QUE SE DESEA USAR ##############################

        #graficar_generacion(all_ind, _+1, coor_cmv)
        
        #graficar_generacion2(all_ind, _+1, coor_cmv)

        graficar_mejor_configuracion_generacion(_+1, coor_cmv, pasajeros, filas, best_ind[_][0])

        ################################# DESCOMENTAR LA GRAFICA QUE SE DESEA USAR ##############################

    # Se hace una copia del array de los mejores individuos de cada generacion
    arr_aux = best_ind.copy()

    # Se ordena el array de la copia de menor a mayor por aptitud
    arr_aux.sort(key=take_aptitude)

    # Array que contiene datos del mejor de individuo de TODOS, se le inserta la primer posicion del array de la copia
    the_best.append(arr_aux[0])
    
    ################################# DESCOMENTAR LA GRAFICA QUE SE DESEA USAR ##############################

    #graficar_mejor_individuo(best_ind, coor_cmv)

    ################################# DESCOMENTAR LA GRAFICA QUE SE DESEA USAR ##############################

    return the_best

# Se grafica el mejor individuo de cada generacion en una grafica general de todas las generaciones
def graficar_mejor_individuo(best_ind, cmv):
    fig, ax = plt.subplots(dpi=90, figsize=(10,5),facecolor='#fefffe')
    plt.suptitle('Evolución del mejor individuo')
    ax.set_xlabel('Generación')
    ax.set_ylabel('Aptitud')
    plt.title(('CMV:'+ str(cmv[0])),loc='right')
    plt.grid()

    x_values = []
    y_values = []
     
    for j in range(len(best_ind)):
        x_values.append(j+1)

    for individuo in best_ind:
        aptitud = individuo[2]
        y_values.append(round(aptitud[0],4))
        
    for i in range(len(x_values)):
        color_txt = 'black'
        plt.text(x_values[i]+0.01,y_values[i], str(y_values[i]), fontsize=7, color=color_txt,rotation=55)
    line = ax.plot(x_values, y_values,marker='o',linestyle='dashed', color='b')
    line2 = ax.plot(x_values[0], y_values[0],marker='o',linestyle='dashed', color='r')
    if len(x_values) <= 20:
        plt.xticks(x_values)
    plt.xticks(rotation=45)
    plt.grid()
    plt.draw()
    plt.show()

# Se grafica cada generacion en su respectiva grafica
def graficar_generacion(all_ind, k, cmv):
    fig, ax = plt.subplots(dpi=90, figsize=(10,5),facecolor='#fefffe')
    plt.suptitle('Generación '+str(k))
    ax.set_xlabel('Generación')
    ax.set_ylabel('Aptitud')
    plt.title(('CMV:'+ str(cmv[0])),loc='right')
    plt.grid()

    x_values = []
    y_values = []

    for r in range(len(all_ind)):
        x_values.append(r+1)

    for r in range(len(all_ind)):
        aptitud = all_ind[r][2]
        y_values.append(round(aptitud[0],4))

    for i in range(len(x_values)):
        color_txt = 'black'
        plt.text(x_values[i]+0.05,y_values[i], str(y_values[i]), fontsize=7, color=color_txt,rotation=60)
    line = ax.plot(x_values, y_values,marker='o',linestyle='dashed', color='b')
    line2 = ax.plot(x_values[0], y_values[0],marker='o',linestyle='dashed', color='r')
    if len(x_values) <= 20:
        plt.xticks(x_values)
    plt.xticks(rotation=45)
    plt.grid()
    plt.draw()
    plt.show()

def graficar_generacion2(all_ind, k, cmv):
    fig, ax = plt.subplots(dpi=90, figsize=(10,8),facecolor='#fefffe')
    plt.suptitle('Generación '+str(k))
    ax.set_xlabel('X')
    ax.set_ylabel('Y', rotation=90)
    plt.grid()

    x_values = []
    y_values = []

    for r in range(len(all_ind)):
        coor_x = all_ind[r][1][0][0]
        coor_x = round(coor_x*0.1,4)
        x_values.append(coor_x)
        coor_y = all_ind[r][1][0][1]
        coor_y = round(coor_y*0.1,4)
        y_values.append(coor_y)
    
    for coor in cmv:
        cmv_x = coor[0]*0.1
        cmv_y = coor[1]*0.1
    
    ax.plot(x_values, y_values, 'o', color='b')
    ax.plot(cmv_x, cmv_y,'o', color='r', label="CDM de avión vacío\n"+"("+str(cmv_x)+", "+str(cmv_y)+")")
    plt.xticks(np.arange(0, 41,5.0))
    plt.xticks(fontsize=8,rotation=45)
    plt.yticks(np.arange(0, (coor_y*2),5.0))
    plt.yticks(fontsize=8,rotation=0)
    ax.legend(loc='best')
    plt.grid()
    plt.draw()
    plt.show()

def graficar_mejor_configuracion_generacion(k, cmv, pasajeros, filas, config):
    pasajeros = asignar_lugar(pasajeros, filas, config)
    cdm = centro_masa_configuracion(pasajeros)

    cdm_x = round(cdm[0][0]*0.1,4)
    cdm_y = round(cdm[0][1]*0.1,4)

    print("\nMejor configuración de la generación",k,":",config)

    fig, ax = plt.subplots(dpi=90, figsize=(10,8),facecolor='#fefffe')
    plt.suptitle('Mejor configuración de la generación '+str(k))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    plt.grid()

    x_values = []
    y_values = []
    
    for coor in cmv:
        cmv_x = coor[0]*0.1
        cmv_y = coor[1]*0.1
    
    for pasajero in pasajeros:
        x = pasajero['x']*0.1
        y = pasajero['y']*0.1
        if pasajero['masa'] > 0:
            ax.plot(x, y, 'o', color='b')
        else:
            ax.plot(x, y, 'o', color='gray')
        y_values.append(y)
        plt.text(x-0.5,y-1.8, str(pasajero['masa'])+" kg", fontsize=8, color='black',rotation=0)
        
    ax.plot(cmv_x, cmv_y,'o', color='r', label="CDM de avión vacío\n"+"("+str(cmv_x)+", "+str(cmv_y)+")")
    ax.plot(cdm_x, cdm_y,'o', color='y', label="CDM de configuración\n"+"("+str(cdm_x)+", "+str(cdm_y)+")")
    ax.legend(loc='best')
    plt.xticks(np.arange(0, 41,5.0))
    plt.xticks(fontsize=8,rotation=45)
    plt.yticks(np.arange(0, (cmv_y*2)+2,2.0))
    plt.yticks(fontsize=8,rotation=0)
    plt.grid()
    plt.draw()
    plt.show()

# Interfaz con CustomTkinter
def gui():
    the_best = []

    customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    app = customtkinter.CTk()
    app.geometry("320x460")
    app.resizable(False, False)
    app.title("Práctica 03 IA")

    sv = StringVar()
    sv.trace("w",lambda name, index, mode, sv=sv: num_pasajeros_callback(sv))

    def button_callback():
        print("Inicia...\n")
        num_filas = entry_1.get()
        num_pasajeros = slider_1.get()
        generaciones = entry_3.get()
        pob_max = slider_2.get()
        p_mut_ind = slider_3.get()

        num_filas = int(num_filas)
        num_pasajeros = int(num_pasajeros)
        generaciones = int(generaciones)
        pob_max = int(pob_max)
        p_mut_ind = float(p_mut_ind) * 0.01
        p_mut_ind = round(p_mut_ind,2)

        the_best = avion(num_filas,num_pasajeros,generaciones,pob_max,p_mut_ind)

        print('\nLa mejor configuracion es:')
        print('>', the_best[0])


    def slider_callback(value):
        value = int(value)
        label_4.configure(text=value)

    def slider_callback2(value):
        value = int(value)
        if value >= 100:
            label_8.configure(text='Max')
        else:
            label_8.configure(text=value)
    
    def slider_callback3(value):
        value = int(value)
        label_10.configure(text=str(value)+'%')

    def num_pasajeros_callback(value):
        valor = value.get()
        if valor != '':
            try:
                label_valor = label_4.cget("text")
                label_valor = int(label_valor)
                valor = int(valor)
                slider_1.configure(from_=2,to=valor*4)
                slider_1.set(2)
                label_4.configure(text=2)
            except ValueError:
                print('No inserte letras o espacios')
            return valor

    frame_1 = customtkinter.CTkFrame(master=app)
    frame_1.pack(pady=20, padx=20, fill="both", expand=True)

    label_1 = customtkinter.CTkLabel(master=frame_1, text="Distribución avión",justify=customtkinter.LEFT,font=customtkinter.CTkFont(size=18, weight="bold"))
    label_1.pack(pady=(15,10), padx=10)

    label_2 = customtkinter.CTkLabel(master=frame_1, text="Número de filas*", justify=tkinter.LEFT)
    label_2.pack(pady=0, padx=32, anchor="w")

    entry_1 = customtkinter.CTkEntry(master=frame_1, width=220, textvariable=sv,  placeholder_text="ej. 4")
    entry_1.pack(pady=(0, 10), padx=10)

    label_6 = customtkinter.CTkLabel(master=frame_1, text="Generaciones*", justify=tkinter.LEFT)
    label_6.pack(pady=0, padx=32, anchor="w")

    entry_3 = customtkinter.CTkEntry(master=frame_1, placeholder_text="ej. 4", width=220)
    entry_3.pack(pady=(0, 10), padx=10)

    label_3 = customtkinter.CTkLabel(master=frame_1, text="Número de pasajeros*", justify=tkinter.LEFT)
    label_3.pack(pady=0, padx=32, anchor="w")

    slider_1 = customtkinter.CTkSlider(master=frame_1, command=slider_callback, from_=0, to=2,width=190)
    slider_1.pack(pady=(0,10), padx=(0,40))
    slider_1.set(0)

    label_4 = customtkinter.CTkLabel(master=frame_1,text="2", justify=tkinter.LEFT)
    label_4.place(anchor="e", y=220, x=240)

    label_5 = customtkinter.CTkLabel(master=frame_1, text="Población máxima*", justify=tkinter.LEFT)
    label_5.pack(pady=0, padx=32, anchor="w")

    slider_2 = customtkinter.CTkSlider(master=frame_1, command=slider_callback2, from_=2, to=100,width=190)
    slider_2.pack(pady=(0,10), padx=(0,40))
    slider_2.set(0)

    label_8 = customtkinter.CTkLabel(master=frame_1,text="2", justify=tkinter.LEFT)
    label_8.place(anchor="e", y=275, x=240)

    label_9 = customtkinter.CTkLabel(master=frame_1, text="Prob. mutación del invidividuo*", justify=tkinter.LEFT)
    label_9.pack(pady=0, padx=32, anchor="w")

    slider_3 = customtkinter.CTkSlider(master=frame_1, command=slider_callback3, from_=0, to=100, width=190)
    slider_3.pack(pady=(0,10), padx=(0,40))
    slider_3.set(50)

    label_10 = customtkinter.CTkLabel(master=frame_1,text="50%", justify=tkinter.LEFT)
    label_10.place(anchor="e", y=330, x=248)

    button_1 = customtkinter.CTkButton(master=frame_1, text="Iniciar", command=button_callback)
    button_1.pack(pady=15, padx=10)

    label_11 = customtkinter.CTkLabel(master=frame_1, text="", justify=tkinter.LEFT, font=customtkinter.CTkFont(weight="bold"))
    label_11.pack(pady=0, padx=32, anchor="w")

    label_12 = customtkinter.CTkLabel(master=frame_1, text="", justify=tkinter.LEFT)
    label_12.pack(pady=0, padx=32, anchor="w")

    label_13 = customtkinter.CTkLabel(master=frame_1, text="", justify=tkinter.LEFT)
    label_13.pack(pady=0, padx=32, anchor="w")

    label_14 = customtkinter.CTkLabel(master=frame_1, text="", justify=tkinter.LEFT)
    label_14.pack(pady=0, padx=32, anchor="w")

    app.mainloop()
       
gui()
#avion(2,6,3,8,0.5)