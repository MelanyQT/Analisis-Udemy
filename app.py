import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Udemy Analytics Dashboard", layout="wide")

# Estilos de colores profesionales
BG, CARD, TEXT = '#0F172A', '#1E2938', '#F8FAFC'
ACC, ACC2 = '#38BDF8', '#818CF8'

# 2. FUNCIÓN DE LIMPIEZA ROBUSTA
def clean_data(df):
    # Limpiar espacios en los nombres de las columnas
    df.columns = df.columns.str.strip()
    
    # Limpieza de estudiantes (maneja texto en ruso: "123 456 студента")
    if 'students' in df.columns:
        df['students_clean'] = df['students'].apply(
            lambda x: int(''.join(c for c in str(x) if c.isdigit())) if any(c.isdigit() for c in str(x)) else 0
        )
    
    # Limpieza de rating (de "4,6" a 4.6)
    if 'rating' in df.columns:
        df['rating_clean'] = df['rating'].astype(str).str.replace(',', '.').astype(float)
    
    # Mapeo de dificultad (Ruso -> Español)
    if 'difficulty' in df.columns:
        diff_map = {
            'Все уровни': 'Todos los niveles', 
            'Начальный': 'Principiante', 
            'Средний': 'Intermedio', 
            'Эксперт': 'Experto'
        }
        df['difficulty_es'] = df['difficulty'].map(diff_map).fillna('Otros')
    
    # Eliminar duplicados
    if 'title' in df.columns:
        df.drop_duplicates(subset=['title'], inplace=True)
        
    return df

# 3. INTERFAZ DE USUARIO
st.title("📊 Análisis de Cursos Udemy")
st.markdown("Dashboard interactivo por **Melany Quiceno y Natalia Lozano**.")

uploaded_file = st.file_uploader("Sube el archivo udemy_Datos.csv", type="csv")

if uploaded_file:
    # Detección automática de separador (por si es coma o punto y coma)
    df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
    df = clean_data(df_raw)
    
    # KPIs Principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cursos Totales", f"{len(df):,}")
    with col2:
        st.metric("Precio Mediano", f"${df['price'].median():,.0f}")
    with col3:
        # Solo promediar ratings mayores a 0
        avg_rating = df[df['rating_clean'] > 0]['rating_clean'].mean()
        st.metric("Rating Promedio", f"{avg_rating:.2f}")
    with col4:
        st.metric("Estudiantes (Máx)", f"{df['students_clean'].max()/1e6:.1f}M")

    st.divider()

    # 4. TABS DE VISUALIZACIÓN
    tab1, tab2, tab3 = st.tabs(["📉 Mercado y Precios", "🏆 Popularidad", "🤖 Predicción"])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Distribución de Precios")
            fig1, ax1 = plt.subplots()
            ax1.hist(df['price'], bins=20, color=ACC2, edgecolor='white')
            ax1.set_xlabel("Precio ($)")
            st.pyplot(fig1)
        
        with col_b:
            st.subheader("Precios por Nivel")
            fig2, ax2 = plt.subplots()
            df.boxplot(column='price', by='difficulty_es', ax=ax2, grid=False)
            plt.xticks(rotation=45)
            plt.title("") # Quitar título automático de pandas
            st.pyplot(fig2)

    with tab2:
        st.subheader("Top 10 Cursos con más Estudiantes")
        top10 = df.nlargest(10, 'students_clean')
        fig3, ax3 = plt.subplots()
        ax3.barh(top10['title'].str[:40], top10['students_clean'], color=ACC)
        ax3.invert_yaxis()
        ax3.set_xlabel("Cantidad de Estudiantes")
        st.pyplot(fig3)

    with tab3:
        st.subheader("Simulador Predictivo")
        st.info("Basado en el modelo de Regresión Lineal: Estudiantes = 5.44 * Reseñas + 5397")
        
        num_reviews = st.number_input("Ingresa el número de reseñas esperadas:", min_value=0, value=1000)
        # Ecuación de tu modelo
        prediccion = (5.44 * num_reviews) + 5397
        
        st.success(f"### Estimación: {int(prediccion):,} Estudiantes")

else:
    st.info("Esperando archivo... Por favor sube el CSV para activar el Dashboard.")
