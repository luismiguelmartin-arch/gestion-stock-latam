import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración profesional
st.set_page_config(page_title="Zitro Stock LATAM", layout="wide", page_icon="🎰")

# Estilo CSS personalizado para imitar los colores de tu Excel
st.markdown("""
    <style>
    .metric-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    # Cargamos las 4 tablas principales saltando las filas de encabezado decorativas del Excel
    panel = pd.read_csv("Gestion_Stock_LATAM.xlsx - 🏠 Panel de Control.csv", skiprows=9)
    historico = pd.read_csv("Gestion_Stock_LATAM.xlsx - 📊 Histórico & Propuestas.csv", skiprows=5)
    seguimiento = pd.read_csv("Gestion_Stock_LATAM.xlsx - 📅 Seguimiento Semanal.csv", skiprows=4)
    ordenes = pd.read_csv("Gestion_Stock_LATAM.xlsx - 📋 Registro de Órdenes.csv", skiprows=4)
    return panel, historico, seguimiento, ordenes

try:
    panel, historico, seguimiento, ordenes = load_data()

    # --- NAVEGACIÓN ---
    menu = st.sidebar.radio("Ir a:", ["🏠 Panel de Control", "📈 Histórico y Análisis", "📅 Seguimiento Semanal", "📋 Registro de Órdenes"])

    if menu == "🏠 Panel de Control":
        st.header("Gestión de Stock - Gabinetes PRIME & FANTASY")
        
        # Simulación de KPI's extraídos del CSV (basado en tu fila 'Inventario Disponible')
        # Nota: En una app real, aquí buscaríamos las celdas específicas
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Modelo PRIME")
            st.error("🔴 ESTADO: DÉFICIT ALTO")
            st.metric("Inventario Disponible", "106", delta="-129 vs ROP")
            st.info("💡 Orden Sugerida: 194 unidades")
            
        with col2:
            st.subheader("Modelo FANTASY")
            st.error("🔴 ESTADO: DÉFICIT ALTO")
            st.metric("Inventario Disponible", "31", delta="-77 vs ROP")
            st.info("💡 Orden Sugerida: 99 unidades")

    elif menu == "📈 Histórico y Análisis":
        st.header("Análisis de Ventas y Tendencias")
        # Limpieza rápida del histórico para graficar
        df_hist = historico.head(15) # Filtramos solo la parte de datos reales
        fig = px.bar(df_hist, x='Mes', y=['PRIME\nVentas', 'FANTASY\nVentas'], 
                     title="Histórico de Ventas Mensuales", barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(historico)

    elif menu == "📅 Seguimiento Semanal":
        st.header("Cronograma de Disponibilidad")
        st.write("Proyección de stock físico + tránsitos - pedidos firmes")
        st.dataframe(seguimiento.dropna(how='all', axis=0))

    elif menu == "📋 Registro de Órdenes":
        st.header("Control de Órdenes de Fabricación")
        # Filtro de estado
        estado = st.selectbox("Filtrar por Estado:", ["Todas", "Aprobada", "Pendiente", "En Tránsito", "Recibida"])
        if estado != "Todas":
            df_ord = ordenes[ordenes['Estado\nAprobación'] == estado]
        else:
            df_ord = ordenes
        st.table(df_ord.dropna(subset=['N° Orden']))

except Exception as e:
    st.error(f"Error al configurar la app: {e}")
    st.warning("Asegúrate de que los archivos CSV subidos a GitHub mantienen el nombre original del export de Excel.")
