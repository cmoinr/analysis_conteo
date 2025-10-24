"""Main entry point for event analysis."""

import sys
from pathlib import Path
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data import load_events_data
from src.stats import descriptive, advanced
from src.viz import basic, advanced as viz_advanced

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def print_subsection(title: str) -> None:
    """Print a formatted subsection header."""
    print(f"\n{title}")
    print("-" * 70)


def report_descriptive_stats(data_by_year: dict) -> None:
    """Generate descriptive statistics report."""
    print_section("DESCRIPTIVE STATISTICS BY YEAR")
    
    for year in sorted(data_by_year.keys()):
        print(f"\n📊 Year {year}:")
        print("-" * 70)
        descriptive.view_data(data_by_year[year], year=year)
        print()


def report_aggregate_stats(data_by_year: dict) -> None:
    """Generate aggregate statistics across years."""
    print_section("AGGREGATE STATISTICS")
    
    years_data = [data_by_year[y] for y in sorted(data_by_year.keys())]
    
    print_subsection("General Statistics")
    print(f"  • Average unique days per year: {descriptive.avg_unique_days(years_data)}")
    print(f"  • Days appearing in ALL years: {descriptive.common_days_across_years(years_data)}")
    
    print_subsection("Standard Deviation by Year")
    for year in sorted(data_by_year.keys()):
        stdev = descriptive.std_dev_events_per_month(data_by_year[year])
        cv = descriptive.coefficient_of_variation(data_by_year[year])
        print(f"  • {year}: σ = {stdev}, CV = {cv}%")


def report_year_comparisons(data_by_year: dict) -> None:
    """Generate year-to-year comparisons."""
    print_section("YEAR-TO-YEAR COMPARISONS")
    
    years = sorted(data_by_year.keys())
    
    for i in range(len(years) - 1):
        year_a, year_b = years[i], years[i + 1]
        comp = descriptive.compare_years(
            data_by_year[year_a], data_by_year[year_b], year_a, year_b
        )
        
        print(f"\n📈 {year_a} vs {year_b}:")
        print("-" * 70)
        
        ta, tb = comp['total_events']
        print(f"  Total events:   {year_a}={ta:3d}, {year_b}={tb:3d} → Δ {tb - ta:+3d}")
        
        aa, ab = comp['avg_per_month']
        print(f"  Avg/month:      {year_a}={aa:4.2f}, {year_b}={ab:4.2f} → Δ {ab - aa:+.2f}")
        
        sa, sb = comp['std_dev']
        print(f"  Std deviation:  {year_a}={sa:4.2f}, {year_b}={sb:4.2f}")
        
        ca, cb = comp['cv']
        print(f"  CV (%):         {year_a}={ca:4.2f}, {year_b}={cb:4.2f}")
        
        print(f"  Jaccard similarity: {comp['jaccard_days']}")
        
        print(f"\n  Top 3 days - {year_a}: {comp[year_a]['top3']} | {year_b}: {comp[year_b]['top3']}")
        print(f"  Bottom 3 days - {year_a}: {comp[year_a]['bottom3']} | {year_b}: {comp[year_b]['bottom3']}")


