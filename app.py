import streamlit as st

def modelo1():
    # Aquí va todo el código adaptado a Streamlit del primer modelo/algoritmo.
    # ...
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
