import pandas as pd
import scipy.stats
import streamlit as st
import time

# Estas son variables de estado que se conservan cuando Streamlit vuelve a ejecutar este script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('Lanzar una moneda')

# Crear el gráfico de línea
chart = st.line_chart([0.5])

# Función para simular lanzar una moneda
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)  # Lanzamientos de moneda (0 = cruz, 1 = cara)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    # Recorrer cada resultado de los lanzamientos
    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no  # Calcular la media acumulada
        chart.add_rows([mean])  # Actualizar el gráfico
        time.sleep(0.05)  # Pausa para simular el tiempo entre lanzamientos

    return mean

# Interfaz de usuario para ingresar el número de lanzamientos
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

# Ejecutar el experimento al presionar el botón
if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1  # Incrementar el número de experimentos

    mean = toss_coin(number_of_trials)  # Realizar el experimento y obtener la media

    # Evitar agregar filas vacías (con NaN)
    if mean is not None:  # Solo agregar resultados si la media no es None
        # Crear una nueva fila para los resultados
        new_result = pd.DataFrame(data=[[st.session_state['experiment_no'], number_of_trials, mean]],
                                  columns=['no', 'iteraciones', 'media'])

        # Concatenar los resultados nuevos con el DataFrame existente
        st.session_state['df_experiment_results'] = pd.concat([st.session_state['df_experiment_results'], new_result], axis=0)

        # Resetear el índice para mantener un índice secuencial
        st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

# Mostrar los resultados acumulados
st.write(st.session_state['df_experiment_results'])