# 🎯 Analysis Conteo v2.0

**Event Data Analysis and Statistical Insights System**

Un sistema profesional para analizar datos de eventos recurrentes en un día específico del mes a lo largo de múltiples años, con estadísticas avanzadas, visualizaciones interactivas y reportes automáticos.

---

## 📋 Características Principales

### ✨ Estadísticas Básicas
- Totales y promedios por año y mes
- Identificación de meses pico y valle
- Días más frecuentes y menos frecuentes
- Distribución de días únicos por mes
- Coeficiente de Variación (CV)

### 🚀 Estadísticas Avanzadas
- **Tendencias**: Regresión lineal año-a-año para detectar patrones de crecimiento/decrecimiento
- **Estacionalidad**: Test ANOVA para determinar si ciertos meses tienen eventos significativamente diferentes
- **Correlaciones**: Análisis de pearson entre patrones mensuales de años adyacentes
- **Tests no-paramétricos**: Mann-Whitney U test para comparar distribuciones
- **Normalidad**: Shapiro-Wilk test para validar distribuciones
- **Bootstrap**: Intervalos de confianza robustos mediante remuestreo
- **Predicción**: Resumen de métricas útiles para forecasting

### 📊 Visualizaciones
- Gráficos de barras por año
- Líneas de tendencia multi-año
- Histogramas de distribución
- Box plots de comparación
- **Heatmap** de intensidad (años vs meses)
- **Scatter plots** con línea de regresión
- Distribución por día del mes
- **Matriz de correlaciones**
- **KDE plots** para análisis de densidad

### 📄 Formatos de Datos
- **Entrada**: JSON con estructura validada (`data/raw/events.json`)
- **Salida**: 
  - Reportes textuales formatados
  - Visualizaciones PNG de alta calidad (300 DPI)
  - Análisis exportables

---

## 📁 Estructura del Proyecto

```
analysis_conteo/
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── loader.py           # Cargador JSON con validación
│   ├── stats/
│   │   ├── __init__.py
│   │   ├── descriptive.py      # Estadísticas básicas
│   │   └── advanced.py         # Estadísticas avanzadas (tendencias, ANOVA, etc)
│   └── viz/
│       ├── __init__.py
│       ├── basic.py            # Gráficos básicos
│       └── advanced.py         # Heatmaps, scatter, correlaciones, etc
├── data/
│   ├── raw/
│   │   └── events.json         # Datos originales
│   └── processed/              # Datos procesados (vacío, preparado para futuros usos)
├── outputs/                    # Gráficos y reportes generados
├── tests/                      # Tests unitarios (futuro)
├── main.py                     # Punto de entrada principal
├── requirements.txt            # Dependencias Python
└── README.md                   # Este archivo
```

---

## 🚀 Instalación y Uso

### Prerequisitos
- Python 3.8+
- pip

### Instalación

1. **Clonar o descargar el repositorio**
```bash
cd analysis_conteo
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### Ejecución

**Ejecutar análisis completo con reportes y visualizaciones:**
```bash
python main.py
```

**En notebook o script personalizado:**
```python
from src.data import load_events_data
from src.stats import descriptive, advanced
from src.viz import basic, advanced as viz_advanced

# Cargar datos
data_by_year = load_events_data()

# Estadísticas descriptivas
for year in sorted(data_by_year.keys()):
    descriptive.view_data(data_by_year[year], year=year)

# Análisis avanzado
trend = advanced.year_over_year_trend(data_by_year)
seasonality = advanced.seasonality_anova(data_by_year)

