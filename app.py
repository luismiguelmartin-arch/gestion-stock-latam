import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Panel de Control - Stock LATAM", layout="wide")

# Encabezado principal
st.title("GESTIÓN DE STOCK – GABINETES PRIME & FANTASY · LATAM")
st.caption("SOP-LOG-ZITRO-001 · Vigencia: Abril – Junio 2026 | Lead Time: 4 semanas | Nivel de servicio objetivo: 95-98%")
st.markdown("---")

# 2. PARÁMETROS DEL PLAN (ESTÁTICO)
st.subheader("▌ PARÁMETROS DEL PLAN (SOP-LOG-ZITRO-001)")
parametros_data = {
    "Indicador": ["Demanda Semanal Ajustada (+20%)", "Stock de Seguridad (Mínimo)", "Punto de Pedido (ROP)", "Stock Máximo de Almacén"],
    "PRIME": [50, 35, 235, 300],
    "FANTASY": [22, 20, 108, 130]
}
st.dataframe(pd.DataFrame(parametros_data), hide_index=True, use_container_width=True)

st.markdown("---")

# 3. SECCIÓN EDITABLE (ENTRADA MANUAL)
st.subheader("▌ STOCK ACTUAL Y FABRICACIONES PENDIENTES (entrada manual)")
st.info("ℹ️ Modifica los valores a continuación. El sistema calculará automáticamente los indicadores de abajo.")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.write("**Campo**")
    st.write("🔵 Stock Físico Actual")
    st.write("🔵 Fabricaciones Pendientes Aprobadas (en tránsito)")
    st.write("🔴 Pedidos en Firme (comprometidos)")
    st.write("🟡 Presupuesto / Forecast (unidades)")

with col2:
    st.write("**PRIME**")
    sf_prime = st.number_input("Stock Físico PRIME", value=142, step=1, label_visibility="collapsed")
    fab_prime = st.number_input("Fabricaciones PRIME", value=115, step=1, label_visibility="collapsed")
    pedidos_prime = st.number_input("Pedidos PRIME", value=151, step=1, label_visibility="collapsed")
    forecast_prime = st.number_input("Forecast PRIME", value=608, step=1, label_visibility="collapsed")

with col3:
    st.write("**FANTASY**")
    sf_fantasy = st.number_input("Stock Físico FANTASY", value=53, step=1, label_visibility="collapsed")
    fab_fantasy = st.number_input("Fabricaciones FANTASY", value=50, step=1, label_visibility="collapsed")
    pedidos_fantasy = st.number_input("Pedidos FANTASY", value=72, step=1, label_visibility="collapsed")
    forecast_fantasy = st.number_input("Forecast FANTASY", value=252, step=1, label_visibility="collapsed")

# --- LÓGICA DE CÁLCULO ---
# Inventario Disponible
inv_disp_prime = sf_prime + fab_prime - pedidos_prime
inv_disp_fantasy = sf_fantasy + fab_fantasy - pedidos_fantasy

# Funciones de estado
def estado_pedidos(inv, rop, seg):
    if inv <= seg: return "🔴 ALERTA ROJA"
    elif inv <= rop: return "🟠 LANZAR ORDEN"
    elif inv > rop * 1.5: return "⚠️ SOBRE MÁXIMO"
    else: return "✅ OK / CUBIERTO"

def estado_forecast(inv, forecast):
    diff = inv - forecast
    if diff < -100: return "🔴 DÉFICIT ALTO"
    elif diff < 0: return "🟡 DÉFICIT LEVE"
    else: return "✅ OK / CUBIERTO"

st.markdown("---")

