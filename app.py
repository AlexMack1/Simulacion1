import streamlit as st

# Imports de los algoritmos
# (Los imports de cada algoritmo deberían ir dentro de su respectiva función para evitar conflictos de nombres)
# ...

# Función que ejecuta el algoritmo genético
def algoritmo_genetico():
    # Aquí iría todo el código relacionado al algoritmo genético

# Función que ejecuta el recocido simulado
def recocido_simulado():
    # Aquí iría todo el código relacionado al recocido simulado

# Aquí agregarías más funciones si tienes otros algoritmos...

# Interfaz principal
def main():
    st.title("Optimización de Cosecha")

    # Seleccionar el algoritmo
    algoritmo = st.selectbox("Elige un algoritmo:", 
                             ["Algoritmo Genético", "Recocido Simulado", "... otros algoritmos ..."])

    # Botón de ejecución
    if st.button("Ejecutar"):
        if algoritmo == "Algoritmo Genético":
            algoritmo_genetico()
        elif algoritmo == "Recocido Simulado":
            recocido_simulado()
        # ... y así para otros algoritmos ...

if __name__ == "__main__":
    main()
