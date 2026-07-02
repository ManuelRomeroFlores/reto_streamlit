# =============================================================================
# Reto: Conociendo el desempeño de los colaboradores del Área de Marketing
#        de Socialize your knowledge
# Aplicación web desarrollada con Python + Streamlit
# =============================================================================

# ----------------------- Librerías necesarias -------------------------------
import streamlit as st          # Framework para construir la aplicación web
import pandas as pd             # Manipulación y análisis de la base de datos
import plotly.express as px     # Gráficos interactivos

# ----------------------- Configuración general de la página -----------------
st.set_page_config(
    page_title="Desempeño de colaboradores | Socialize your knowledge",
    layout="wide",
)

# ----------------------- Carga y limpieza de la base de datos ---------------
@st.cache_data
def cargar_datos():
    df = pd.read_csv("Employee_data.csv")
    # Limpieza: la columna 'gender' contiene espacios extra (ej. 'M ')
    df["gender"] = df["gender"].str.strip()
    # Etiquetas legibles en español para el usuario final
    df["genero"] = df["gender"].map({"M": "Masculino", "F": "Femenino"})
    return df

datos = cargar_datos()

# =============================================================================
# SECCIÓN 1. CÓDIGO PARA DESPLEGAR EL TÍTULO Y LA DESCRIPCIÓN DE LA APLICACIÓN
# =============================================================================
st.title("Análisis del desempeño de los colaboradores")
st.markdown(
    """
    Bienvenido(a) al **cuadro de mando de Socialize your knowledge**.
    Esta aplicación web permite explorar de forma sencilla el desempeño de los
    colaboradores del área de Marketing: filtra por **género**, **puntaje de
    desempeño** y **estado civil**, y analiza los indicadores y gráficos para
    identificar **fortalezas** y **áreas de oportunidad** del equipo.
    """
)

# =============================================================================
# SECCIÓN 2. CÓDIGO PARA DESPLEGAR EL LOGOTIPO DE LA EMPRESA
# =============================================================================
st.sidebar.image("logo_syk.png", use_container_width=True)

# =============================================================================
# APARTADO DE SELECCIÓN DE CONTROLES (FILTROS INTERACTIVOS)
# Se colocan en la barra lateral para mantener limpia la pantalla principal.
# =============================================================================
st.sidebar.header("🎛️ Controles de filtrado")

# -----------------------------------------------------------------------------
# SECCIÓN 3. CÓDIGO PARA INCLUIR UN CONTROL PARA SELECCIONAR EL GÉNERO
# -----------------------------------------------------------------------------
opciones_genero = ["Todos"] + sorted(datos["genero"].unique().tolist())
genero_seleccionado = st.sidebar.selectbox(
    "Selecciona el género del empleado:",
    options=opciones_genero,
)

# -----------------------------------------------------------------------------
# SECCIÓN 4. CÓDIGO PARA INCLUIR UN CONTROL PARA SELECCIONAR EL RANGO DEL
#            PUNTAJE DE DESEMPEÑO
# -----------------------------------------------------------------------------
puntaje_min = int(datos["performance_score"].min())
puntaje_max = int(datos["performance_score"].max())
rango_puntaje = st.sidebar.slider(
    "Selecciona el rango del puntaje de desempeño:",
    min_value=puntaje_min,
    max_value=puntaje_max,
    value=(puntaje_min, puntaje_max),
    step=1,
)

# -----------------------------------------------------------------------------
# SECCIÓN 5. CÓDIGO PARA INCLUIR UN CONTROL PARA SELECCIONAR EL ESTADO CIVIL
# -----------------------------------------------------------------------------
opciones_estado_civil = ["Todos"] + sorted(datos["marital_status"].unique().tolist())
estado_civil_seleccionado = st.sidebar.selectbox(
    "Selecciona el estado civil del empleado:",
    options=opciones_estado_civil,
)

