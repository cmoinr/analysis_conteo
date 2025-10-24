# 🚀 GUÍA RÁPIDA - Analysis Conteo v2.0

## ⚡ Inicio Rápido (3 pasos)

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar análisis completo
```bash
python main.py
```

### 3. Ver gráficos en `outputs/`
- 📊 13 visualizaciones automáticas
- 📄 Reporte completo en consola

---

## 📚 Usar en tu código

### Cargar datos
```python
from src.data import load_events_data
data = load_events_data()  # Dict[int, List[List[int]]]
```

### Estadísticas básicas
```python
from src.stats import descriptive as desc

total = desc.total(data[2024])
avg = desc.total_avg(data[2024])
cv = desc.coefficient_of_variation(data[2024])
print(f"{total} eventos, {avg}/mes, CV={cv}%")
```

### Estadísticas avanzadas
```python
from src.stats import advanced as adv

# Tendencias
trend = adv.year_over_year_trend(data)
print(f"Tendencia: {trend['trend']} (p={trend['p_value']})")

# Estacionalidad
season = adv.seasonality_anova(data)
print(f"Estacionalidad: {'SÍ' if season['significant'] else 'NO'}")

# Predicción
pred = adv.predictive_summary(data)
print(f"Eventos esperados 2025: {pred['expected_annual_total']}")
```

### Visualizaciones
```python
from src.viz import basic, advanced as viz

# Gráficos simples
basic.plot_year_comparison(data, show=True)
basic.plot_box_comparison(data, show=True)

# Gráficos avanzados
viz.plot_heatmap_days_vs_years(data, show=True)
viz.plot_trend_with_regression(data, show=True)
viz.plot_correlation_matrix(data, show=True)

# Generar todos
viz.generate_all_plots(data, 'outputs')
```

---

## 🔍 Función a Función

### `src/stats/descriptive.py`
```python
total(data)                          # Total eventos
total_avg(data)                      # Promedio/mes
total_per_month(data)               # Lista de eventos por mes
peak_month(data)                    # Mes con más eventos
lowest_month(data)                  # Mes con menos eventos
top_repeated_days(data, n=3)        # Top N días más frecuentes
least_repeated_days(data, n=3)      # Bottom N días menos frecuentes
unique_days_per_month(data)         # Días únicos por mes
unique_days_total(data)             # Total días únicos
std_dev_events_per_month(data)      # Desviación estándar
coefficient_of_variation(data)      # CV en porcentaje
jaccard_similarity_days(a, b)       # Similitud conjuntos [0,1]
compare_years(a, b, ya, yb)         # Comparación completa
view_data(data)                     # Print resumen
```

### `src/stats/advanced.py`
```python
linear_trend(data)                  # Regresión lineal meses
year_over_year_trend(data_dict)    # Regresión anual
seasonality_anova(data_dict)        # Test ANOVA meses
day_distribution_analysis(data)     # Análisis por día mes
bootstrap_confidence_interval(data) # Intervalos confianza
correlation_between_years(data_dict) # Pearson entre años
mann_whitney_test(a, b)             # Test Mann-Whitney U
normality_test(data)                # Test Shapiro-Wilk
predictive_summary(data_dict)       # Resumen predicción
comprehensive_analysis(data_dict)   # Análisis completo
```

### `src/viz/basic.py`
```python
plot_monthly_totals(data, year, save_path, show)
plot_year_comparison(years_data, save_path, show)
plot_distribution_histogram(years_data, save_path, show)
plot_box_comparison(years_data, save_path, show)
```

### `src/viz/advanced.py`
```python
plot_heatmap_days_vs_years(years_data, save_path, show)
plot_trend_with_regression(years_data, save_path, show)
plot_day_distribution(data, year, save_path, show)
plot_correlation_matrix(years_data, save_path, show)
plot_kde_comparison(years_data, save_path, show)
generate_all_plots(years_data, output_dir)
```

---

## 📊 Estructura de Datos

