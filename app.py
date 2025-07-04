import streamlit as st
import pandas as pd
import plotly.express as px
from utils import resumen_kpis, tabla_cumplimiento_unidades, grafico_vulnerabilidad_por_unidad

# Configuración general del dashboard
st.set_page_config(page_title="Quantum Readiness Dashboard", layout="wide")
st.title("🔐 Quantum Readiness Dashboard")
st.markdown("""
Este tablero proporciona una vista ejecutiva de los riesgos criptográficos, preparación organizacional y cumplimiento ante la amenaza cuántica.
""")

# Cargar datos desde archivo CSV
@st.cache_data

def cargar_datos():
    return pd.read_csv("demo_quantum_data.csv")

df = cargar_datos()

# Sidebar para filtros o navegación
st.sidebar.header("📊 Filtros")
unidad_seleccionada = st.sidebar.selectbox("Selecciona unidad de negocio", ["Todas"] + sorted(df['Unidad de Negocio'].unique()))
criticidad_seleccionada = st.sidebar.selectbox("Nivel de criticidad", ["Todos"] + sorted(df['Criticidad'].unique()))

# Aplicar filtros
df_filtrado = df.copy()
if unidad_seleccionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado['Unidad de Negocio'] == unidad_seleccionada]
if criticidad_seleccionada != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Criticidad'] == criticidad_seleccionada]

# Sección de KPIs principales
resumen_kpis(df_filtrado)

# Visualización: uso de algoritmos
st.subheader("🔍 Algoritmos criptográficos en uso")
data_crypto = df_filtrado.groupby(['Algoritmo', 'Vulnerabilidad Cuántica'])['Uso (%)'].mean().reset_index()
fig_crypto = px.bar(data_crypto, x='Algoritmo', y='Uso (%)', color='Vulnerabilidad Cuántica',
                    color_discrete_map={'Alta': 'red', 'Media': 'orange', 'Baja': 'green'})
st.plotly_chart(fig_crypto, use_container_width=True)

# Visualización: exposición por unidad de negocio
grafico_vulnerabilidad_por_unidad(df_filtrado)

# Índice de madurez cuántica (simulado)
st.subheader("📈 Índice de preparación organizacional")
st.metric(label="Nivel de madurez (escala 0-5)", value="2.5", delta="+0.5 desde Q1")
st.progress(50)

# Estado de cumplimiento
st.subheader("📋 Cumplimiento frente a estándares")
data_compliance = pd.DataFrame({
    'Estándar': ['NIST PQC', 'ETSI GR ELLF', 'ISO/IEC 23837'],
    'Cumplimiento (%)': [
        100 * (df_filtrado['Cumple NIST PQC'] == 'Sí').mean(),
        100 * (df_filtrado['Cumple ETSI'] == 'Sí').mean(),
        100 * (df_filtrado['Cumple ISO'] == 'Sí').mean()
    ]
})
fig_compliance = px.bar(data_compliance, x='Estándar', y='Cumplimiento (%)', color='Estándar')
st.plotly_chart(fig_compliance, use_container_width=True)

# Tabla de cumplimiento por unidad
tabla_cumplimiento_unidades(df_filtrado)

# Roadmap visual (timeline simplificada)
st.subheader("🗺️ Timeline de acciones estratégicas")
st.markdown("""
- ✅ Q1 2025: Inventario de algoritmos y llaves.
- 🔄 Q2 2025: Evaluación de proveedores.
- ⏳ Q3 2025: Piloto de migración post-cuántica.
- 🧪 Q4 2025: Pruebas con algoritmos lattice-based.
- 🚀 2026: Despliegue inicial en sistemas críticos.
""")

# Espacio para descargar reporte
st.download_button("📥 Descargar reporte ejecutivo (CSV)", data=df_filtrado.to_csv(index=False), file_name="reporte_quantum.csv")
