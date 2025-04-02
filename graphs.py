import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np

# Función para ejecutar el programa y obtener las métricas
def obtener_metricas():
    # Ejecutamos el script y capturamos la salida
    result = subprocess.run(['python3', 'backtracking_con_greedy_propagation.py'], capture_output=True, text=True)
    
    # Definir patrones regex para extraer las métricas
    patrones = {
        'uso_cpu_despues': r'Uso de CPU después: (\d+\.\d+%)',
        'tiempo_cpu_usado': r'Tiempo de CPU usado por el proceso: (\d+\.\d+) segundos',
        'memoria_extra': r'Memoria extra usada por el proceso: (\d+\.\d+) MB'
    }

    # Buscar las métricas en la salida
    metricas = {}
    for key, pattern in patrones.items():
        match = re.search(pattern, result.stdout)
        if match:
            metricas[key] = float(match.group(1).replace('%', '').strip())

    return metricas

# Ejecutamos el programa 20 veces y almacenamos las métricas
metricas_lista = []
for _ in range(20):
    metricas_lista.append(obtener_metricas())

# Extraemos las métricas en listas separadas
uso_cpu_despues = [m['uso_cpu_despues'] for m in metricas_lista]
tiempo_cpu_usado = [m['tiempo_cpu_usado'] for m in metricas_lista]
memoria_extra = [m['memoria_extra'] for m in metricas_lista]

# Calculamos el promedio
promedio_uso_cpu = np.mean(uso_cpu_despues)
promedio_tiempo_cpu = np.mean(tiempo_cpu_usado)
promedio_memoria_extra = np.mean(memoria_extra)

# Colores solicitados
color_uso_cpu = '#94AC5E'
color_tiempo_cpu = '#A827A6'
color_memoria_extra = '#E87970'

# Graficamos los line plots con los colores especificados
plt.figure(figsize=(12, 6))

# Gráfico para Uso de CPU después
plt.subplot(1, 3, 1)
plt.plot(range(1, 21), uso_cpu_despues, label='Uso de CPU después', marker='o', color=color_uso_cpu)
plt.axhline(y=promedio_uso_cpu, color='r', linestyle='-', label=f'Promedio: {promedio_uso_cpu:.2f}%')
plt.title('Uso de CPU después')
plt.xlabel('Ejecutión #')
plt.ylabel('Uso de CPU (%)')
plt.legend()

# Gráfico para Tiempo de CPU usado
plt.subplot(1, 3, 2)
plt.plot(range(1, 21), tiempo_cpu_usado, label='Tiempo de CPU usado', marker='o', color=color_tiempo_cpu)
plt.axhline(y=promedio_tiempo_cpu, color='r', linestyle='-', label=f'Promedio: {promedio_tiempo_cpu:.4f} seg')
plt.title('Tiempo de CPU usado')
plt.xlabel('Ejecutión #')
plt.ylabel('Tiempo de CPU (segundos)')
plt.legend()

# Gráfico para Memoria extra usada
plt.subplot(1, 3, 3)
plt.plot(range(1, 21), memoria_extra, label='Memoria extra usada', marker='o', color=color_memoria_extra)
plt.axhline(y=promedio_memoria_extra, color='r', linestyle='-', label=f'Promedio: {promedio_memoria_extra:.4f} MB')
plt.title('Memoria extra usada')
plt.xlabel('Ejecutión #')
plt.ylabel('Memoria extra (MB)')
plt.legend()

plt.tight_layout()
plt.show()
