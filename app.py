import streamlit as st

def modelo1():
    import streamlit as st
import random
import matplotlib.pyplot as plt

# Configuración inicial
st.title("Optimización de Cosecha con Algoritmo Genético")
st.write("Ajusta los parámetros y ejecuta el algoritmo genético para maximizar la cosecha.")

# Entradas
N = st.sidebar.slider("Número de parcelas (N)", 1, 100, 10)

V = [random.randint(100, 1200) for _ in range(N)]
P = [random.uniform(1.0, 10.0) for _ in range(N)]

num_vehiculos = st.sidebar.slider("Número de vehículos de transporte", 1, 10, 1)
C = [st.sidebar.slider(f"Capacidad máxima de carga del vehículo {i+1}", 1000, 2500, 1500) for i in range(num_vehiculos)]

num_trabajadores = st.sidebar.slider("Número total de trabajadores", 1, 100, 10)
W = 40 * num_trabajadores

# Parámetros del algoritmo genético
POBLACION_SIZE = 100
GENES = "01"
GENERACIONES = st.sidebar.slider("Número de generaciones", 100, 5000, 1000)
PROBABILIDAD_MUTACION = st.sidebar.slider("Probabilidad de mutación", 0.0, 1.0, 0.2)

def individuo_inicial(n):
    return ''.join(random.choice(GENES) for _ in range(n))

def fitness(individuo):
    # Evaluamos cuánta caña de azúcar se cosecha y si cumple con las restricciones
    total_valor = sum(V[i] if individuo[i] == '1' else 0 for i in range(N))
    total_peso = sum(P[i] if individuo[i] == '1' else 0 for i in range(N))
    
    # Verificamos restricciones
    if total_peso > W or total_valor > min(C):
        return 0
    
    return total_valor

def seleccionar_padres(poblacion):
    weights = [fitness(ind) for ind in poblacion]
    return random.choices(poblacion, weights=weights, k=2)

def crossover(padres):
    punto_cruce = random.randint(1, N-1)
    hijo1 = padres[0][:punto_cruce] + padres[1][punto_cruce:]
    hijo2 = padres[1][:punto_cruce] + padres[0][punto_cruce:]
    return hijo1, hijo2

def mutacion(individuo):
    return ''.join(g if random.random() > PROBABILIDAD_MUTACION else random.choice(GENES) for g in individuo)

# Algoritmo Genético
if st.button("Ejecutar Algoritmo Genético"):
    poblacion = [individuo_inicial(N) for _ in range(POBLACION_SIZE)]
    mejores_aptitudes = []

    for generacion in range(GENERACIONES):
        nueva_poblacion = []

        while len(nueva_poblacion) < POBLACION_SIZE:
            padres = seleccionar_padres(poblacion)
            hijos = crossover(padres)
            nueva_poblacion.append(mutacion(hijos[0]))
            nueva_poblacion.append(mutacion(hijos[1]))

        poblacion = nueva_poblacion
        mejor_aptitud_generacion = max([fitness(ind) for ind in poblacion])
        mejores_aptitudes.append(mejor_aptitud_generacion)

    mejor_individuo = max(poblacion, key=fitness)
    valor_mejor_individuo = fitness(mejor_individuo)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(mejores_aptitudes)
    ax.set_title("Evolución de la aptitud máxima por generación")
    ax.set_xlabel("Generaciones")
    ax.set_ylabel("Mejor aptitud")
    ax.grid(True)
    texto = f"Mejor solución: {mejor_individuo}\nAptitud: {valor_mejor_individuo}"
    ax.annotate(texto, xy=(GENERACIONES, valor_mejor_individuo), xycoords='data',
                 xytext=(-150, 20), textcoords='offset points',
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),
                 bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="aliceblue"))
    st.pyplot(fig)

    st.subheader("Explicación:")
    st.write("Cada individuo en nuestra población está representado por una cadena de '0's y '1's.")
    st.write("La longitud de esta cadena es igual al número de parcelas N.")
    st.write("- Un '1' en la posición i significa que la parcela i ha sido seleccionada para la cosecha.")
    st.write("- Un '0' en la posición i significa que la parcela i no ha sido seleccionada para la cosecha.")
    
    st.subheader("Interpretación de la solución:")
    st.write(f"La aptitud máxima obtenida es {valor_mejor_individuo}.")
    st.write("Esto significa que, dada la selección óptima de parcelas, la cantidad total de caña de azúcar que puede ser cosechada y transportada sin exceder las restricciones es de", valor_mejor_individuo, "kilogramos.")
    parcelas_seleccionadas = [i+1 for i, bit in enumerate(mejor_individuo) if bit == '1']
    st.write("Las parcelas seleccionadas para lograr esta cosecha son:", parcelas_seleccionadas)
    st.write("Resultados del Modelo 1")



def modelo2():
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
        
    st.write("Resultados del Modelo 2")

def modelo3():
    # Aquí va todo el código adaptado a Streamlit del tercer modelo/algoritmo.
    # ...
    st.write("Resultados del Modelo 3")

def modelo4():
    # Aquí va todo el código adaptado a Streamlit del cuarto modelo/algoritmo.
    # ...
    st.write("Resultados del Modelo 4")

def main():
    st.title("Selección de Modelo/Algoritmo")

    # Crear un desplegable con los modelos/algoritmos disponibles.
    opcion = st.selectbox(
        'Seleccione el modelo o algoritmo que desea ejecutar:',
        ('Modelo 1', 'Modelo 2', 'Modelo 3', 'Modelo 4')
    )

    if st.button("Ejecutar"):
        if opcion == 'Modelo 1':
            modelo1()
        elif opcion == 'Modelo 2':
            modelo2()
        elif opcion == 'Modelo 3':
            modelo3()
        elif opcion == 'Modelo 4':
            modelo4()

if __name__ == '__main__':
    main()
