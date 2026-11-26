# ♠ VIP Intelligence

Predictive analytics for iGaming VIP lifecycle transitions, powered by machine learning and Streamlit.

**Responsable del despliegue:** Daniel Holguin

## Funcionalidades

- Churn VIP: estima la pérdida de calificación VIP en el mes siguiente mediante votación soft (regresión logística, MLP y Gradient Boosting).
- Reactivación VIP: estima el reingreso al segmento VIP mediante regresión logística.
- Formularios con perfiles sintéticos editables, scores, umbrales y métricas agregadas de evaluación.

Los dos análisis fueron desarrollados en colaboración. La interfaz es una demostración técnica; no predice abandono total de la plataforma ni retorno al juego.

## Ejecución local

Python 3.13 recomendado.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Despliegue en Streamlit Community Cloud

Seleccionar el repositorio, la rama `main` y `app.py` como archivo principal. Utilizar Python 3.13 si está disponible. Mantener `.streamlit/config.toml` en su carpeta original.

## Artefactos y evaluación

La aplicación carga dos modelos entrenados localmente y no necesita las bases de entrenamiento. El modelo de churn fue reproducido para compatibilidad con scikit-learn 1.8.0 e imbalanced-learn 0.14.1, manteniendo arquitectura, hiperparámetros y umbral original de 0,40; las predicciones individuales pueden diferir del artefacto original. Las métricas de churn corresponden a la evaluación retrospectiva de septiembre de la reproducción compatible. La versión de despliegue fue ajustada con enero–septiembre y no conserva el remuestreador ajustado. Reactivación conserva su modelo original y su evaluación retrospectiva de agosto. Los scores no tienen calibración demostrada. La disponibilidad temporal de `perfilado` en churn requiere confirmación. Las métricas de ambos modelos no son directamente comparables debido a las diferentes poblaciones y prevalencias.

## Privacidad y uso responsable

Los ejemplos precargados son ficticios. No se incluyen archivos de datos de entrenamiento, identificadores ni registros individuales. Los artefactos contienen parámetros aprendidos de los datos: su publicación y la de las métricas requieren autorización del titular de la información. No introducir datos personales o confidenciales. Esta demostración no ofrece apuestas ni recomendaciones de contacto o incentivos. No usar para decisiones sobre personas sin validación independiente y controles adecuados de privacidad y juego responsable.
