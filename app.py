import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Zitro Stock LATAM", layout="wide", page_icon="🎰")

# Estilos CSS
st.markdown("""
    <style>
    .metric-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Ahora lee los archivos limpios
    panel = pd.read_csv("panel.csv")
    historico = pd.read_csv("historico.csv")
    seguimiento = pd.read_csv("seguimiento.csv")
    ordenes = pd.read_csv("ordenes.csv")
    return panel, historico, seguimiento, ordenes

try:
    panel, historico, seguimiento, ordenes = load_data()

    menu = st.sidebar.radio("Ir a:", ["🏠 Panel de Control", "📈 Histórico y Análisis", "📅 Seguimiento Semanal", "📋 Registro de Órdenes"])

    if menu == "🏠 Panel de Control":
        st.header("Gestión de Stock - Gabinetes PRIME & FANTASY")
        
        col1, col2 = st.columns(2)
        
        # Extraer datos dinámicamente del CSV para PRIME (Fila 0)
        with col1:
            st.subheader(f"Modelo {panel.iloc[0]['Modelo']}")
            st.error(f"🔴 ESTADO: {panel.iloc[0]['Estado']}")
            st.metric("Inventario Disponible", str(panel.iloc[0]['Inventario_Disponible']))
            st.info(f"💡 Orden Sugerida: {panel.iloc[0]['Orden_Sugerida']} unidades")
            
        # Extraer datos dinámicamente del CSV para FANTASY (Fila 1)
        with col2:
            st.subheader(f"Modelo {panel.iloc[1]['Modelo']}")
            st.error(f"🔴 ESTADO: {panel.iloc[1]['Estado']}")
            st.metric("Inventario Disponible", str(panel.iloc[1]['Inventario_Disponible']))
            st.info(f"💡 Orden Sugerida: {panel.iloc[1]['Orden_Sugerida']} unidades")

    elif menu == "📈 Histórico y Análisis":
        st.header("Análisis de Ventas y Tendencias")
        fig = px.bar(historico, x='Mes', y=['PRIME_Ventas', 'FANTASY_Ventas'], 
                     title="Histórico de Ventas Mensuales", barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(historico, use_container_width=True)

    elif menu == "📅 Seguimiento Semanal":
        st.header("Cronograma de Disponibilidad")
        st.dataframe(seguimiento, use_container_width=True)

    elif menu == "📋 Registro de Órdenes":
        st.header("Control de Órdenes de Fabricación")
        estado = st.selectbox("Filtrar por Estado:", ["Todas"] + list(ordenes['Estado_Aprobacion'].dropna().unique()))
        
        if estado != "Todas":
            df_ord = ordenes[ordenes['Estado_Aprobacion'] == estado]
        else:
            df_ord = ordenes
            
        st.table(df_ord.dropna(subset=['N_Orden']))

except Exception as e:
    st.error(f"Error al cargar la aplicación: {e}")
    st.warning("Verifica que los 4 archivos (panel.csv, historico.csv, seguimiento.csv, ordenes.csv) estén subidos a tu GitHub.")
