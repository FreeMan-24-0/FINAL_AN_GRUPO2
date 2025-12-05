import sys #Este Import SYS basicamente es una libreria que me permite poner un valor "infinito"
INF = sys.maxsize #Por eso mismo aqui especifico que la variable inf agarra un valor infinito de la misma libreria que es sys.maxsize
#Basicamente esto es para poder darle un valor imposible de alcanzar en una ruta real, pq si usaramos un valor como 1000 por ejemplo
#El algoritmo podria fallar y pensar que el numero que le he asignado es un numero real para trabajar

LUGARES = { #Basicamente esto es solo para que sepamos los valores y lo que representa cada uno de los nodos
    0: "Hospital Central (Norte)", #Por ejemplo este es el nodo 0 llamado Hospital Central
    1: "Base de Bomberos (Sur)", # Nodo 1
    2: "Plaza de Armas (Centro)", # Nodo 2
    3: "Zona Industrial (Accidentes)", #Nodo 3
    4: "Panamericana Norte" #Nodo 4
} #Esto es para que sepamos nosotros de que nodo a que nodo va, si es del 1 al 4, entonces seria "Desde el hospital central hasta Panamericana Norte"

#INICIO FUERZA BRUTA
def ruta_fuerza_bruta(origen, destino, grafo, visitados): #Esta es nuestra funcion que usa recursividad y tiene los parametros a la vista
    if origen == destino: #Como se sabe, si tu punto de origen es el mismo que el punto de destino, entonces no necesitas hacer ningun calculo
        return 0 #Por eso retorna a 0, ya que el costo y tiempo de llegada es 0. Sin esto la funcion no tendria fin.

    visitados[origen] = True #Esto es para que no existan los circulos viciosos, que si yo voy de A -> B, no quiero que este retroceda ya que tengo;
    #que calcular el tiempo y no puedo dejar que retroceda inmediatamente;
    tiempo_minimo = INF #Por eso mismo la variable tiempo_minimo se inicializa en infinito, ya que lo que yo busco es reducirlo.
    n = len(grafo) #Aqui se le asigna a la variable n la cantidad de elementos que tiene cada grafo
    
    for vecino in range(n): #A la variable vecino se le asigna dentro de un for, el rango N que se asigno arriba 
        #Aqui se ve que esto es fuerza bruta, ya que en el if de aqui abajo, solo se prueba ir de un punto a otro sin tener en cuenta;
        #si la direccion es buena o mala. No piensa como tal, solo prueba.
        if grafo[origen][vecino] != INF and not visitados[vecino]:
            tiempo_restante = ruta_fuerza_bruta(vecino, destino, grafo, visitados) #Esto es basicamente la recursividad que hay
            
            if tiempo_restante != INF: #si la recursividad encuentra un camino, se suman los tiempos hasta que encuentra el mejor resultado
                tiempo_total = grafo[origen][vecino] + tiempo_restante
                if tiempo_total < tiempo_minimo:
                    tiempo_minimo = tiempo_total
    #Aqui basicamente es para terminar y desmarcar el punto visitado como ya visitado, ya que necesitamos dejar el nodo libre nuevamente;
    #Para cuando se prueben futuras rutas y futuras pruebas, para que el programa sepa que puede volver a utilizar este camino (Backtracking)
    #Esto es como un laberinto cuando ya no tiene salida y tienes que retroceder, y haciendo el backtracking le permitimos al programa hacer eso
    visitados[origen] = False
    return tiempo_minimo
#FIN DE FUERZA BRUTA

#INICIO METODO Floyd-Warshall
def optimizar_rutas_dinamico(grafo): 
    n = len(grafo)
    dist = [fila[:] for fila in grafo]
    #Aqui lo que primero se hace es medir el tamaño del mapa en una variable n, y hace una copia de la matriz original en una variable llamada "dist"
#El "dist" es lo que lo hace programacion dinamica, ya que es la tabla donde se ira guardando y actualizando los calculos.

    for k in range(n): #Este bucle externo "K" actua como punto intermedio entre los demas puntos
        for i in range(n): #La variable "i" seria el Origen (Hospital)
            for j in range(n): # La variable "j" seria el Destino (Accidente)
#Lo que hace esto es que Los bucles recorren la matriz completa, tanto fila como columna pasando por el nodo k que mas le sirve;
#En este caso, el atajo mas rapido entre ellos.