# ----------------------- Aplicación de los filtros ---------------------------
datos_filtrados = datos.copy()

if genero_seleccionado != "Todos":
    datos_filtrados = datos_filtrados[datos_filtrados["genero"] == genero_seleccionado]

datos_filtrados = datos_filtrados[
    (datos_filtrados["performance_score"] >= rango_puntaje[0])
    & (datos_filtrados["performance_score"] <= rango_puntaje[1])
]

if estado_civil_seleccionado != "Todos":
    datos_filtrados = datos_filtrados[
        datos_filtrados["marital_status"] == estado_civil_seleccionado
    ]

# ----------------------- Indicadores clave (KPIs) ----------------------------
st.header("📌 Indicadores clave del personal filtrado")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Colaboradores", len(datos_filtrados))
col2.metric("Desempeño promedio", f"{datos_filtrados['performance_score'].mean():.2f}" if len(datos_filtrados) else "—")
col3.metric("Horas mensuales promedio", f"{datos_filtrados['average_work_hours'].mean():,.0f}" if len(datos_filtrados) else "—")
col4.metric("Satisfacción promedio", f"{datos_filtrados['satisfaction_level'].mean():.2f}" if len(datos_filtrados) else "—")

# Advertencia si los filtros no arrojan resultados
if datos_filtrados.empty:
    st.warning("⚠️ No hay colaboradores que cumplan con los filtros seleccionados. Ajusta los controles de la barra lateral.")
    st.stop()

# =============================================================================
# APARTADO DE GRÁFICAS Y VISUALIZACIONES DE DESEMPEÑO
# =============================================================================
st.header("📈 Visualizaciones de desempeño")

fila1_col1, fila1_col2 = st.columns(2)
fila2_col1, fila2_col2 = st.columns(2)

# -----------------------------------------------------------------------------
# SECCIÓN 6. CÓDIGO PARA VISUALIZAR LA DISTRIBUCIÓN DE LOS PUNTAJES DE
#            DESEMPEÑO DE LOS EMPLEADOS
# -----------------------------------------------------------------------------
with fila1_col1:
    st.subheader("Distribución de los puntajes de desempeño")
    grafico_distribucion = px.histogram(
        datos_filtrados,
        x="performance_score",
        color="performance_score_desc",
        labels={
            "performance_score": "Puntaje de desempeño",
            "performance_score_desc": "Descripción",
        },
        color_discrete_sequence=px.colors.qualitative.Prism,
    )
    grafico_distribucion.update_layout(yaxis_title="Número de empleados", bargap=0.2)
    st.plotly_chart(grafico_distribucion, use_container_width=True)

# -----------------------------------------------------------------------------
# SECCIÓN 7. CÓDIGO PARA VISUALIZAR EL PROMEDIO DE HORAS TRABAJADAS POR EL
#            GÉNERO DEL EMPLEADO
# -----------------------------------------------------------------------------
with fila1_col2:
    st.subheader("Promedio de horas trabajadas por género")
    horas_por_genero = (
        datos_filtrados.groupby("genero", as_index=False)["average_work_hours"].mean()
    )
    grafico_horas_genero = px.bar(
        horas_por_genero,
        x="genero",
        y="average_work_hours",
        color="genero",
        text_auto=".0f",
        labels={
            "genero": "Género",
            "average_work_hours": "Promedio de horas mensuales",
        },
        color_discrete_sequence=["#009691", "#143C46"],
    )
    st.plotly_chart(grafico_horas_genero, use_container_width=True)

# -----------------------------------------------------------------------------
# SECCIÓN 8. CÓDIGO PARA VISUALIZAR LA EDAD DE LOS EMPLEADOS CON RESPECTO AL
#            SALARIO
# -----------------------------------------------------------------------------
with fila2_col1:
    st.subheader("Edad de los empleados vs. salario")
    grafico_edad_salario = px.scatter(
        datos_filtrados,
        x="age",
        y="salary",
        color="genero",
        hover_data=["name_employee", "position"],
        labels={"age": "Edad", "salary": "Salario anual (USD)", "genero": "Género"},
        color_discrete_sequence=["#009691", "#143C46"],
    )
    st.plotly_chart(grafico_edad_salario, use_container_width=True)