def report_advanced_analysis(data_by_year: dict) -> None:
    """Generate advanced statistical analysis."""
    print_section("ADVANCED STATISTICAL ANALYSIS")
    
    # Year-over-year trend
    print_subsection("📊 Year-Over-Year Trend")
    trend = advanced.year_over_year_trend(data_by_year)
    print(f"  Years: {trend['years']}")
    print(f"  Totals: {trend['totals']}")
    print(f"  Trend: {trend['trend'].upper()}")
    print(f"  Slope: {trend['slope']:.4f} (p-value: {trend['p_value']:.4f})")
    print(f"  R-squared: {trend['r_squared']:.4f}")
    print(f"  Statistically significant: {'YES ✓' if trend['significant'] else 'NO ✗'}")
    
    # Seasonality
    print_subsection("🌊 Seasonality Analysis (ANOVA)")
    seasonality = advanced.seasonality_anova(data_by_year)
    print(f"  F-statistic: {seasonality['f_statistic']:.4f}")
    print(f"  p-value: {seasonality['p_value']:.4f}")
    print(f"  Result: {seasonality['interpretation']}")
    print(f"\n  Monthly statistics:")
    for m_stat in seasonality['month_stats']:
        month_name = descriptive.MONTHS[m_stat['month'] - 1] if m_stat['month'] <= 12 else f"Month {m_stat['month']}"
        print(f"    {month_name:12s}: μ={m_stat['mean']:5.2f}, σ={m_stat['stdev']:5.2f}, "
              f"range=[{m_stat['min']:2d}, {m_stat['max']:2d}]")
    
    # Day distribution
    print_subsection("📅 Day Distribution Analysis")
    for year in sorted(data_by_year.keys()):
        day_dist = advanced.day_distribution_analysis(data_by_year[year])
        print(f"\n  {year}:")
        print(f"    Unique days: {day_dist['total_unique_days']}")
        print(f"    Most common: day {day_dist['most_common_day']} ({day_dist['most_common_count']} times)")
        print(f"    Least common: day {day_dist['least_common_day']} ({day_dist['least_common_count']} times)")
        print(f"    First week:  {day_dist['first_week_events']:3d} | Second week: {day_dist['second_week_events']:3d} | "
              f"Third week: {day_dist['third_week_events']:3d}")
    
    # Correlations
    print_subsection("🔗 Year-to-Year Correlations")
    correlations = advanced.correlation_between_years(data_by_year)
    for corr in correlations['correlations']:
        print(f"  {corr['pair']}: r = {corr['correlation']:6.3f} ({corr['relationship']} relationship)")
    print(f"  Average correlation: {correlations['average_correlation']:.3f}")
    
    # Normality test
    print_subsection("📊 Normality Test (Shapiro-Wilk)")
    for year in sorted(data_by_year.keys()):
        norm_test = advanced.normality_test(data_by_year[year])
        status = "✓ Normal" if norm_test['normal'] else "✗ Non-normal"
        print(f"  {year}: p-value = {norm_test['p_value']:.4f} {status}")
    
    # Predictive summary
    print_subsection("🔮 Predictive Summary")
    pred = advanced.predictive_summary(data_by_year)
    print(f"  Overall trend direction: {pred['trend_direction'].upper()}")
    print(f"  Trend is statistically significant: {'YES ✓' if pred['trend_significance'] else 'NO ✗'}")
    print(f"  Seasonality detected: {'YES ✓' if pred['seasonality_detected'] else 'NO ✗'}")
    print(f"  Expected annual total (based on recent years): {pred['expected_annual_total']:.0f} events")


def report_comparative_analysis(data_by_year: dict) -> None:
    """Generate comparative analysis."""
    print_section("COMPARATIVE ANALYSIS")
    
    years = sorted(data_by_year.keys())
    
    # First vs Last year
    if len(years) > 1:
        print_subsection(f"First Year vs Last Year ({years[0]} vs {years[-1]})")
        comp = descriptive.compare_years(
            data_by_year[years[0]], data_by_year[years[-1]], years[0], years[-1]
        )
        
        ta, tb = comp['total_events']
        print(f"  Total events change: {ta} → {tb} ({((tb - ta) / ta * 100):+.1f}%)")
        
        aa, ab = comp['avg_per_month']
        print(f"  Average/month change: {aa:.2f} → {ab:.2f}")
        
        print(f"  Jaccard similarity: {comp['jaccard_days']} (0=completely different, 1=identical)")


def main():
    """Main execution function."""
    print("\n" + "=" * 70)
    print("  🎯 ANALYSIS CONTEO v2.0 - Event Data Analysis System")
    print("=" * 70)
    
    try:
        # Load data
        logger.info("Loading data from JSON...")
        data_by_year = load_events_data()
        logger.info(f"Successfully loaded data for years: {sorted(data_by_year.keys())}")
        
        # Generate reports
        report_descriptive_stats(data_by_year)
        report_aggregate_stats(data_by_year)
        report_year_comparisons(data_by_year)
        report_advanced_analysis(data_by_year)
        report_comparative_analysis(data_by_year)
        
        # Generate visualizations
        print_section("GENERATING VISUALIZATIONS")
        viz_advanced.generate_all_plots(data_by_year, output_dir='outputs')
        
        print_section("ANALYSIS COMPLETE ✓")
        print("Check the 'outputs/' folder for generated visualizations.\n")
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
