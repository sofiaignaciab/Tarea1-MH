import time

class CentroVacunacion:
    def __init__(self):

        self.adyacencias = {
            1: [4, 3, 13],
            2: [4, 1, 12, 15],
            3: [13, 1, 4, 5, 6],
            4: [3, 1, 2, 12, 5],
            5: [3, 4, 12, 7, 8, 9, 6],
            6: [3, 5, 9],
            7: [5, 8, 12, 15, 14, 11, 10],
            8: [5, 7, 9, 10],
            9: [6, 5, 8, 10, 11],
            10: [9, 8, 7, 11],
            11: [7, 10, 9, 14],
            12: [5, 4, 2, 15, 7],
            13: [1, 3],
            14: [7, 11, 15],
            15: [2, 12, 7, 14]
        }
        
        self.costos = {
            1: 60, 2: 30, 3: 60, 4: 70, 5: 130,
            6: 60, 7: 70, 8: 60, 9: 80, 10: 70,
            11: 50, 12: 90, 13: 30, 14: 30, 15: 100
        }
        
        self.todas_comunas = list(range(1, 16))

def todas_comunas_cubiertas(centros, problema):
    cubiertas = set()
    for centro in centros:
        cubiertas.add(centro)
        for adyacente in problema.adyacencias.get(centro, []):
            cubiertas.add(adyacente)
    return len(cubiertas) == len(problema.todas_comunas)

def backtracking_cronologico_iterativo():
    problema = CentroVacunacion()
    mejor_solucion = None
    mejor_costo = float('inf')
    
    stack = []
    stack.append(([], 0, 0))
    
    while stack:
        sol_parcial, idx, costo_actual = stack.pop()
        
        if todas_comunas_cubiertas(sol_parcial, problema):
            if costo_actual < mejor_costo:
                mejor_solucion = sol_parcial.copy()
                mejor_costo = costo_actual
            continue
        
        if idx >= len(problema.todas_comunas) or costo_actual >= mejor_costo:
            continue
        
        comuna_actual = problema.todas_comunas[idx]
        
        stack.append((sol_parcial.copy(), idx + 1, costo_actual))
        
        nueva_sol = sol_parcial.copy()
        nueva_sol.append(comuna_actual)
        nuevo_costo = costo_actual + problema.costos[comuna_actual]
        stack.append((nueva_sol, idx + 1, nuevo_costo))
    
    return mejor_solucion, mejor_costo

def greedy_propagation_heuristic():
    problema = CentroVacunacion()
    solucion = []
    costo_total = 0
    comunas_por_cubrir = set(problema.todas_comunas)
    
    while comunas_por_cubrir:
        mejor_comuna = None
        mejor_ratio = -1
        mejor_cubiertas = set()
        
        for comuna in problema.todas_comunas:
            if comuna not in solucion:
                cubiertas = {c for c in problema.adyacencias[comuna] + [comuna] if c in comunas_por_cubrir}
                if cubiertas:
                    ratio = len(cubiertas) / problema.costos[comuna]
                    if ratio > mejor_ratio or (ratio == mejor_ratio and problema.costos[comuna] < problema.costos.get(mejor_comuna, float('inf'))):
                        mejor_ratio = ratio
                        mejor_comuna = comuna
                        mejor_cubiertas = cubiertas
        
        if mejor_comuna is None:
            break 
        
        solucion.append(mejor_comuna)
        costo_total += problema.costos[mejor_comuna]
        comunas_por_cubrir -= mejor_cubiertas
    
    return solucion, costo_total

def backtracking_con_greedy_propagation():
    problema = CentroVacunacion()
    mejor_solucion = None
    mejor_costo = float('inf')
    
    solucion_greedy, costo_greedy = greedy_propagation_heuristic()
    if solucion_greedy:
        mejor_solucion = solucion_greedy
        mejor_costo = costo_greedy
    
    stack = []
    stack.append(([], 0, set(problema.todas_comunas), 0)) 
    
    while stack:
        sol_parcial, idx, comunas_restantes, costo_actual = stack.pop()
        
        if not comunas_restantes:
            if costo_actual < mejor_costo:
                mejor_solucion = sol_parcial.copy()
                mejor_costo = costo_actual
            continue
        
        if idx >= len(problema.todas_comunas) or costo_actual >= mejor_costo:
            continue
        
        comuna_actual = problema.todas_comunas[idx]
        
        stack.append((sol_parcial.copy(), idx + 1, comunas_restantes.copy(), costo_actual))
        
        cubiertas = {c for c in problema.adyacencias[comuna_actual] + [comuna_actual] if c in comunas_restantes}
        if cubiertas:
            nueva_sol = sol_parcial.copy()
            nueva_sol.append(comuna_actual)
            stack.append((
                nueva_sol,
                idx + 1,
                comunas_restantes - cubiertas,
                costo_actual + problema.costos[comuna_actual]
            ))
    
    return mejor_solucion, mejor_costo

def ejecutar_y_comparar():
    print("=== Backtracking Cronológico Iterativo ===")
    inicio = time.time()
    sol_cronologico, costo_cronologico = backtracking_cronologico_iterativo()
    tiempo_cronologico = time.time() - inicio
    print(f"Solución: {sorted(sol_cronologico)}")
    print(f"Costo total: {costo_cronologico}")
    print(f"Tiempo de ejecución: {tiempo_cronologico:.4f} segundos\n")
    
    print("=== Backtracking con Greedy Propagation ===")
    inicio = time.time()
    sol_hibrido, costo_hibrido = backtracking_con_greedy_propagation()
    tiempo_hibrido = time.time() - inicio
    print(f"Solución: {sorted(sol_hibrido)}")
    print(f"Costo total: {costo_hibrido}")
    print(f"Tiempo de ejecución: {tiempo_hibrido:.4f} segundos\n")

if __name__ == "__main__":
    ejecutar_y_comparar()
