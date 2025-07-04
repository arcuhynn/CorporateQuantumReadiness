import pandas as pd
import plotly.express as px
import streamlit as st

def resumen_kpis(df):
    total = len(df)
    alta = df[df['Vulnerabilidad Cuántica'] == 'Alta'].shape[0]
    cumplimiento_nist = 100 * (df['Cumple NIST PQC'] == 'Sí').mean()
    cumplimiento_prom = 100 * ((df['Cumple NIST PQC'] == 'Sí') & 
                                (df['Cumple ETSI'] == 'Sí') & 
                                (df['Cumple ISO'] == 'Sí')).mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔢 Total de activos evaluados", total)
    col2.metric("🚨 Algoritmos con alta vulnerabilidad", alta, delta=f"{(alta/total*100):.1f}%")
    col3.metric("✅ Cumplimiento NIST PQC", f"{cumplimiento_nist:.1f}%")
    col4.metric("📊 Cumplimiento completo 3 estándares", f"{cumplimiento_prom:.1f}%")


def tabla_cumplimiento_unidades(df):
    tabla = pd.crosstab(df['Unidad de Negocio'], df['Cumple NIST PQC'])
    st.subheader("📋 Tabla de cumplimiento NIST PQC por unidad")
    st.dataframe(tabla)


def grafico_vulnerabilidad_por_unidad(df):
    resumen = df.groupby(['Unidad de Negocio', 'Vulnerabilidad Cuántica']).size().reset_index(name='Cantidad')
    fig = px.bar(resumen, x='Unidad de Negocio', y='Cantidad', color='Vulnerabilidad Cuántica', 
                 barmode='stack', title="Exposición por Unidad de Negocio")
    st.plotly_chart(fig, use_container_width=True)
