# ❓ PREGUNTAS FRECUENTES - Analysis Conteo v2.0

## 🤔 Preguntas Frecuentes

### 1. ¿Cómo instalo el proyecto?

```bash
cd analysis_conteo
pip install -r requirements.txt
```

**Si tienes errores**, intenta:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

### 2. ¿Cómo ejecuto el análisis?

**Opción 1: Análisis completo**
```bash
python main.py
```
Genera reporte completo + 13 gráficos en `outputs/`

**Opción 2: Ver ejemplos**
```bash
python examples.py
```
Muestra 5 ejemplos de uso

**Opción 3: En tu código**
```python
from src.data import load_events_data
from src.stats import advanced

data = load_events_data()
trend = advanced.year_over_year_trend(data)
print(trend)
```

---

### 3. ¿Qué son los gráficos que se generan?

**Gráficos básicos:**
- `monthly_totals_YEAR.png` - Barras de eventos por mes
- `year_comparison.png` - Líneas de tendencia
- `distribution_histogram.png` - Histograma
- `box_comparison.png` - Box plots

**Gráficos avanzados:**
- `heatmap_intensity.png` - 🔥 Mapa de calor (años vs meses)
- `trend_analysis.png` - 📈 Scatter + regresión
- `day_distribution_recent.png` - 📅 Días más frecuentes
- `correlation_matrix.png` - 🔗 Correlaciones
- `kde_comparison.png` - Curvas de densidad

---

### 4. ¿Cómo agrego más datos?

1. **Editar `data/raw/events.json`**:
```json
{
  "events": {
    "2025": [
      [1, 2, 3, ...],  // Enero
      [4, 5, 6, ...],  // Febrero
      ...              // 12 meses total
    ]
  }
}
```

2. **Ejecutar análisis nuevamente**:
```bash
python main.py
```

---

### 5. ¿Qué significan los resultados?

### Regresión (Tendencias)
```python
trend = advanced.year_over_year_trend(data)
```
- `slope`: Cambio por año (positivo = crecimiento)
- `p_value < 0.05`: Tendencia estadísticamente significativa
- `r_squared`: Qué tan bien predice (0-1)

### ANOVA (Estacionalidad)
```python
seasonality = advanced.seasonality_anova(data)
```
- `p_value < 0.05`: Meses tienen eventos significativamente diferentes
- `p_value > 0.05`: Todos los meses son similares

### Correlación
```python
correlations = advanced.correlation_between_years(data)
```
- `r = 1.0`: Perfectamente correlacionados
- `r = 0.0`: Sin correlación
- `r = -1.0`: Correlación inversa

---

### 6. ¿Cómo interpreto el Coeficiente de Variación (CV)?

```python
cv = descriptive.coefficient_of_variation(data[2024])
```

- **CV < 15%**: Muy consistente
- **CV 15-30%**: Moderadamente variable
- **CV > 30%**: Muy variable

Tu dato: 2024 tiene CV=17.88% (moderado)

---

### 7. ¿Qué es Jaccard similarity?

```python
jaccard = descriptive.jaccard_similarity_days(data[2020], data[2024])
```

Mide similitud entre días:
- **1.0**: Exactamente los mismos días
- **0.5**: 50% de similitud
- **0.0**: Completamente diferentes

Tu dato: 0.97 = muy similar

---

### 8. ¿Cómo uso esto con MongoDB?

1. **Exportar a JSON**:
```python
from src.data.loader import export_to_json
from pathlib import Path

export_to_json(data, Path('data/processed/events.json'))
```

2. **Cargar en MongoDB**:
```bash
mongoimport --db analysis --collection events --file data/processed/events.json
```

---

### 9. ¿Puedo crear mis propios análisis?

¡Sí! El código es modular:

```python
from src.stats import advanced, descriptive

def mi_analisis_custom(data):
    """Mi análisis personalizado"""
    for year in sorted(data.keys()):
        total = descriptive.total(data[year])
        trend = advanced.year_over_year_trend({year: data[year]})
        print(f"{year}: {total} eventos")
    
mi_analisis_custom(data)
```

---

### 10. ¿Cómo agrego nuevas funciones estadísticas?