### Entrada (JSON)
```json
{
  "events": {
    "2024": [
      [2, 3, 5, 9, 10, 12, 21],    // Enero (7 eventos)
      [6, 9, 11, 15, 16],           // Febrero (5 eventos)
      ...
    ]
  }
}
```

### En memoria
```python
data_by_year = {
    2024: [
        [2, 3, 5, 9, 10, 12, 21],   # Enero
        [6, 9, 11, 15, 16],          # Febrero
        ...
    ],
    ...
}
```

---

## 🎯 Casos de Uso

### Caso 1: Comparar dos años
```python
comp = descriptive.compare_years(data[2020], data[2024], 2020, 2024)
ta, tb = comp['total_events']
print(f"Cambio: {ta} → {tb}")
```

### Caso 2: Detectar anomalías
```python
norm = advanced.normality_test(data[2024])
if not norm['normal']:
    print("⚠️ Distribución anormal detectada")
```

### Caso 3: Predicción simple
```python
pred = advanced.predictive_summary(data)
print(f"Esperado 2025: {pred['expected_annual_total']:.0f} eventos")
```

### Caso 4: Análisis completo
```python
analysis = advanced.comprehensive_analysis(data)
print(analysis.keys())  # trend, seasonality, correlations, predictive
```

---

## 📁 Archivos Clave

| Archivo | Propósito |
|---------|-----------|
| `main.py` | Punto entrada - ejecuta análisis completo |
| `examples.py` | Ejemplos de uso de cada módulo |
| `data/raw/events.json` | Datos originales en JSON |
| `src/data/loader.py` | Cargar y validar datos |
| `src/stats/descriptive.py` | 13 funciones estadísticas básicas |
| `src/stats/advanced.py` | 12 funciones estadísticas avanzadas |
| `src/viz/basic.py` | 4 gráficos básicos |
| `src/viz/advanced.py` | 5 gráficos avanzados + batch |

---

## ⚙️ Configuración

### Cambiar ruta de datos
```python
from src.data.loader import load_events_data, get_data_path
# Por defecto: data/raw/events.json
data = load_events_data('events.json')
```

### Cambiar ruta de salida
```python
from src.viz.advanced import generate_all_plots
generate_all_plots(data, output_dir='mi_carpeta')
```

### Guardar gráficos sin mostrar
```python
basic.plot_year_comparison(data, save_path='outputs/plot.png', show=False)
```

---

## 🐛 Troubleshooting

**Problema: "ModuleNotFoundError: No module named 'scipy'"**
```bash
pip install -r requirements.txt
```

**Problema: "FileNotFoundError: data/raw/events.json"**
- Verificar que estás en el directorio correcto
- Ejecutar: `cd analysis_conteo && python main.py`

**Problema: "Year 2025: Expected 12 months, got 9"**
- 2025 tiene solo 9 meses de datos
- Completar datos en `data/raw/events.json`

---

## 📈 Interpretación de Resultados

| Métrica | Bueno | Malo |
|---------|-------|------|
| **p-value** | < 0.05 | > 0.05 |
| **R²** | > 0.7 | < 0.3 |
| **Correlación** | ±0.7 - ±1.0 | ±0.0 - ±0.3 |
| **CV (%)** | 10-20% | > 50% |
| **Jaccard** | 0.8-1.0 | < 0.5 |

---

## 🔗 Enlaces Útiles

- 📖 [README.md](README.md) - Documentación completa
- 📊 [SUMMARY.md](SUMMARY.md) - Resumen de cambios
- 🎓 [examples.py](examples.py) - Ejemplos de código

---

## 💡 Tips

- ✅ Ejecuta `python main.py` primero para ver todo
- ✅ Modifica `examples.py` para tus análisis específicos
- ✅ Usa type hints para mejor autocompletar en IDE
- ✅ Exporta datos con `export_to_json()` si lo necesitas
- ✅ Los gráficos se guardan automáticamente en `outputs/`

---

**¡Listo! Ahora estás preparado para usar Analysis Conteo v2.0 🚀**

