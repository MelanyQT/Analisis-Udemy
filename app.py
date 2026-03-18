import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Udemy Analytics Dashboard", layout="wide")

# Estilos de colores
BG, CARD, TEXT = '#0F172A', '#1E2938', '#F8FAFC'
ACC, ACC2 = '#38BDF8', '#818CF8'

# 2. FUNCIÓN DE LIMPIEZA
def clean_data(df):
    df.columns = df.columns.str.strip()
    if 'students' in df.columns:
        df['students_clean'] = df['students'].apply(
            lambda x: int(''.join(c for c in str(x) if c.isdigit())) if any(c.isdigit() for c in str(x)) else 0
        )
    if 'rating' in df.columns:
        df['rating_clean'] = df['rating'].astype(str).str.replace(',', '.').astype(float)
    if 'difficulty' in df.columns:
        diff_map = {'Все уровни': 'Todos los niveles', 'Начальный': 'Principiante', 'Средний': 'Intermedio', 'Эксперт': 'Experto'}
        df['difficulty_es'] = df['difficulty'].map(diff_map).fillna('Otros')
    if 'title' in df.columns:
        df.drop_duplicates(subset=['title'], inplace=True)
    return df

# 3. LÓGICA DE CARGA AUTOMÁTICA
st.title("📊 Análisis de Cursos Udemy")
st.markdown("Proyecto de **Melany Quiceno y Natalia Lozano**")

# Intentar cargar el archivo directamente desde el repositorio
try:
    # Cambia "udemy_Datos.csv" por el nombre EXACTO de tu archivo en GitHub
    df_raw = pd.read_csv("udemy_Datos.csv", sep=None, engine='python')
    df = clean_data(df_raw)
    st.sidebar.success("✅ Datos cargados automáticamente")
except Exception:
    st.sidebar.warning("⚠️ No se encontró el archivo automático.")
    uploaded_file = st.sidebar.file_uploader("Sube el archivo CSV manualmente:", type="csv")
    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
        df = clean_data(df_raw)
    else:
        st.info("Por favor, sube el archivo CSV en el menú lateral para ver el análisis.")
        st.stop()

# 4. CUERPO DEL DASHBOARD (Se ejecuta solo si hay datos)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Cursos Totales", f"{len(df):,}")
col2.metric("Precio Mediano", f"${df['price'].median():,.0f}")
avg_rating = df[df['rating_clean'] > 0]['rating_clean'].mean()
col3.metric("Rating Promedio", f"{avg_rating:.2f}")
col4.metric("Estudiantes (Máx)", f"{df['students_clean'].max()/1e6:.1f}M")

st.divider()

tab1, tab2, tab3 = st.tabs(["📉 Mercado", "🏆 Popularidad", "🤖 Predicción"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Distribución de Precios")
        fig1, ax1 = plt.subplots()
        ax1.hist(df['price'], bins=20, color=ACC2)
        st.pyplot(fig1)
    with c2:
        st.subheader("Precios por Nivel")
        fig2, ax2 = plt.subplots()
        df.boxplot(column='price', by='difficulty_es', ax=ax2)
        plt.xticks(rotation=45)
        st.pyplot(fig2)

with tab2:
    st.subheader("Top 10 Cursos")
    top10 = df.nlargest(10, 'students_clean')
    fig3, ax3 = plt.subplots()
    ax3.barh(top10['title'].str[:40], top10['students_clean'], color=ACC)
    ax3.invert_yaxis()
    st.pyplot(fig3)

with tab3:
    st.subheader("Simulador de Demanda")
    num_rev = st.slider("Número de reseñas:", 0, 20000, 1000)
    pred = (5.44 * num_rev) + 5397
    st.success(f"### Estudiantes estimados: {int(pred):,}")
