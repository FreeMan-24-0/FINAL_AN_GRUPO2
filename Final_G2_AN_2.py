import sys
import time # Importamos esto para medir la velocidad (Cronómetro)

# --- CONFIGURACIÓN ---
INF = sys.maxsize

# 15 LUGARES (Del 0 al 14)
LUGARES = {
    0: "Hospital Central",   
    1: "Bomberos",        
    2: "Plaza de Armas",
    3: "Zona Industrial",    
    4: "Panamericana",    
    5: "Comisaría",
    6: "Aeropuerto",         
    7: "Estadio",         
    8: "Universidad",
    9: "Mercado Mayorista", 
    10: "Centro Financiero", 
    11: "Residencial Norte",
    12: "Puerto Marítimo",  
    13: "Parque Zonal",    
    14: "Terrapuerto"
}

# --- ALGORITMOS ---

def ruta_fuerza_bruta(origen, destino, grafo, visitados):
    if origen == destino:
        return 0
    
    visitados[origen] = True
    tiempo_minimo = INF
    n = len(grafo)

    for vecino in range(n):
        if grafo[origen][vecino] != INF and not visitados[vecino]:
            res = ruta_fuerza_bruta(vecino, destino, grafo, visitados)
            if res != INF:
                costo = grafo[origen][vecino] + res
                if costo < tiempo_minimo:
                    tiempo_minimo = costo
    
    visitados[origen] = False
    return tiempo_minimo

def optimizar_rutas_dinamico(grafo):
    n = len(grafo)
    dist = [fila[:] for fila in grafo] # Copia profunda

    # Los 3 bucles sagrados de Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != INF and dist[k][j] != INF:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
    return dist

# --- MAIN ---
if __name__ == "__main__":
    # MATRIZ 15x15 (Hecha para tener múltiples caminos y confundir a la fuerza bruta)
    # Es un mapa complejo: Muchas conexiones, algunas directas, otras trampas.
# MATRIZ 15x15 "MODO PESADILLA" (Alta Densidad de Conexiones)
    # Menos INF = Más caminos posibles = Fuerza Bruta sufre mucho más
    mapa_ciudad = [
        # 0    1    2    3    4    5    6    7    8    9   10   11   12   13   14
        [0,   10,  35,  INF, 50,  20,  INF, 80,  INF, INF, INF, INF, INF, INF, INF], # 0: Hospital (Más salidas)
        [10,   0,  15,  45,  20,  25,  INF, 30,  12,  60,  INF, INF, INF, INF, INF], # 1: Bomberos (Muy conectado)
        [35,  15,   0,  10,  40,   5,  70,  25,   8,  40,  INF, INF, INF, INF, INF], # 2: Plaza
        [INF, 45,  10,   0,   5,  30,  60,  INF,  55,  20,  20,  INF, INF, INF, INF], # 3: Industrial
        [50,  20,  40,   5,   0,  35,  15,  45,  INF, INF,  65,  30,  INF, INF, INF], # 4: Panamericana
        [20,  25,   5,  30,  35,   0,  40,  10,  25,  INF,  INF, INF, INF, INF, INF], # 5: Comisaría
        [INF, INF, 70,  60,  15,  40,   0,  50,  80,  90,  35,  45,  45,  INF, INF], # 6: Aeropuerto
        [80,  30,  25,  INF,  45,  10,  50,   0,  15,  20,  INF,  60,  INF,  20, INF], # 7: Estadio
        [INF, 12,   8,  55,  INF,  25,  80,  15,   0,  10,  30,  INF,  90,  INF, INF], # 8: Universidad
        [INF, 60,  40,  20,  INF, INF,  90,  20,  10,   0,   5,  15,  75,  40,  85], # 9: Mercado (Nudo crítico)
        [INF, INF, INF,  20,  65, INF,  35, INF,  30,   5,   0,  10,  25,  55,  50], # 10: Financiero
        [INF, INF, INF, INF,  30, INF,  45,  60, INF,  15,  10,   0,  15,  30,  40], # 11: Residencial
        [INF, INF, INF, INF, INF, INF,  45, INF,  90,  75,  25,  15,   0,  20,  35], # 12: Puerto
        [INF, INF, INF, INF, INF, INF, INF,  20, INF,  40,  55,  30,  20,   0,  10], # 13: Parque
        [INF, INF, INF, INF, INF, INF, INF, INF, INF,  85,  50,  40,  35,  10,   0]  # 14: Terrapuerto
    ]
    
    N = len(mapa_ciudad)
    print(f"--- SIMULACIÓN DE GRAN ESCALA ({N}x{N} Nodos) ---\n")

    # DEFINIMOS UNA RUTA DIFÍCIL (Del 0 al 14 cruzando todo el mapa)
    origen_test = 0  # Hospital
    destino_test = 14 # Terrapuerto (Al otro extremo)

    # 1. PRUEBA DE FUERZA BRUTA (MEDIMOS TIEMPO)
    print(f"1. Calculando con FUERZA BRUTA (Recursivo)... Espere...")
    visitados = [False] * N
    
    inicio_fb = time.time() # Start cronómetro
    costo_fb = ruta_fuerza_bruta(origen_test, destino_test, mapa_ciudad, visitados)
    fin_fb = time.time()    # Stop cronómetro
    
    tiempo_fb = fin_fb - inicio_fb
    print(f"   -> Costo Mínimo encontrado: {costo_fb} min")
    print(f"   -> TIEMPO DE CÓMPUTO: {tiempo_fb:.6f} segundos\n")

    # 2. PRUEBA DE PROGRAMACIÓN DINÁMICA (MEDIMOS TIEMPO)
    print(f"2. Calculando con FLOYD-WARSHALL (Dinámico)...")
    
    inicio_pd = time.time() # Start cronómetro
    matriz_optima = optimizar_rutas_dinamico(mapa_ciudad)
    costo_pd = matriz_optima[origen_test][destino_test]
    fin_pd = time.time()    # Stop cronómetro
    
    tiempo_pd = fin_pd - inicio_pd
    print(f"   -> Costo Mínimo encontrado: {costo_pd} min")
    print(f"   -> TIEMPO DE CÓMPUTO: {tiempo_pd:.6f} segundos\n")

    # 3. COMPARACIÓN FINAL
    print("--- VEREDICTO ---")
    if tiempo_fb > 0:
        veces_mas_rapido = tiempo_fb / tiempo_pd
        print(f"Floyd-Warshall fue {veces_mas_rapido:.2f} veces más rápido que Fuerza Bruta.")
    else:
        print("La fuerza bruta fue rápida, pero Floyd-Warshall calculó TODO el mapa a la vez.")