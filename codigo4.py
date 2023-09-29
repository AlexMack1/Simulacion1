import numpy as np
import pulp
import random
import matplotlib.pyplot as plt

# Inicialización del problema con entrada del usuario
def init_problem_from_user(N):
    # Generando las parcelas
    Vi = [random.randint(100, 1200) for _ in range(N)]
    Pi = [random.uniform(1.0, 10.0) for _ in range(N)]

    # Vehículos de transporte
    num_vehiculos = int(input("Ingrese el número de vehículos de transporte: "))
    C = [int(input(f"Ingrese la capacidad máxima de carga del vehículo {i+1} (entre 1000 y 2500): ")) for i in range(num_vehiculos)]
    
    # Capacidad de trabajo total
    num_trabajadores = int(input("Ingrese el número total de trabajadores: "))
    W = 40 * num_trabajadores  # Total de horas de trabajo disponibles
    
    return Vi, Pi, sum(C), W

def linear_programming_solution(Vi, Pi, C, W):
    # Definimos el problema
    prob = pulp.LpProblem("CosechaDeCania", pulp.LpMaximize) # Maximizacion

    # Definimos las variables de decisión
    x = [pulp.LpVariable(f"x_{i}", cat="Binary") for i in range(len(Vi))]

    # Función objetivo
    prob += pulp.lpSum([Vi[i] * x[i] for i in range(len(Vi))]), "ValorTotalCosecha"

    # Restricciones
    prob += pulp.lpSum([Vi[i] * x[i] for i in range(len(Vi))]) <= C, "RestriccionCarga"
    prob += pulp.lpSum([Pi[i] * x[i] for i in range(len(Vi))]) <= W, "RestriccionTrabajo"

    # Resolvemos el problema
    prob.solve()

    # Obtenemos la solución
    solution = [int(pulp.value(var)) for var in x]
    value = pulp.value(prob.objective)

    return solution, value

# Graficar la región factible y el punto óptimo
def plot_feasible_region_and_optimal_point(Vi, Pi, C, W, solution):
    plt.figure(figsize=(10, 10))

    # Línea vertical para representar la restricción de carga
    plt.axvline(x=C, color='blue', linestyle='--', label="Restricción de carga")

    # Línea horizontal para representar la restricción de trabajo
    plt.axhline(y=W, color='orange', linestyle='--', label="Restricción de trabajo")

    # Diagrama de dispersión para las sumas acumuladas de Vi y Pi
    accumulated_Vi = np.cumsum(Vi)
    accumulated_Pi = np.cumsum(Pi)
    plt.scatter(accumulated_Vi, accumulated_Pi, color='green', marker='o', label="Suma acumulada de parcelas")

    # Resaltar el punto óptimo
    optimal_Vi = sum([Vi[i] for i, isSelected in enumerate(solution) if isSelected])
    optimal_Pi = sum([Pi[i] for i, isSelected in enumerate(solution) if isSelected])
    plt.scatter(optimal_Vi, optimal_Pi, color='red', s=100, marker='*', label="Punto óptimo")

    plt.title("Visualización de restricciones y punto óptimo")
    plt.xlabel("Suma de Vi")
    plt.ylabel("Suma de Pi")
    plt.legend()
    plt.grid(True)
    plt.show()

# Solicitamos los parámetros iniciales
N = int(input("Ingrese el número de parcelas (N): "))
Vi, Pi, C, W = init_problem_from_user(N)

solution, value = linear_programming_solution(Vi, Pi, C, W)
print("\nSolución óptima:", solution)
print("Valor óptimo:", value)

# Mostrar la visualización con el punto óptimo y restricciones
plot_feasible_region_and_optimal_point(Vi, Pi, C, W, solution)
