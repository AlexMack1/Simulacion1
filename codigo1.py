import random
import matplotlib.pyplot as plt

# Solicitar parámetros iniciales
N = int(input("Ingrese el número de parcelas (N): "))

V = [random.randint(100, 1200) for _ in range(N)]
P = [random.uniform(1.0, 10.0) for _ in range(N)]

num_vehiculos = int(input("Ingrese el número de vehículos de transporte: "))
C = [int(input(f"Ingrese la capacidad máxima de carga del vehículo {i+1} (entre 1000 y 2500): ")) for i in range(num_vehiculos)]

num_trabajadores = int(input("Ingrese el número total de trabajadores: "))
W = 40 * num_trabajadores

# Parámetros del algoritmo genético
POBLACION_SIZE = 100
GENES = "01"
GENERACIONES = 1000
PROBABILIDAD_MUTACION = 0.2

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
    # Seleccionamos dos individuos basados en su aptitud (ruleta)
    weights = [fitness(ind) for ind in poblacion]
    return random.choices(poblacion, weights=weights, k=2)

def crossover(padres):
    punto_cruce = random.randint(1, N-1)
    hijo1 = padres[0][:punto_cruce] + padres[1][punto_cruce:]
    hijo2 = padres[1][:punto_cruce] + padres[0][punto_cruce:]
    return hijo1, hijo2

def mutacion(individuo):
    # Invertimos algunos bits con una probabilidad dada
    return ''.join(g if random.random() > PROBABILIDAD_MUTACION else random.choice(GENES) for g in individuo)

# Algoritmo Genético
poblacion = [individuo_inicial(N) for _ in range(POBLACION_SIZE)]

# Lista para almacenar la mejor aptitud de cada generación
mejores_aptitudes = []

for generacion in range(GENERACIONES):
    nueva_poblacion = []
    
    while len(nueva_poblacion) < POBLACION_SIZE:
        padres = seleccionar_padres(poblacion)
        hijos = crossover(padres)
        nueva_poblacion.append(mutacion(hijos[0]))
        nueva_poblacion.append(mutacion(hijos[1]))
    
    poblacion = nueva_poblacion
    
    # Almacenamos la mejor aptitud de esta generación
    mejor_aptitud_generacion = max([fitness(ind) for ind in poblacion])
    mejores_aptitudes.append(mejor_aptitud_generacion)




# Al final de las generaciones, obtenemos la mejor solución:
mejor_individuo = max(poblacion, key=fitness)
valor_mejor_individuo = fitness(mejor_individuo)

# Gráfica de la evolución de la aptitud
plt.figure(figsize=(12, 6))
plt.plot(mejores_aptitudes)
plt.title("Evolución de la aptitud máxima por generación")
plt.xlabel("Generaciones")
plt.ylabel("Mejor aptitud")
plt.grid(True)

# Indicamos la solución en la gráfica
texto = f"Mejor solución: {mejor_individuo}\nAptitud: {valor_mejor_individuo}"
plt.annotate(texto, xy=(GENERACIONES, valor_mejor_individuo), xycoords='data',
             xytext=(-150, 20), textcoords='offset points',
             arrowprops=dict(arrowstyle="->",
                             connectionstyle="arc3,rad=.2"),
             bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="aliceblue"))

plt.show()

# Explicación sobre la representación de los individuos:
print("\nEXPLICACIÓN:")
print("Cada individuo en nuestra población está representado por una cadena de '0's y '1's.")
print("La longitud de esta cadena es igual al número de parcelas N.")
print("- Un '1' en la posición i significa que la parcela i ha sido seleccionada para la cosecha.")
print("- Un '0' en la posición i significa que la parcela i no ha sido seleccionada para la cosecha.")

# Explicación sobre la aptitud y la interpretación de la solución:
print("\nINTERPRETACIÓN DE LA SOLUCIÓN:")
print(f"La aptitud máxima obtenida es {valor_mejor_individuo}.")
print("Esto significa que, dada la selección óptima de parcelas, la cantidad total de caña de azúcar que puede ser cosechada y transportada sin exceder las restricciones es de", valor_mejor_individuo, "kilogramos.")
parcelas_seleccionadas = [i+1 for i, bit in enumerate(mejor_individuo) if bit == '1']
print("Las parcelas seleccionadas para lograr esta cosecha son:", parcelas_seleccionadas)
