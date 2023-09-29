import random
import matplotlib.pyplot as plt
import numpy as np

# Solicitar parámetros iniciales
N = int(input("Ingrese el número de parcelas (N): "))

V = [random.randint(100, 1200) for _ in range(N)]
P = [random.uniform(1.0, 10.0) for _ in range(N)]

num_vehiculos = int(input("Ingrese el número de vehículos de transporte: "))
C = [int(input(f"Ingrese la capacidad máxima de carga del vehículo {i+1} (entre 1000 y 2500): ")) for i in range(num_vehiculos)]

num_trabajadores = int(input("Ingrese el número total de trabajadores: "))
W = 40 * num_trabajadores

# Parámetros de PSO
NUM_PARTICULAS = 100
GENERACIONES = 1000
W_INERCIA = 0.5
C1 = 1.5
C2 = 1.5

def fitness(particula):
    total_valor = sum(V[i] if particula[i] > 0.5 else 0 for i in range(N))
    total_peso = sum(P[i] if particula[i] > 0.5 else 0 for i in range(N))
    
    if total_peso > W or total_valor > min(C):
        return 0
    
    return total_valor

class Particula:
    def __init__(self, dimension):
        self.posicion = [random.uniform(0, 1) for _ in range(dimension)]
        self.velocidad = [random.uniform(-0.5, 0.5) for _ in range(dimension)]
        self.mejor_posicion_personal = list(self.posicion)
        self.mejor_score_personal = fitness(self.posicion)

enjambre = [Particula(N) for _ in range(NUM_PARTICULAS)]
mejor_posicion_global = random.choice(enjambre).mejor_posicion_personal
mejor_score_global = fitness(mejor_posicion_global)

mejores_aptitudes = []

for generacion in range(GENERACIONES):
    for particula in enjambre:
        for i in range(N):
            r1 = random.random()
            r2 = random.random()
            
            vel_cognitiva = C1 * r1 * (particula.mejor_posicion_personal[i] - particula.posicion[i])
            vel_social = C2 * r2 * (mejor_posicion_global[i] - particula.posicion[i])
            
            particula.velocidad[i] = W_INERCIA * particula.velocidad[i] + vel_cognitiva + vel_social
            particula.posicion[i] = particula.posicion[i] + particula.velocidad[i]
            particula.posicion[i] = np.clip(particula.posicion[i], 0, 1)
        
        if fitness(particula.posicion) > particula.mejor_score_personal:
            particula.mejor_score_personal = fitness(particula.posicion)
            particula.mejor_posicion_personal = particula.posicion
            
        if fitness(particula.posicion) > mejor_score_global:
            mejor_score_global = fitness(particula.posicion)
            mejor_posicion_global = particula.posicion
    
    mejores_aptitudes.append(mejor_score_global)

# Visualizar resultados
plt.figure(figsize=(12, 6))
plt.plot(mejores_aptitudes)
plt.title("Evolución de la aptitud máxima por generación")
plt.xlabel("Generaciones")
plt.ylabel("Mejor aptitud")
plt.grid(True)
plt.show()

mejor_solucion = [1 if i > 0.5 else 0 for i in mejor_posicion_global]
print(f"Mejor solución encontrada: {mejor_solucion}")
print(f"Aptitud de la mejor solución: {mejor_score_global}")
