import streamlit as st
import pandas as pd
import math
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="FarmaCosta Nexus", layout="wide", page_icon="🚚")

# Inyectar CSS para estilo futurista
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    .stApp {color: #e0e0e0;}
    .metric-card {
        background-color: #1e1e26;
        border: 1px solid #333;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    h1, h2, h3 {color: #00f2ff !important;}
    </style>
""", unsafe_allow_html=True)

if 'clientes' not in st.session_state:
    st.session_state.clientes = []

def calcular_distancia(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111000

st.title("🚀 FarmaCosta Nexus")
st.markdown("### Sistema Inteligente de Despacho Logístico")

# Layout de control principal
tab1, tab2 = st.tabs(["⚙️ CONFIGURACIÓN", "📊 ANALYTICS"])

with tab1:
    col_input1, col_input2 = st.columns([1, 1])
    
    with col_input1:
        st.subheader("Centro de Distribución (CEDI)")
        cedi_lat = st.number_input("CEDI Latitud", value=11.015, format="%.4f")
        cedi_lon = st.number_input("CEDI Longitud", value=-74.805, format="%.4f")
        capacidad_max = st.number_input("Capacidad Vehículo (kg)", value=1800)

    with col_input2:
        st.subheader("Ingreso de Clientes")
        with st.form("add_cliente_form"):
            nombre = st.text_input("Nombre Cliente")
            c_lat = st.number_input("Latitud Cliente", value=10.978, format="%.4f")
            c_lon = st.number_input("Longitud Cliente", value=-74.786, format="%.4f")
            demanda = st.number_input("Demanda (kg)", value=500)
            if st.form_submit_button("Añadir al Nodo"):
                st.session_state.clientes.append({'nombre': nombre, 'lat': c_lat, 'lon': c_lon, 'demanda': demanda})
    
    if st.button("🚀 INICIAR OPTIMIZACIÓN"):
        st.session_state.run_opt = True
    else:
        st.session_state.run_opt = False

with tab2:
    if st.session_state.run_opt and st.session_state.clientes:
        nodos_dict = {0: {'nombre': 'CEDI', 'lat': cedi_lat, 'lon': cedi_lon, 'demanda': 0}}
        for i, c in enumerate(st.session_state.clientes):
            nodos_dict[i+1] = c
        
        # Algoritmo (Lógica de algoritmo_de_ruteo_farmacosta.py adaptada)
        pendientes = list(range(1, len(st.session_state.clientes) + 1))
        rutas = []
        while pendientes:
            ruta = [0]
            carga = 0
            for c in list(pendientes):
                if carga + nodos_dict[c]['demanda'] <= capacidad_max:
                    ruta.append(c)
                    carga += nodos_dict[c]['demanda']
                    pendientes.remove(c)
            ruta.append(0)
            rutas.append({'nodos': ruta, 'carga': carga})
        
        # Dashboard KPIs
        m1, m2, m3 = st.columns(3)
        m1.metric("Vehículos Activos", len(rutas))
        m2.metric("Clientes Atendidos", len(st.session_state.clientes))
        m3.metric("Capacidad Promedio", f"{sum([r['carga'] for r in rutas])/len(rutas):.0f} kg")

        # Visualización Interactiva con Plotly
        fig = go.Figure()
        
        for i, r in enumerate(rutas):
            lats = [nodos_dict[n]['lat'] for n in r['nodos']]
            lons = [nodos_dict[n]['lon'] for n in r['nodos']]
            fig.add_trace(go.Scatter(x=lons, y=lats, mode='lines+markers', name=f'Vehículo {i+1}'))
        
        fig.add_trace(go.Scatter(x=[cedi_lon], y=[cedi_lat], mode='markers', name='CEDI', marker=dict(size=15, color='red')))
        
        fig.update_layout(
            paper_bgcolor="#0e1117", 
            plot_bgcolor="#0e1117",
            font_color="white",
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Configura tus nodos y presiona 'INICIAR OPTIMIZACIÓN' para ver los resultados.")
