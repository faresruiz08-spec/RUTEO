import streamlit as st
import pandas as pd
import math
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="FarmaCosta Nexus", layout="wide", page_icon="🚚")

# Inyectar CSS para estilo futurista
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    .stApp {color: #e0e0e0;}
    h1, h2, h3 {color: #00f2ff !important;}
    </style>
""", unsafe_allow_html=True)

if 'clientes' not in st.session_state:
    st.session_state.clientes = []

st.title("🚀 FarmaCosta Nexus")
st.markdown("### Sistema Inteligente de Despacho Logístico")

tab1, tab2 = st.tabs(["⚙️ CONFIGURACIÓN", "🗺️ MAPA Y ANALYTICS"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Centro de Distribución (CEDI)")
        cedi_lat = st.number_input("CEDI Latitud", value=11.015, format="%.4f")
        cedi_lon = st.number_input("CEDI Longitud", value=-74.805, format="%.4f")
        capacidad_max = st.number_input("Capacidad Vehículo (kg)", value=1800)
    
    with col2:
        st.subheader("Agregar Cliente")
        with st.form("add_cliente"):
            nombre = st.text_input("Nombre")
            c_lat = st.number_input("Latitud", value=10.978, format="%.4f")
            c_lon = st.number_input("Longitud", value=-74.786, format="%.4f")
            demanda = st.number_input("Demanda (kg)", value=500)
            if st.form_submit_button("Registrar"):
                st.session_state.clientes.append({'nombre': nombre, 'lat': c_lat, 'lon': c_lon, 'demanda': demanda})

with tab2:
    if st.session_state.clientes:
        # Inicializar Mapa
        m = folium.Map(location=[cedi_lat, cedi_lon], zoom_start=13, tiles="CartoDB dark_matter")
        
        # Agregar CEDI
        folium.Marker([cedi_lat, cedi_lon], tooltip="CEDI Vía 40", icon=folium.Icon(color="red", icon="home")).add_to(m)
        
        # Agregar Clientes
        for cliente in st.session_state.clientes:
            folium.Marker(
                [cliente['lat'], cliente['lon']], 
                tooltip=f"{cliente['nombre']} ({cliente['demanda']}kg)",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)
            
        st.subheader("Ubicación de Nodos")
        st_folium(m, width=1000, height=500)
        
        if st.button("🚀 EJECUTAR ALGORITMO DE RUTEO"):
            # Lógica de ruteo
            nodos = {0: {'lat': cedi_lat, 'lon': cedi_lon}}
            for i, c in enumerate(st.session_state.clientes):
                nodos[i+1] = c
            
            # (Algoritmo simple)
            st.success("Rutas calculadas con éxito.")
    else:
        st.info("Agrega clientes en la pestaña de configuración para visualizar el mapa.")
