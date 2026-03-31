import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Gestión de Stock LATAM", layout="wide")

st.title("📊 Panel de Control de Inventario - LATAM")

# Función para cargar datos
@st.cache_data
def load_data():
    # Cargamos el archivo (asegúrate de que el nombre coincida en GitHub)
    df = pd.read_csv("LATAM.xlsx - Hoja1.csv")
    # Convertir columna MES a formato fecha si es necesario
    df['MES'] = pd.to_datetime(df['MES'])
    return df

try:
    df = load_data()

    # --- SIDEBAR: Filtros ---
    st.sidebar.header("Filtros")
    anio = st.sidebar.multiselect("Selecciona el Año:", options=df["AÑO"].unique(), default=df["AÑO"].unique())
    df_selection = df[df["AÑO"].isin(anio)]

    # --- KPI's Principales ---
    col1, col2, col3 = st.columns(3)
    with col1:
        total_prime = df_selection["PRIME"].sum()
        st.metric("Total Stock PRIME", f"{total_prime:,.0f} u.")
    with col2:
        total_fantasy = df_selection["FANTASY"].sum()
        st.metric("Total Stock FANTASY", f"{total_fantasy:,.0f} u.")
    with col3:
        st.metric("Registros", len(df_selection))

    # --- GRÁFICOS ---
    st.markdown("""---""")
    
    # Gráfico de evolución temporal
    st.subheader("Evolución de Inventario por Mes")
    df_mensual = df_selection.groupby('MES')[['PRIME', 'FANTASY']].sum().reset_index()
    fig_line = px.line(df_mensual, x='MES', y=['PRIME', 'FANTASY'], 
                       labels={'value': 'Unidades', 'variable': 'Modelo'},
                       markers=True, template="plotly_white")
    st.plotly_chart(fig_line, use_container_width=True)

    # Comparativa de modelos
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Distribución PRIME vs FANTASY")
        fig_pie = px.pie(values=[total_prime, total_fantasy], names=['PRIME', 'FANTASY'], hole=0.4)
        st.plotly_chart(fig_pie)

    with col_right:
        st.subheader("Vista de Datos (Primeras filas)")
        st.dataframe(df_selection.head(10), use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    st.info("Asegúrate de que el archivo CSV esté en la misma carpeta que este script.")