Edita `src/stats/advanced.py`:

```python
def mi_metrica(data: List[List[int]]) -> float:
    """Mi métrica personalizada"""
    counts = total_per_month(data)
    # Tu lógica aquí
    return resultado
```

---

### 11. ¿Por qué falta 2025?

El JSON solo tiene 9 meses de 2025. 

Para incluirlo:
1. Completa los 12 meses en `data/raw/events.json`
2. O ignóralo (el loader lo salta automáticamente)

---

### 12. ¿Dónde están los tests?

**`tests/` está vacío** pero preparado.

Para agregar tests:
```python
# tests/test_stats.py
import unittest
from src.stats import descriptive

class TestDescriptive(unittest.TestCase):
    def test_total(self):
        data = [[1, 2], [3, 4]]
        self.assertEqual(descriptive.total(data), 4)
```

---

### 13. ¿Puedo cambiar los gráficos?

Sí, edita `src/viz/basic.py` o `src/viz/advanced.py`:

```python
def plot_monthly_totals(...):
    # Cambiar colores
    bars = ax.bar(months, totals, color='green')  # ← Cambia aquí
    
    # Cambiar títulos
    ax.set_title('MI TÍTULO PERSONALIZADO')  # ← O aquí
```

---

### 14. ¿Cómo exporto a Excel/PDF?

**A Excel**:
```python
import pandas as pd
from src.stats import descriptive

data = load_events_data()
df = pd.DataFrame({
    'Year': [2020, 2021, 2022, 2023, 2024],
    'Total': [descriptive.total(data[y]) for y in sorted(data.keys())]
})
df.to_excel('outputs/resumen.xlsx', index=False)
```

**A PDF**: Usa `matplotlib`:
```python
plt.savefig('outputs/grafico.pdf', format='pdf')
```

---

### 15. ¿Cuáles son los requisitos mínimos?

- **Python**: 3.8+
- **RAM**: 512 MB (tu dataset es pequeño)
- **Disco**: 100 MB (para dependencias)

---

### 16. ¿Cómo creo un dashboard?

Instala Streamlit:
```bash
pip install streamlit
```

Crea `app.py`:
```python
import streamlit as st
from src.data import load_events_data
from src.stats import descriptive

st.title("Analysis Conteo Dashboard")

data = load_events_data()

for year in sorted(data.keys()):
    st.metric(f"Total {year}", descriptive.total(data[year]))
```

Ejecuta:
```bash
streamlit run app.py
```

---

### 17. ¿Cómo colaboro/contribuyo?

1. Fork el proyecto
2. Crea rama `git checkout -b feature/mi-feature`
3. Commit `git commit -m "Agrego mi-feature"`
4. Push `git push origin feature/mi-feature`
5. Abre Pull Request

---

### 18. ¿Hay performance issues?

**Problema**: Lentitud al ejecutar

**Solución**: 
```python
# En main.py, comenta generación de gráficos
# viz_advanced.generate_all_plots(data)  # ← Comenta esta línea
```

**Problema**: Memoria excesiva

**Solución**: Tus datos son pequeños, no hay issue

---

### 19. ¿Cómo depuro errores?

**Activar logging detallado**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

data = load_events_data()  # Verás más detalles
```

---

### 20. ¿Qué licencia tiene?

**MIT License** - Úsalo libremente

---

## 🔗 Más Ayuda

| Necesitas | Consulta |
|-----------|----------|
| Visión general | README.md |
| Empezar rápido | QUICKSTART.md |
| Cambios v2.0 | SUMMARY.md |
| Archivos | INDEX.md |
| Código ejemplo | examples.py |
| Docstrings | src/*.py |

---

## 💬 Comentarios Adicionales

### Si los gráficos no se muestran:
```python
import matplotlib.pyplot as plt
plt.show()  # Agrégalo después de plot
```

### Si falta un módulo:
```bash
pip install --upgrade scipy numpy pandas
```

### Si quieres logs detallados:
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

**¡Si tu pregunta no está aquí, revisa los docstrings del código!**

Cada función tiene documentación completa:
```python
help(descriptive.total)
```

---

*Última actualización: 2025-10-24*
