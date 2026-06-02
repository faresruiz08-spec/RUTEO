import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt

# Configuración de página
st.set_page_config(page_title="FarmaCosta Ruteo", layout="wide")

st.title("🚚 Sistema de Ruteo Inteligente - FarmaCosta S.A.")

# --- BARRA LATERAL: ENTRADA DE DATOS ---
st.sidebar.header("Configuración de Nodos")

# CEDI
st.sidebar.subheader("Centro de Distribución (CEDI)")
cedi_lat = st.sidebar.number_input("CEDI Latitud", value=11.015, format="%.4f")
cedi_lon = st.sidebar.number_input("CEDI Longitud", value=-74.805, format="%.4f")

# Clientes
st.sidebar.subheader("Gestión de Clientes")
if 'clientes' not in st.session_state:
    st.session_state.clientes = []

with st.sidebar.form("add_cliente"):
    nombre = st.text_input("Nombre Cliente")
    lat = st.number_input("Latitud", value=10.978, format="%.4f")
    lon = st.number_input("Longitud", value=-74.786, format="%.4f")
    demanda = st.number_input("Demanda (kg)", value=500)
    if st.form_submit_button("Agregar Cliente"):
        st.session_state.clientes.append({'nombre': nombre, 'lat': lat, 'lon': lon, 'demanda': demanda})

# --- LÓGICA DE RUTEO ---
CAPACIDAD_MAX = st.sidebar.number_input("Capacidad Vehículo (kg)", value=1800)

def calcular_distancia(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111000

if st.button("Ejecutar Optimización de Rutas"):
    if not st.session_state.clientes:
        st.error("Agregue al menos un cliente.")
    else:
        # Estructurar nodos
        nodos_dict = {0: {'nombre': 'CEDI', 'lat': cedi_lat, 'lon': cedi_lon, 'demanda': 0}}
        for i, c in enumerate(st.session_state.clientes):
            nodos_dict[i+1] = c
        
        # Algoritmo sencillo (Greedy)
        pendientes = list(range(1, len(st.session_state.clientes) + 1))
        rutas = []
        while pendientes:
            ruta = [0]
            carga = 0
            for c in list(pendientes):
                if carga + nodos_dict[c]['demanda'] <= CAPACIDAD_MAX:
                    ruta.append(c)
                    carga += nodos_dict[c]['demanda']
                    pendientes.remove(c)
            ruta.append(0)
            rutas.append({'nodos': ruta, 'carga': carga})
        
        # Mostrar Resultados
        st.subheader("Resultados del Despacho")
        cols = st.columns(len(rutas))
        for i, r in enumerate(cols):
            with r:
                st.write(f"**Vehículo {i+1}**")
                st.write(f"Carga: {rutas[i]['carga']} kg")
        
        # Mapa
        fig, ax = plt.subplots()
        for i, r in enumerate(rutas):
            lats = [nodos_dict[n]['lat'] for n in r['nodos']]
            lons = [nodos_dict[n]['lon'] for n in r['nodos']]
            ax.plot(lons, lats, marker='o', label=f'Vehículo {i+1}')
        ax.scatter(cedi_lon, cedi_lat, c='red', s=100, label='CEDI')
        st.pyplot(fig)
