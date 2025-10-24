#!/usr/bin/env python3
"""
Quick start example - Demostración de uso del proyecto
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.data import load_events_data
from src.stats import descriptive, advanced
from src.viz import basic, advanced as viz_advanced


def example_basic_stats():
    """Ejemplo 1: Estadísticas básicas"""
    print("\n" + "="*70)
    print("EJEMPLO 1: Estadísticas Básicas")
    print("="*70)
    
    data = load_events_data()
    
    for year in sorted(data.keys()):
        total = descriptive.total(data[year])
        avg = descriptive.total_avg(data[year])
        peak = descriptive.peak_month(data[year])
        lowest = descriptive.lowest_month(data[year])
        
        print(f"\n{year}:")
        print(f"  Total: {total:3d} eventos")
        print(f"  Promedio: {avg:.2f} eventos/mes")
        print(f"  Mes pico: {peak}")
        print(f"  Mes bajo: {lowest}")


def example_advanced_stats():
    """Ejemplo 2: Estadísticas avanzadas"""
    print("\n" + "="*70)
    print("EJEMPLO 2: Estadísticas Avanzadas")
    print("="*70)
    
    data = load_events_data()
    
    # Tendencia anual
    trend = advanced.year_over_year_trend(data)
    print(f"\n📈 Tendencia anual:")
    print(f"  Dirección: {trend['trend'].upper()}")
    print(f"  Slope: {trend['slope']:.4f} eventos/año")
    print(f"  Significancia: {'SÍ ✓' if trend['significant'] else 'NO ✗'} (p={trend['p_value']:.4f})")
    print(f"  R²: {trend['r_squared']:.4f}")
    
    # Estacionalidad
    seasonality = advanced.seasonality_anova(data)
    print(f"\n🌊 Estacionalidad (ANOVA):")
    print(f"  Detectada: {'SÍ ✓' if seasonality['significant'] else 'NO ✗'}")
    print(f"  p-value: {seasonality['p_value']:.4f}")
    
    # Distribución de días
    day_dist = advanced.day_distribution_analysis(data[2024])
    print(f"\n📅 Distribución de días (2024):")
    print(f"  Día más común: {day_dist['most_common_day']} ({day_dist['most_common_count']} veces)")
    print(f"  Día menos común: {day_dist['least_common_day']} ({day_dist['least_common_count']} veces)")
    print(f"  Eventos primera semana: {day_dist['first_week_events']}")
    print(f"  Eventos fin de mes: {day_dist['end_month_events']}")


def example_comparisons():
    """Ejemplo 3: Comparaciones entre años"""
    print("\n" + "="*70)
    print("EJEMPLO 3: Comparaciones entre Años")
    print("="*70)
    
    data = load_events_data()
    
    # 2020 vs 2024
    comp = descriptive.compare_years(data[2020], data[2024], 2020, 2024)
    
    ta, tb = comp['total_events']
    print(f"\n2020 vs 2024:")
    print(f"  Total: {ta} → {tb} ({((tb-ta)/ta*100):+.1f}%)")
    print(f"  Promedio/mes: {comp['avg_per_month'][0]:.2f} → {comp['avg_per_month'][1]:.2f}")
    print(f"  Similitud (Jaccard): {comp['jaccard_days']} (1.0 = idéntico)")
    
    # Correlaciones
    correlations = advanced.correlation_between_years(data)
    print(f"\n🔗 Correlaciones año-a-año:")
    for corr in correlations['correlations']:
        print(f"  {corr['pair']}: r = {corr['correlation']:6.3f} ({corr['relationship']})")


def example_predictions():
    """Ejemplo 4: Predicciones y resumen"""
    print("\n" + "="*70)
    print("EJEMPLO 4: Predicciones y Resumen Predictivo")
    print("="*70)
    
    data = load_events_data()
    
    pred = advanced.predictive_summary(data)
    print(f"\nResumen predictivo para 2025:")
    print(f"  Tendencia: {pred['trend_direction'].upper()}")
    print(f"  Tendencia significativa: {'SÍ ✓' if pred['trend_significance'] else 'NO ✗'}")
    print(f"  Estacionalidad: {'SÍ ✓' if pred['seasonality_detected'] else 'NO ✗'}")
    print(f"  Total esperado: ~{pred['expected_annual_total']:.0f} eventos")
    print(f"\n  Patrón esperado por mes:")
    for i, count in enumerate(pred['avg_monthly_pattern_recent']):
        month_name = descriptive.MONTHS[i] if i < 12 else f"Mes {i+1}"
        print(f"    {month_name:12s}: {count:5.1f} eventos")


def example_visualizations():
    """Ejemplo 5: Generar visualizaciones"""
    print("\n" + "="*70)
    print("EJEMPLO 5: Generar Visualizaciones")
    print("="*70)
    
    data = load_events_data()
    
    print("\nGenerando visualizaciones seleccionadas...")
    print("  (No se mostrarán, se guardarán en outputs/)")
    
    # Generar algunas visualizaciones
    basic.plot_year_comparison(data, save_path='outputs/example_comparison.png', show=False)
    print("  ✓ year_comparison.png")
    
    viz_advanced.plot_heatmap_days_vs_years(data, save_path='outputs/example_heatmap.png', show=False)
    print("  ✓ heatmap_intensity.png")
    
    viz_advanced.plot_trend_with_regression(data, save_path='outputs/example_trend.png', show=False)
    print("  ✓ trend_analysis.png")
    
    print("\n  Archivos guardados en outputs/")


def main():
    print("\n" + "🎓 "*20)
    print("  QUICK START - Analysis Conteo v2.0")
    print("🎓 "*20)
    
    try:
        example_basic_stats()
        example_advanced_stats()
        example_comparisons()
        example_predictions()
        example_visualizations()
        
        print("\n" + "="*70)
        print("✅ TODOS LOS EJEMPLOS COMPLETADOS EXITOSAMENTE")
        print("="*70)
        print("\nPróximos pasos:")
        print("  1. Revisa outputs/ para ver las visualizaciones")
        print("  2. Modifica este script para tus análisis específicos")
        print("  3. Lee README.md para documentación completa")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
