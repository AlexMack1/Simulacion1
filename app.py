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
    # Aquí va todo el código adaptado a Streamlit del segundo modelo/algoritmo.
    # ...
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
