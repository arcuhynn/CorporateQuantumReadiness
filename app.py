import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# Sección de insights automáticos
st.subheader("📢 Alertas e Insights Automáticos")

# Insight: cantidad de activos con algoritmos de alta vulnerabilidad sin cumplimiento NIST
alto_riesgo = df_filtrado[(df_filtrado['Vulnerabilidad Cuántica'] == 'Alta') & (df_filtrado['Cumple NIST PQC'] != 'Sí')]
if len(alto_riesgo) > 0:
    st.warning(f"⚠️ {len(alto_riesgo)} activos utilizan algoritmos con alta vulnerabilidad cuántica y no cumplen con NIST PQC.")

# Insight: unidades sin ningún cumplimiento completo
unidades_sin_cumplimiento = df_filtrado.groupby('Unidad de Negocio').apply(
    lambda x: ((x['Cumple NIST PQC'] != 'Sí') & (x['Cumple ETSI'] != 'Sí') & (x['Cumple ISO'] != 'Sí')).all()
)
unidades_en_riesgo = unidades_sin_cumplimiento[unidades_sin_cumplimiento].index.tolist()
if unidades_en_riesgo:
    st.error(f"❌ Las siguientes unidades no tienen ningún activo que cumpla completamente con los 3 estándares: {', '.join(unidades_en_riesgo)}")

# Insight positivo
cumplen_todo = df_filtrado[(df_filtrado['Cumple NIST PQC'] == 'Sí') & 
                           (df_filtrado['Cumple ETSI'] == 'Sí') & 
                           (df_filtrado['Cumple ISO'] == 'Sí')]
if len(cumplen_todo) > 0:
    st.success(f"✅ {len(cumplen_todo)} activos cumplen completamente con los 3 estándares de seguridad post-cuántica.")

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

# Timeline de regulaciones relevantes
st.subheader("📅 Timeline de Regulaciones Relevantes")
timeline_df = pd.DataFrame({
    'Fecha': ["2016-05-25", "2019-10-01", "2022-07-05", "2023-11-01", "2025-04-01", "2026-06-01", "2027-01-01"],
    'Evento': [
        "GDPR entra en vigor",
        "ENISA publica directrices PQC",
        "NIST selecciona finalistas PQC",
        "Borradores Kyber y Dilithium",
        "Revisión de GDPR con enfoque IA",
        "Adopción recomendada de PQC en infraestructura crítica",
        "Adopción global esperada de PQC"
    ],
    'Organismo': ["UE", "ENISA", "NIST", "NIST", "UE", "ETSI/ENISA", "Global"]
})
timeline_df['Fecha'] = pd.to_datetime(timeline_df['Fecha'])
timeline_df['Fin'] = timeline_df['Fecha'] + pd.Timedelta(days=10)

fig_timeline = px.timeline(
    timeline_df,
    x_start="Fecha",
    x_end="Fin",
    y="Evento",
    color="Organismo",
    title="Hitos de Regulaciones Clave"
)
fig_timeline.update_yaxes(autorange="reversed")
fig_timeline.update_layout(showlegend=True)
st.plotly_chart(fig_timeline, use_container_width=True)

# Perspectivas Avanzadas
st.subheader("🔍 Perspectivas Avanzadas")

# Sunburst Chart
st.markdown("**🌞 Distribución jerárquica de exposición**")
sunburst_data = df_filtrado.copy()
sunburst_data['count'] = 1
fig_sunburst = px.sunburst(sunburst_data, path=['Algoritmo', 'Unidad de Negocio', 'Vulnerabilidad Cuántica'], values='count')
st.plotly_chart(fig_sunburst, use_container_width=True)

# Radar Chart
st.markdown("**🕸️ Comparativo de cumplimiento por unidad**")
radar_data = df_filtrado.copy()
radar_data['cumple_nist'] = (radar_data['Cumple NIST PQC'] == 'Sí').astype(int) * 100
radar_data['cumple_etsi'] = (radar_data['Cumple ETSI'] == 'Sí').astype(int) * 100
radar_data['cumple_iso'] = (radar_data['Cumple ISO'] == 'Sí').astype(int) * 100
radar_grouped = radar_data.groupby('Unidad de Negocio')[['cumple_nist', 'cumple_etsi', 'cumple_iso']].mean().reset_index()

fig_radar = go.Figure()
for _, row in radar_grouped.iterrows():
    fig_radar.add_trace(go.Scatterpolar(
        r=row[['cumple_nist', 'cumple_etsi', 'cumple_iso']].values,
        theta=['NIST PQC', 'ETSI', 'ISO/IEC'],
        fill='toself',
        name=row['Unidad de Negocio']
    ))
fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True)
st.plotly_chart(fig_radar, use_container_width=True)

# Heatmap
st.markdown("**🔥 Mapa de calor de cumplimiento por unidad**")
heatmap_counts = pd.crosstab(df_filtrado['Unidad de Negocio'], df_filtrado['Cumple NIST PQC'])
fig_heatmap = px.imshow(heatmap_counts, text_auto=True, aspect='auto',
                        labels=dict(x="Cumple NIST PQC", y="Unidad de Negocio", color="Cantidad"),
                        title="Mapa de Calor: Cumplimiento NIST PQC por Unidad")
st.plotly_chart(fig_heatmap, use_container_width=True)

# Espacio para descargar reporte
st.download_button("📥 Descargar reporte ejecutivo (CSV)", data=df_filtrado.to_csv(index=False), file_name="reporte_quantum.csv")
