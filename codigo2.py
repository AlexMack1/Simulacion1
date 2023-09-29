import numpy as np
import random
import math
import streamlit as st

# Función para inicializar el problema desde widgets de Streamlit
def init_problem():
    N = st.sidebar.slider("Número de parcelas (N)", 1, 100, 50)
    num_vehiculos = st.sidebar.slider("Número de vehículos de transporte", 1, 10, 5)
    capacities = st.sidebar.slider("Capacidad máxima de carga de los vehículos", 1000, 2500, 1500)
    num_trabajadores = st.sidebar.slider("Número total de trabajadores", 1, 50, 25)

    # Generando las parcelas
    Vi = np.random.randint(100, 1201, size=N)  # Valor de caña de azúcar por parcela
    Pi = np.random.uniform(1.0, 10.1, size=N)  # Tiempo necesario para cosechar
    C = capacities * num_vehiculos
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
    
    st.subheader("Interpretación de los resultados")
    st.write(f"Se ha decidido cosechar {num_parcelas_cosechadas} de las {len(Vi)} parcelas disponibles.")
    st.write(f"El valor total obtenido de la caña recolectada es: {best_value}.")
    st.write(f"Esto se traduce en un tiempo total de cosecha de {total_peso} horas.")
    if total_peso <= W:
        st.write(f"El tiempo total de cosecha está dentro del límite de trabajo disponible de {W} horas.")
    else:
        st.warning(f"¡Advertencia! El tiempo total de cosecha excede el límite de trabajo disponible de {W} horas.")
    if best_value <= C:
        st.write(f"El valor total de la caña recolectada está dentro de la capacidad de carga del vehículo de {C}.")
    else:
        st.warning(f"¡Advertencia! El valor total de la caña recolectada excede la capacidad de carga del vehículo de {C}.")

if __name__ == '__main__':
    st.title("Optimización de Cosecha con Recocido Simulado")

    Vi, Pi, C, W = init_problem()

    temp = 100
    cooling_factor = 0.95
    iterations = 1000

    if st.button("Ejecutar Recocido Simulado"):
        best_solution, best_value, fitness_evolution = simulated_annealing(Vi, Pi, C, W, temp, cooling_factor, iterations)

        # Graficando la evolución del fitness en Streamlit
        st.line_chart(fitness_evolution, use_container_width=True)

        st.write("Mejor solución:", best_solution)
        st.write("Mejor valor:", best_value)
        interpret_results(best_solution, best_value, Vi, Pi, C, W)