# Generar visualizaciones
viz_advanced.generate_all_plots(data_by_year, output_dir='outputs')
```

---

## 📊 Formato de Datos JSON

```json
{
  "metadata": {
    "description": "Daily events data...",
    "event_type": "recurring_monthly_event",
    "date_range": "2020-2025"
  },
  "events": {
    "2020": [
      [3, 9, 11, 13, 15, 17, 17, 20],  // Enero
      [6, 7, 9, 14, 14, 18, 18, 19],   // Febrero
      ...
    ],
    "2021": [...],
    ...
  }
}
```

**Estructura:**
- 12 meses por año (enero a diciembre)
- Cada mes contiene una lista de días (1-31) donde ocurrieron eventos
- Días pueden repetirse si ocurrieron múltiples eventos ese día

---

## 📈 Métricas y Análisis

### Estadísticas Básicas
| Métrica | Descripción |
|---------|------------|
| Total | Cantidad total de eventos en el año |
| Promedio | Promedio de eventos por mes |
| Desv. Estándar | Variabilidad de eventos entre meses |
| CV (%) | Coeficiente de Variación = (σ/μ) × 100 |
| Jaccard | Similitud de días únicos entre años (0-1) |

### Estadísticas Avanzadas
| Test | Interpretación |
|------|---|
| **Regresión Lineal** | Detecta tendencias significativas (p < 0.05 = significativo) |
| **ANOVA** | Prueba si hay estacionalidad (diferencias significativas entre meses) |
| **Pearson r** | Correlación entre patrones mensuales (-1 a +1) |
| **Mann-Whitney U** | Compara distribuciones no-paramétricamente |
| **Shapiro-Wilk** | Verifica si datos siguen distribución normal |
| **Bootstrap** | Genera intervalos de confianza robustos |

### Análisis de Distribución de Días
- Por semana (1-7, 8-14, 15-21, 22-28)
- Fin de mes (29-31)
- Día más y menos frecuente

---

## 📊 Visualizaciones Generadas

Al ejecutar `main.py`, se generan automáticamente en `outputs/`:

1. **monthly_totals_YEAR.png** - Barras de eventos por mes (una por año)
2. **year_comparison.png** - Líneas de tendencia múltiples años
3. **distribution_histogram.png** - Histograma de distribución general
4. **box_comparison.png** - Box plots por año
5. **heatmap_intensity.png** - Mapa de calor años × meses
6. **trend_analysis.png** - Scatter + regresión año-a-año
7. **day_distribution_recent.png** - Frecuencia por día del mes
8. **correlation_matrix.png** - Matriz de correlaciones entre años
9. **kde_comparison.png** - Curvas de densidad por año

---

## 🔍 Ejemplo de Salida

```
======================================================================
  🎯 ANALYSIS CONTEO v2.0 - Event Data Analysis System
======================================================================

======================================================================
  DESCRIPTIVE STATISTICS BY YEAR
======================================================================

📊 Year 2020:
----------------------------------------------------------------------
Total: 249
Total AVG: 20.75/month
Total per months: [8, 8, 7, 6, 7, 11, 11, 13, 13, 11, 13, 19]
Highest month: December
Lowest month: April
Top 3 repeated days: [(1, 4), (27, 4), (18, 4)]
Bottom 3 least frequent days: [(2, 1), (7, 1), (8, 1)]
Unique days per month: [8, 8, 7, 6, 7, 11, 11, 13, 13, 11, 13, 19]
Standard deviation: 3.35
Coefficient of variation: 16.14%

...
```

---

## 🛠️ Extensiones Futuras

- [ ] Tests unitarios (`tests/`)
- [ ] Dashboard interactivo con Streamlit
- [ ] Modelos de predicción (ARIMA, Prophet)
- [ ] Exportación a Excel/PDF
- [ ] API REST con FastAPI
- [ ] Base de datos MongoDB
- [ ] Visualización interactiva con Plotly Dash

---

## 📝 Cambios en v2.0

### ✨ Nuevas Características
- ✅ Estructura de carpetas profesional (`src/`, `data/`, `outputs/`)
- ✅ Datos en JSON en lugar de hardcodeado
- ✅ Data loader con validación robusta
- ✅ Estadísticas avanzadas (ANOVA, regresión, correlaciones, etc)
- ✅ Visualizaciones mejoradas (heatmaps, KDE, scatter)
- ✅ Reportes formatados y automáticos
- ✅ Type hints completos
- ✅ Logging integrado

### 🔄 Refactorizado
- Módulos separados por responsabilidad
- Funciones con docstrings detallados
- Eliminación de código duplicado
- Mejor mantenibilidad y escalabilidad

---

## 📚 Referencias

- [NumPy Documentation](https://numpy.org/doc/)
- [SciPy Statistics](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [Matplotlib/Seaborn](https://matplotlib.org/)
- [Statsmodels](https://www.statsmodels.org/)

---

## 👨‍💻 Autor

**Analysis Conteo Team**

---

## 📄 Licencia

MIT License

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## ❓ Preguntas?

Consulta la documentación en `src/` o abre un issue en el repositorio.

**¡Happy Analyzing! 📊✨**