#             
# Ecuacion de bellman (la logica del ahorro [Tengo que estudiarlo mejor]) y Comparacion matematica
# La ecuacion de recurrencia es asi, primero se pregunta: si voy de i a k y luego de k a j, me demoro menos que yendo directo?
# Si esto es verdadero, entonces se actualiza la tabla "dist" de arriba con el nuevo tiempo grabado. y asi se va puliendo la matriz hasta que se optimice.
# o en su defecto, hasta que la matriz quede perfecta.
# 
                if dist[i][k] != INF and dist[k][j] != INF:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
    return dist
#Y ya para acabar, el dist que retorna es el valor total de la tabla, esta te retorna el resultado final para usarlo en el sistema de emergencias.

#Simulacion:
#AQUI ES DONDE EMPIEZA A EJECUTARSE EL CODIGO REALMENTE, TODO LO ANTERIOR SON LAS FORMULAS
if __name__ == "__main__":
    mapa_ciudad = [ #Aqui el origen es Fila y Destino es Columna
        [0,   10,  INF, 45,  INF], #Aqui la ruta empieza desde el Hospital Central 
        [10,  0,   15,  INF, 20],  
        [INF, 15,  0,   10,  INF], 
        [45,  INF, 10,  0,   5],   
        [INF, 20,  INF, 5,   0]    
    ]
    N = len(mapa_ciudad)

    print("--- INICIANDO SISTEMA DE DESPACHO DE EMERGENCIAS ---\n")

    print(f"Calculando ruta Hosp. Central -> Zona Industrial con Fuerza Bruta...")
    #Linea de memoria del algoritmo de fuerza bruta
    visitados = [False] * N #Se sabe que esto es para que cuando se visite un lugar no caiga en un bucle el algoritmo de fuerza bruta
    tiempo_fb = ruta_fuerza_bruta(0, 3, mapa_ciudad, visitados)
    print(f"Resultado FB: {tiempo_fb} minutos (Cálculo lento y repetitivo)\n")

    #Ejecucion de programacion dinamica
    print("Ejecutando Floyd-Warshall para pre-calcular TODAS las rutas...")
    #aqui se llama a la funcion del floyd-warshall, aqui "matriz_tiempos" ahora tiene LAS RUTAS
    matriz_tiempos = optimizar_rutas_dinamico(mapa_ciudad) 
    print("¡Matriz Maestra generada con éxito!\n")
    #Luego se hace un uso de caso real en el que se reporta un accidente.
    accidente_en = 3 #Sabemos que el punto 3 es la Zona Industrial
    unidades_disponibles = [0, 1] #Esto sabemos que son Hospital y Bomberos
    #Se les llama unidades_disponibles pq sabemos que entre los 2, el que menor tiempo tenga es el que se decide mandar.


    print(f"*** ALERTA: Accidente reportado en {LUGARES[accidente_en]} ***")
    print("Evaluando mejor unidad de respuesta...\n")

    mejor_unidad = -1 #Aqui se le pone -1 ya que esta esperando por un nodo para confirmar, si le ponemos 0 tomaria que es el hospital
    mejor_tiempo = INF # Aqui igualmente, se le pone un valor no accesible para luego cambiarlo por uno que si.

    for unidad in unidades_disponibles:
        tiempo = matriz_tiempos[unidad][accidente_en] #Aqui se busca en la matriz_tiempos quien llega mas rapido, la unidad hasta el accidente;
        #Y se almacena esa informacion en la variable tiempo.
        print(f" - Tiempo desde {LUGARES[unidad]}: {tiempo} minutos")
        
        if tiempo < mejor_tiempo: #Esto se puede leer por si solo, si el tiempo es menor que el "infinito", entonces:
            mejor_tiempo = tiempo #el mejor tiempo ahora pasa a tener la informacion de tiempo,
            mejor_unidad = unidad #y la mejor unidad pasa a tener la informacion de unidad.
#FIN METODO Floyd-Warshall

    print(f"\n>>> DECISIÓN DEL SISTEMA: DESPACHAR UNIDAD DE {LUGARES[mejor_unidad]}")
#Esta linea imprime los resultados del floyd-warshall, ya que ya se sabe cual es la mejor unidad para despachar
#Aparte de que la orden es clara como se puede leer.

    print(f">>> Tiempo estimado de llegada: {mejor_tiempo} minutos.")
#El 2do print es el dato critico sobre el tiempo de llegada o sea el valor minimo que se encontro en la matriz, por eso se imprime la variable mejor_tiempo

    print(f">>> Ahorro vs ruta directa: {mapa_ciudad[0][3] - mejor_tiempo} minutos ganados.")
#Este ultimo print es la justificacion que hay al usar floyd-warshall y por que es mejor que la fuerza bruta, ya que se restan los tiempos de ambos.
#Mostrando el tiempo como algo mas que justificable sabiendo que se trata de un problema real teniendo un impacto verdadero.