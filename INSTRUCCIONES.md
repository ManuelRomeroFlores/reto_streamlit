# Cómo ejecutar la aplicación

1. Coloca en una misma carpeta estos archivos:
   - `app.py`
   - `Employee_data.csv`  (renombra tu archivo original a este nombre exacto)
   - `logo_syk.png`

2. Instala las librerías (solo la primera vez):
   ```
   pip install streamlit pandas plotly
   ```

3. Ejecuta la aplicación desde la terminal, dentro de la carpeta:
   ```
   streamlit run app.py
   ```

4. Se abrirá automáticamente en tu navegador (http://localhost:8501).

## Estructura del código (mapeo con la rúbrica)

| Criterio de la rúbrica | Sección en app.py |
|---|---|
| 1. Título y descripción | SECCIÓN 1 — `st.title()` + `st.markdown()` |
| 2. Logotipo de la empresa | SECCIÓN 2 — `st.sidebar.image()` |
| 3. Control de género | SECCIÓN 3 — `st.sidebar.selectbox()` |
| 4. Control de rango de puntaje | SECCIÓN 4 — `st.sidebar.slider()` |
| 5. Control de estado civil | SECCIÓN 5 — `st.sidebar.selectbox()` |
| 6. Distribución de puntajes | SECCIÓN 6 — `px.histogram()` + `st.plotly_chart()` |
| 7. Horas promedio por género | SECCIÓN 7 — `groupby` + `px.bar()` |
| 8. Edad vs. salario | SECCIÓN 8 — `px.scatter()` |
| 9. Horas vs. desempeño | SECCIÓN 9 — `groupby` + `px.bar()` |
| 10. Conclusión del análisis | SECCIÓN 10 — `st.markdown()` con cálculos dinámicos |
