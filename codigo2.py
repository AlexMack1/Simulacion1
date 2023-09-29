import numpy as np
import random
import math
import matplotlib.pyplot as plt

# Inicialización del problema basado en la entrada del usuario
def init_problem_from_user():
    N = int(input("Ingrese el número de parcelas (N): "))

    # Generando las parcelas
    Vi = np.random.randint(100, 1201, size=N)  # Valor de caña de azúcar por parcela
    Pi = np.random.uniform(1.0, 10.1, size=N)  # Tiempo necesario para cosechar
    
    num_vehiculos = int(input("Ingrese el número de vehículos de transporte: "))
    capacities = []
    for i in range(num_vehiculos):
        capacity = int(input(f"Ingrese la capacidad máxima de carga del vehículo {i+1} (entre 1000 y 2500): "))
        capacities.append(capacity)

    C = sum(capacities)  # Suma total de capacidades de todos los vehículos

    num_trabajadores = int(input("Ingrese el número total de trabajadores: "))
    W = num_trabajadores * 40  # Total de horas de trabajo disponibles
    
    return Vi, Pi, C, W

# Función de Aptitud (Fitness)
def fitness_calculation(solution, Vi, Pi, C, W):
    total_valor = np.sum(Vi * solution)
    total_peso = np.sum(Pi * solution)
    
    # Verificando restricciones
    if total_valor > C or total_peso > W:
        return -1  # Solución no válida
    return total_valor  # Retornamos el total de caña recolectada

# Generación de solución inicial
def gen_initial_solution(N):
    return np.random.randint(0, 2, size=N)  # Cosechamos o no cada parcela (1 o 0)

# Generación de solución vecina
def generate_neighbor(solution):
    new_solution = solution.copy()
    index = random.randint(0, len(solution)-1)
    new_solution[index] = 1 - new_solution[index]  # Cambiamos el estado de la parcela
    return new_solution

def simulated_annealing(Vi, Pi, C, W, temp, cooling_factor, iterations):
    current_solution = gen_initial_solution(len(Vi))
    current_value = fitness_calculation(current_solution, Vi, Pi, C, W)
    
    best_solution = current_solution
    best_value = current_value
    
    # Guardar la evolución del fitness en cada iteración
    fitness_evolution = []
    
    for i in range(iterations):
        neighbor = generate_neighbor(current_solution)
        neighbor_value = fitness_calculation(neighbor, Vi, Pi, C, W)
        
        if neighbor_value > current_value:
            current_solution, current_value = neighbor, neighbor_value
            if neighbor_value > best_value:
                best_solution, best_value = neighbor, neighbor_value
        else:
            delta = neighbor_value - current_value
            probability = math.exp(delta / temp)
            if random.random() < probability:
                current_solution, current_value = neighbor, neighbor_value
        
        temp *= cooling_factor
        
        # Añadir el mejor valor actual a la lista de evolución
        fitness_evolution.append(best_value)
    
    return best_solution, best_value, fitness_evolution

def interpret_results(best_solution, best_value, Vi, Pi, C, W):
    total_peso = np.sum(Pi * best_solution)
    num_parcelas_cosechadas = np.sum(best_solution)
    
    print("\nInterpretación de los resultados:")
    print("---------------------------------")
    print(f"Se ha decidido cosechar {num_parcelas_cosechadas} de las {len(Vi)} parcelas disponibles.")
    print(f"El valor total obtenido de la caña recolectada es: {best_value}.")
    print(f"Esto se traduce en un tiempo total de cosecha de {total_peso} horas.")
    if total_peso <= W:
        print(f"El tiempo total de cosecha está dentro del límite de trabajo disponible de {W} horas.")
    else:
        print(f"¡Advertencia! El tiempo total de cosecha excede el límite de trabajo disponible de {W} horas.")
    if best_value <= C:
        print(f"El valor total de la caña recolectada está dentro de la capacidad de carga del vehículo de {C}.")
    else:
        print(f"¡Advertencia! El valor total de la caña recolectada excede la capacidad de carga del vehículo de {C}.")
    
    print("\nInterpretación de la gráfica:")
    print("------------------------------")
    print("La gráfica muestra cómo evoluciona el mejor valor de caña recolectada a lo largo de las iteraciones del algoritmo.")
    print("Esto da una idea de cómo el algoritmo explora el espacio de soluciones y cuán rápidamente encuentra una solución óptima o cerca de óptima.")
    print("Si la gráfica muestra una tendencia ascendente, significa que con el tiempo, el algoritmo está encontrando soluciones con valores más altos.")
    print("Si la gráfica se estabiliza, indica que el algoritmo ha encontrado una solución que considera óptima en el contexto de las restricciones.")

# Definición de las variables y ejecución del algoritmo
Vi, Pi, C, W = init_problem_from_user()

temp = 100
cooling_factor = 0.95
iterations = 1000

best_solution, best_value, fitness_evolution = simulated_annealing(Vi, Pi, C, W, temp, cooling_factor, iterations)

# Graficando la evolución del fitness
plt.figure(figsize=(12, 6))
plt.plot(fitness_evolution)
plt.title("Evolución del Fitness en el Recocido Simulado")
plt.xlabel("Iteraciones")
plt.ylabel("Valor de la Función Objetivo (Fitness)")
plt.grid(True)
plt.show()

print("Mejor solución:", best_solution)
print("Mejor valor:", best_value)
interpret_results(best_solution, best_value, Vi, Pi, C, W)
