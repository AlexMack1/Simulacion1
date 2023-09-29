import streamlit as st

PAGES = {
    "Algoritmo genético": "codigo1.py",
    "Algoritmo de recocido simulado": "codigo2.py",
    "Algoritmo de Enjambre de Partículas (PSO)": "codigo3.py",
    "Utilizando programacion Lineal": "codigo4.py"
}

def main():
    st.title('Menú de algoritmos')
    choice = st.sidebar.radio("Elija un algoritmo:", list(PAGES.keys()))

    # Aquí es donde cargamos y ejecutamos el archivo seleccionado
    with open(PAGES[choice], 'r') as file:
        exec(file.read())

if __name__ == '__main__':
    main()
