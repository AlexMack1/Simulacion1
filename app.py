import streamlit as st

def main():
    st.title('Selección de Algoritmo')

    algoritmos = {
        'Algoritmo Genético': 'codigo1.py',
        'Recocido Simulado': 'codigo2.py',
        'Enjambre de Partículas (PSO)': 'codigo3.py',
        'Programación Lineal': 'codigo4.py'
    }

    seleccion = st.selectbox('Elige un algoritmo:', list(algoritmos.keys()))

    if st.button('Ejecutar Algoritmo'):
        with open(algoritmos[seleccion], 'r') as file:
            exec(file.read())
        st.experimental_rerun()  # Para refrescar la app una vez que finalice el algoritmo

if __name__ == '__main__':
    main()

