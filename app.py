import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Configuración de la página
st.set_page_config(page_title="Udemy Analytics Dashboard", layout="wide")

# Estilo de colores (basado en tu notebook)
BG, CARD, TEXT, SUBTEXT = '#0F172A', '#1E2938', '#F8FAFC', '#94A3B8'
ACC, ACC2, WARN = '#38BDF8', '#818CF8', '#F43F5E'

def clean_data(df):
    # 1. Limpiar nombres de columnas (elimina espacios en blanco accidentales)
    df.columns = df.columns.str.strip()
    
    # 2. Limpieza de estudiantes (maneja el texto en ruso del dataset)
    if 'students' in df.columns:
        df['students_clean'] = df['students'].apply(lambda x: int(''.join(c for c in str(x) if c.isdigit())) if any(c.isdigit() for c in str(x)) else 0) [cite: 58, 62]
    
    # 3. Limpieza de rating (convierte comas en puntos)
    if 'rating' in df.columns:
        df['rating_clean'] = df['rating'].astype(str).str.replace(',', '.').astype(float) [cite: 65]
    
    # 4. Eliminar duplicados de forma segura
    if 'title' in df.columns:
        df.drop_duplicates(subset=['title'], inplace=True) [cite: 81]
    else:
        st.error(f"Error: No se encontró la columna 'title'. Columnas detectadas: {list(df.columns)}")
        
    return df

st.title("📊 Análisis de Cursos Udemy")
st.markdown("Dashboard interactivo basado en el análisis de **Melany Quiceno y Natalia Lozano**[cite: 4].")

# Carga de datos
uploaded_file = st.file_uploader("Sube el archivo udemy_courses_data.csv", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = clean_data(df)
    
    # KPIs Principales
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Cursos Totales", len(df)) [cite: 92]
    col2.metric("Precio Mediano", f"${df['price'].median():,.0f}") [cite: 206]
    col3.metric("Rating Promedio", f"{df[df['rating_clean']>0]['rating_clean'].mean():.2f}") [cite: 286]
    col4.metric("Estudiantes (Máx)", f"{df['students_clean'].max()/1e6:.1f}M") [cite: 317]

    st.divider()

    # Gráficos
    tab1, tab2, tab3 = st.tabs(["Mercado y Precios", "Popularidad", "Modelo Predictivo"])

    with tab1:
        c1, c2 = st.columns(2)
        # Distribución de Precios [cite: 183]
        fig1, ax1 = plt.subplots(facecolor=BG)
        ax1.set_facecolor(BG)
        ax1.hist(df['price'], bins=35, color=ACC2, alpha=0.85)
        ax1.set_title("Distribución de Precios", color=TEXT)
        st.pyplot(fig1)

        # Precios por Nivel [cite: 229, 249]
        fig2, ax2 = plt.subplots(facecolor=BG)
        ax2.set_facecolor(BG)
        # (Simplificado para el ejemplo)
        df.boxplot(column='price', by='difficulty_es', ax=ax2)
        st.pyplot(fig2)

    with tab2:
        # Top 10 Cursos [cite: 299, 330]
        top10 = df.nlargest(10, 'students_clean')
        fig3, ax3 = plt.subplots(facecolor=BG)
        ax3.set_facecolor(BG)
        ax3.barh(top10['title'].str[:30], top10['students_clean'], color=ACC)
        ax3.invert_yaxis()
        st.pyplot(fig3)

    with tab3:
        # Lógica del modelo predictivo [cite: 339, 370]
        st.subheader("Predicción de Estudiantes")
        rev_input = st.slider("Número de reseñas", 0, 50000, 1000)
        # Basado en tu coeficiente de 5.44 e intercepto de 5397 [cite: 371, 375]
        prediccion = (5.44 * rev_input) + 5397
        st.write(f"### Estudiantes estimados: {int(prediccion):,}")