# 4. CÁLCULO INVENTARIO DISPONIBLE (ESTÁTICO/CALCULADO)
st.subheader("▌ CÁLCULO: INVENTARIO DISPONIBLE")
st.caption("Fórmula: Stock Físico + Fabricaciones en Tránsito − Pedidos en Firme")
calculo_data = {
    "Concepto": ["Stock Físico", "(+) Fabricaciones en Tránsito", "(−) Pedidos en Firme", " = Inventario Disponible"],
    "PRIME": [sf_prime, fab_prime, pedidos_prime, inv_disp_prime],
    "FANTASY": [sf_fantasy, fab_fantasy, pedidos_fantasy, inv_disp_fantasy]
}
st.dataframe(pd.DataFrame(calculo_data), hide_index=True, use_container_width=True)

st.markdown("---")

# 5. ANÁLISIS A Y B (ESTÁTICO/CALCULADO)
colA, colB = st.columns(2)

with colA:
    st.subheader("▌ ANÁLISIS A: STOCK vs PEDIDOS FIRME")
    analisis_a_data = {
        "Indicador": [
            "Inventario Disponible", "ROP (Punto de Pedido)", "Stock Máximo", "Stock de Seguridad",
            "Exceso / Déficit vs ROP", "Orden Sugerida (hasta Stock Máx.)", "Estado vs Pedidos Firme"
        ],
        "PRIME": [
            inv_disp_prime, 235, 300, 35,
            inv_disp_prime - 235, 
            max(0, 300 - inv_disp_prime), 
            estado_pedidos(inv_disp_prime, 235, 35)
        ],
        "FANTASY": [
            inv_disp_fantasy, 108, 130, 20,
            inv_disp_fantasy - 108, 
            max(0, 130 - inv_disp_fantasy), 
            estado_pedidos(inv_disp_fantasy, 108, 20)
        ]
    }
    st.dataframe(pd.DataFrame(analisis_a_data), hide_index=True, use_container_width=True)

with colB:
    st.subheader("▌ ANÁLISIS B: STOCK vs FORECAST")
    analisis_b_data = {
        "Indicador": [
            "Inventario Disponible", "Presupuesto / Forecast", "Demanda Semanal (plan)",
            "Semanas de Cobertura (Disp./Dem.Sem.)", "Cobertura vs Forecast (semanas)",
            "Diferencia Stock – Forecast", "Orden Sugerida vs Forecast", "Estado vs Presupuesto"
        ],
        "PRIME": [
            inv_disp_prime, forecast_prime, 50,
            round(inv_disp_prime / 50, 2), round(forecast_prime / 50, 2),
            inv_disp_prime - forecast_prime,
            max(0, forecast_prime - inv_disp_prime),
            estado_forecast(inv_disp_prime, forecast_prime)
        ],
        "FANTASY": [
            inv_disp_fantasy, forecast_fantasy, 22,
            round(inv_disp_fantasy / 22, 2), round(forecast_fantasy / 22, 2),
            inv_disp_fantasy - forecast_fantasy,
            max(0, forecast_fantasy - inv_disp_fantasy),
            estado_forecast(inv_disp_fantasy, forecast_fantasy)
        ]
    }
    st.dataframe(pd.DataFrame(analisis_b_data), hide_index=True, use_container_width=True)

st.markdown("---")

# 6. LEYENDA
st.subheader("▌ LEYENDA DE ESTADOS")
leyenda_col1, leyenda_col2 = st.columns(2)
with leyenda_col1:
    st.write("✅ **OK / CUBIERTO:** Stock suficiente, sin acción inmediata")
    st.write("🟡 **DÉFICIT LEVE / LANZAR ORDEN:** Stock por debajo del ROP o Forecast. Preparar orden.")
    st.write("🟠 **LANZAR ORDEN:** Inventario ≤ Punto de Pedido. Emitir orden inmediata.")
with leyenda_col2:
    st.write("🔴 **ALERTA ROJA:** Stock ≤ Seguridad. Agilizar logística, posible exprés.")
    st.write("🔴 **DÉFICIT ALTO:** Muy por debajo del Forecast.")
    st.write("⚠️ **SOBRE MÁXIMO:** Exceso de stock. Revisar cancelaciones o sobreproducción.")
