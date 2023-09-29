import streamlit as st
# Asumiendo que tus algoritmos están en archivos llamados codigo1.py, codigo2.py, etc.
import codigo1
import codigo2
import codigo3
import codigo4

def main():
    st.title("Selección de Algoritmo para Cosecha de Caña")

    algoritmo = st.selectbox("Elija un algoritmo:", ["Algoritmo 1", "Algoritmo 2", "Algoritmo 3", "Algoritmo 4"])
    
    if algoritmo == "Algoritmo 1":
        # Solicitar parámetros específicos del algoritmo 1
        # Por ejemplo:
        N = st.number_input("Ingrese el número de parcelas (N):", min_value=1)
        # (repite para otros parámetros si es necesario)
        if st.button("Ejecutar"):
            result = codigo1.ejecutar(N)  # Asumiendo que 'ejecutar' es una función que haz definido en codigo1.py
            st.write(result)
        
    elif algoritmo == "Algoritmo 2":
        # Repite lo anterior para cada algoritmo
        pass  # (solo un marcador de posición)

    # (repite para los algoritmos 3 y 4)

if __name__ == "__main__":
    main()
