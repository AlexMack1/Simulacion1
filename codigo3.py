import random
import numpy as np
import streamlit as st

# Parámetros de PSO
NUM_PARTICULAS = 100
GENERACIONES = 1000
W_INERCIA = 0.5
C1 = 1.5
C2 = 1.5

def fitness(particula, V, P, W, C):
    total_valor = sum(V[i] if particula[i] > 0.5 else 0 for i in range(len(V)))
    total_peso = sum(P[i] if particula[i] > 0.5 else 0 for i in range(len(P)))
    
    if total_peso > W or total_valor > min(C):
        return 0
    
    return total_valor

class Particula:
    def __init__(self, dimension):
        self.posicion = [random.uniform(0, 1) for _ in range(dimension)]
        self.velocidad = [random.uniform(-0.5, 0.5) for _ in range(dimension)]
        self.mejor_posicion_personal = list(self.posicion)
        self.mejor_score_personal = fitness(self.posicion)

def optimizar_pso(N, V, P, C, W):
    enjambre = [Particula(N) for _ in range(NUM_PARTICULAS)]
    mejor_posicion_global = random.choice(enjambre).mejor_posicion_personal
    mejor_score_global = fitness(mejor_posicion_global, V, P, W, C)

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
            
            if fitness(particula.posicion, V, P, W, C) > particula.mejor_score_personal:
                particula.mejor_score_personal = fitness(particula.posicion, V, P, W, C)
                particula.mejor_posicion_personal = particula.posicion
                
            if fitness(particula.posicion, V, P, W, C) > mejor_score_global:
                mejor_score_global = fitness(particula.posicion, V, P, W, C)
                mejor_posicion_global = particula.posicion
        
        mejores_aptitudes.append(mejor_score_global)

    return mejor_posicion_global, mejor_score_global, mejores_aptitudes

def main():
    st.title("Optimización de Cosecha con PSO")

    # Solicitar parámetros iniciales con widgets de Streamlit
    N = st.sidebar.slider("Número de parcelas (N)", 1, 100, 50)
    V = [random.randint(100, 1200) for _ in range(N)]
    P = [random.uniform(1.0, 10.0) for _ in range(N)]

    num_vehiculos = st.sidebar.slider("Número de vehículos de transporte", 1, 10, 5)
    C = [st.sidebar.slider(f"Capacidad máxima de carga del vehículo {i+1}", 1000, 2500, 1500) for i in range(num_vehiculos)]

    num_trabajadores = st.sidebar.slider("Número total de trabajadores", 1, 50, 25)
    W = 40 * num_trabajadores

    if st.button("Ejecutar PSO"):
        mejor_posicion_global, mejor_score_global, mejores_aptitudes = optimizar_pso(N, V, P, C, W)

        # Visualizar resultados en Streamlit
        st.line_chart(mejores_aptitudes, use_container_width=True)

        mejor_solucion = [1 if i > 0.5 else 0 for i in mejor_posicion_global]
        st.write(f"Mejor solución encontrada: {mejor_solucion}")
        st.write(f"Aptitud de la mejor solución: {mejor_score_global}")

if __name__ == '__main__':
    main()

