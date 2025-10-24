# 📚 ÍNDICE DE ARCHIVOS - Analysis Conteo v2.0

## 📋 Documentación
| Archivo | Descripción |
|---------|------------|
| **README.md** | 📖 Documentación completa del proyecto |
| **QUICKSTART.md** | ⚡ Guía rápida para empezar |
| **SUMMARY.md** | 📊 Resumen de mejoras implementadas |
| **INDEX.md** | 📚 Este archivo - índice de archivos |

## 💻 Código Ejecutable
| Archivo | Descripción |
|---------|------------|
| **main.py** | 🎯 Punto de entrada - análisis completo |
| **examples.py** | 🎓 5 ejemplos de uso del sistema |

## 📦 Módulos (src/)
| Archivo | Descripción | Funciones |
|---------|------------|-----------|
| **src/__init__.py** | Inicialización paquete | - |
| **src/data/loader.py** | Cargar y validar JSON | 8 |
| **src/stats/descriptive.py** | Estadísticas básicas | 13 |
| **src/stats/advanced.py** | Análisis avanzados | 12 |
| **src/viz/basic.py** | Gráficos básicos | 4 |
| **src/viz/advanced.py** | Gráficos avanzados | 5 |

**Total: 35+ funciones documentadas con type hints**

## 📊 Datos
| Archivo | Descripción |
|---------|------------|
| **data/raw/events.json** | JSON con eventos 2020-2024 |
| **data/processed/** | (Vacío, para procesados futuros) |

## 🎨 Salida (Visualizaciones)
| Archivo | Tipo | Descripción |
|---------|------|------------|
| **outputs/monthly_totals_YEAR.png** | Bar | Eventos por mes (5 gráficos) |
| **outputs/year_comparison.png** | Line | Tendencias multi-año |
| **outputs/distribution_histogram.png** | Histogram | Distribución general |
| **outputs/box_comparison.png** | Box | Comparación por años |
| **outputs/heatmap_intensity.png** | Heatmap | 🔥 Matriz años-meses |
| **outputs/trend_analysis.png** | Scatter | 📈 Regresión anual |
| **outputs/day_distribution_recent.png** | Bar | 📅 Frecuencia por día |
| **outputs/correlation_matrix.png** | Heatmap | 🔗 Correlaciones |
| **outputs/kde_comparison.png** | KDE | Densidad por año |

**Total: 13 PNG de alta calidad (300 DPI)**

## ⚙️ Configuración
| Archivo | Descripción |
|---------|------------|
| **requirements.txt** | Dependencias Python |

## 🧪 Testing (preparado)
| Carpeta | Descripción |
|---------|------------|
| **tests/** | (Vacío, preparado para tests) |

---

## 🗂️ Estructura Completa

```
analysis_conteo/
├── 📄 Documentación
│   ├── README.md              ← DOCUMENTACIÓN COMPLETA
│   ├── QUICKSTART.md          ← GUÍA RÁPIDA
│   ├── SUMMARY.md             ← CAMBIOS IMPLEMENTADOS
│   └── INDEX.md               ← ESTE ARCHIVO
│
├── 💻 Scripts Ejecutables
│   ├── main.py                ← ANÁLISIS COMPLETO (EJECUTAR)
│   └── examples.py            ← EJEMPLOS DE USO
│
├── 📦 src/                    ← CÓDIGO FUENTE (MÓDULOS)
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── loader.py          ← JSON loader + validación
│   ├── stats/
│   │   ├── __init__.py
│   │   ├── descriptive.py     ← 13 funciones estadísticas
│   │   └── advanced.py        ← 12 análisis avanzados
│   └── viz/
│       ├── __init__.py
│       ├── basic.py           ← 4 gráficos básicos
│       └── advanced.py        ← 5 gráficos avanzados
│
├── 📊 data/                   ← DATOS
│   ├── raw/
│   │   └── events.json        ← DATOS (2020-2024)
│   └── processed/             ← (Vacío, para futuros usos)
│
├── 🎨 outputs/                ← VISUALIZACIONES GENERADAS
│   ├── monthly_totals_*.png   ← 5 gráficos
│   ├── year_comparison.png
│   ├── distribution_histogram.png
│   ├── box_comparison.png
│   ├── heatmap_intensity.png
│   ├── trend_analysis.png
│   ├── day_distribution_recent.png
│   ├── correlation_matrix.png
│   └── kde_comparison.png
│
├── 🧪 tests/                  ← TESTS (PREPARADO)
│   └── (vacío)
│
└── ⚙️ Configuración
    ├── requirements.txt       ← DEPENDENCIAS
    ├── __init__.py           ← (antiguo)
    └── (archivos antiguos)   ← conteo.py, data.py, stats.py, etc
```

---

## 🚀 CÓMO EMPEZAR (3 pasos)

### 1️⃣ Instalar
```bash
pip install -r requirements.txt
```

### 2️⃣ Ejecutar
```bash
python main.py
```

### 3️⃣ Explorar
- 📄 Revisa `README.md` para documentación
- ⚡ Revisa `QUICKSTART.md` para guía rápida
- 🎓 Ejecuta `python examples.py` para ver ejemplos
- 📊 Mira los gráficos en `outputs/`

---

## 📈 ANÁLISIS DISPONIBLES

### Estadísticas Básicas (13)
```python
from src.stats import descriptive
```
- Total, promedio, desviación estándar
- Coeficiente de Variación (CV%)
- Similitud Jaccard
- Días únicos por mes/total
- Meses pico y valle
- Días más/menos frecuentes

### Estadísticas Avanzadas (12)
```python
from src.stats import advanced
```
- Regresión lineal (tendencias)
- ANOVA (estacionalidad)
- Correlaciones Pearson
- Shapiro-Wilk (normalidad)
- Mann-Whitney U (distribuciones)
- Bootstrap (intervalos confianza)
- Análisis distribución días
- Resumen predictivo

### Visualizaciones (13)
```python
from src.viz import basic, advanced as viz
```
- Barras, líneas, histogramas, box plots
- **Heatmaps** (matriz intensidad)
- **Scatter + Regresión** (tendencias)
- **Correlaciones** (matriz heatmap)
- **KDE plots** (densidad)

---

## 🎯 FUNCIONES MÁS IMPORTANTES

### Cargar datos
```python
from src.data import load_events_data
data = load_events_data()  # Dict[int, List[List[int]]]
```

### Análisis rápido
```python
from src.stats import descriptive as desc
desc.view_data(data[2024])  # Resumen completo
```

### Comparar años
```python
from src.stats import descriptive as desc
comp = desc.compare_years(data[2020], data[2024], 2020, 2024)
```

### Detectar tendencias
```python
from src.stats import advanced as adv
trend = adv.year_over_year_trend(data)
```

### Generar visualizaciones
```python
from src.viz import advanced as viz
viz.generate_all_plots(data, 'outputs')
```

---

## 📊 ESTADÍSTICAS ACTUALES (2020-2024)

| Métrica | Valor |
|---------|-------|
| Años analizados | 5 (2020-2024) |
| Total eventos | 715 |
| Promedio anual | 143 |
| Rango | 127-160 |
| Tendencia | ↗️ Crecimiento |
| Estacionalidad | ❌ No detectada |
| Consistencia | ✅ Alta (0.97) |
| Predicción 2025 | ~144 eventos |

---

## 🔗 DEPENDENCIAS EXTERNAS

| Paquete | Versión | Uso |
|---------|---------|-----|
| numpy | ≥1.21 | Cálculos numéricos |
| pandas | ≥1.3 | Manipulación datos |
| scipy | ≥1.7 | Tests estadísticos |
| matplotlib | ≥3.4 | Gráficos base |
| seaborn | ≥0.11 | Gráficos mejorados |
| plotly | ≥5.0 | Gráficos interactivos |
| statsmodels | ≥0.13 | Modelos estadísticos |

---

## ✨ CARACTERÍSTICAS V2.0

- ✅ Estructura modular y profesional
- ✅ Datos en JSON (MongoDB-ready)
- ✅ Validación robusta
- ✅ 35+ funciones documentadas
- ✅ Type hints 100%
- ✅ 13 visualizaciones
- ✅ Reportes automáticos
- ✅ Ejemplos incluidos
- ✅ Docstrings completos
- ✅ Listo para producción

---

## 🎓 SIGUIENTE LECTURA

1. **Primero**: README.md (visión general)
2. **Luego**: QUICKSTART.md (guía rápida)
3. **Después**: examples.py (código)
4. **Profundo**: Docstrings en src/

---

## 📞 SOPORTE

- 📖 Ver README.md para preguntas frecuentes
- 🎓 Ver examples.py para código de ejemplo
- 💻 Ver QUICKSTART.md para troubleshooting
- 📊 Ver SUMMARY.md para cambios implementados

---

**¡Bienvenido a Analysis Conteo v2.0! 🚀**

Última actualización: 2025-10-24
Versión: 2.0.0