# -----------------------------------------------------------------------------
# SECCIÓN 9. CÓDIGO PARA VISUALIZAR LA RELACIÓN DEL PROMEDIO DE HORAS
#            TRABAJADAS VERSUS EL PUNTAJE DE DESEMPEÑO
# -----------------------------------------------------------------------------
with fila2_col2:
    st.subheader("Promedio de horas trabajadas vs. puntaje de desempeño")
    horas_por_puntaje = (
        datos_filtrados.groupby("performance_score", as_index=False)[
            "average_work_hours"
        ].mean()
    )
    grafico_horas_desempeno = px.bar(
        horas_por_puntaje,
        x="performance_score",
        y="average_work_hours",
        color="performance_score",
        text_auto=".0f",
        labels={
            "performance_score": "Puntaje de desempeño",
            "average_work_hours": "Promedio de horas mensuales",
        },
        color_continuous_scale="Teal",
    )
    grafico_horas_desempeno.update_layout(coloraxis_showscale=False)
    grafico_horas_desempeno.update_xaxes(dtick=1)
    st.plotly_chart(grafico_horas_desempeno, use_container_width=True)

# =============================================================================
# SECCIÓN 10. CÓDIGO PARA DESPLEGAR LAS CONCLUSIONES DEL ANÁLISIS
# =============================================================================
st.header("Conclusión del análisis")

# Cálculos dinámicos que se adaptan a los filtros seleccionados
promedio_desempeno = datos_filtrados["performance_score"].mean()
promedio_horas = datos_filtrados["average_work_hours"].mean()
promedio_satisfaccion = datos_filtrados["satisfaction_level"].mean()
correlacion_horas_desempeno = datos_filtrados["average_work_hours"].corr(
    datos_filtrados["performance_score"]
)
pct_alto_desempeno = (
    (datos_filtrados["performance_score"] >= 3).mean() * 100
)

st.markdown(
    f"""
    Con base en los **{len(datos_filtrados)} colaboradores** que cumplen con los
    filtros seleccionados, se concluye lo siguiente:

    **Fortalezas**
    - El **{pct_alto_desempeno:.1f}%** del personal analizado alcanza un puntaje
      de desempeño de 3 o más (*Fully Meets* o *Exceeds*), lo que refleja un
      equipo mayoritariamente comprometido con sus objetivos.
    - El promedio general de desempeño es de **{promedio_desempeno:.2f}** y el
      nivel promedio de satisfacción es de **{promedio_satisfaccion:.2f}**
      (escala 1 a 5), indicadores de un clima laboral estable.

    **Áreas de oportunidad**
    - La correlación entre horas trabajadas y desempeño es de
      **{correlacion_horas_desempeno:.2f}**, es decir, trabajar más horas
      (promedio actual: **{promedio_horas:,.0f} horas mensuales**) **no garantiza
      un mejor desempeño**; conviene enfocar los esfuerzos en la calidad del
      trabajo y no en la cantidad de horas.
    - Se recomienda dar seguimiento cercano a los colaboradores con puntajes de
      1 y 2 (*PIP* y *Needs Improvement*) mediante planes de capacitación y
      retroalimentación continua.
    - El análisis de edad vs. salario permite verificar la **equidad salarial**
      entre géneros y grupos de edad; cualquier brecha detectada debe revisarse
      con el área de Recursos Humanos.

    En conjunto, el panel permite a la gerencia identificar de un solo
    vistazo el estado del equipo y tomar decisiones informadas para mejorar el
    desempeño del Área de Marketing de *Socialize your knowledge*.
    """
)
