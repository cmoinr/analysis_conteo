"""Advanced statistical analysis for event data."""

import statistics
from typing import Dict, List, Tuple, Optional
from scipy import stats as scipy_stats
from scipy.stats import linregress, f_oneway, mannwhitneyu
import numpy as np

from .descriptive import total_per_month, total_avg, total


def linear_trend(data: List[List[int]]) -> Dict:
    """
    Calculate linear regression trend across months.
    
    Args:
        data: List of 12 months with daily events
        
    Returns:
        Dictionary with slope, intercept, r-value, p-value
    """
    counts = total_per_month(data)
    x = np.arange(len(counts))
    y = np.array(counts)
    
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    
    return {
        'slope': round(slope, 4),
        'intercept': round(intercept, 4),
        'r_squared': round(r_value ** 2, 4),
        'r_value': round(r_value, 4),
        'p_value': round(p_value, 4),
        'std_err': round(std_err, 4),
        'trend': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'flat',
        'significant': p_value < 0.05,
    }


def year_over_year_trend(years_data: Dict[int, List[List[int]]]) -> Dict:
    """
    Calculate trend of total events across years.
    
    Args:
        years_data: Dictionary with year -> data mapping
        
    Returns:
        Dictionary with regression results
    """
    sorted_years = sorted(years_data.keys())
    totals = [total(years_data[year]) for year in sorted_years]
    
    x = np.arange(len(sorted_years))
    y = np.array(totals)
    
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    
    return {
        'years': sorted_years,
        'totals': totals,
        'slope': round(slope, 4),
        'intercept': round(intercept, 4),
        'r_squared': round(r_value ** 2, 4),
        'r_value': round(r_value, 4),
        'p_value': round(p_value, 4),
        'std_err': round(std_err, 4),
        'trend': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'flat',
        'significant': p_value < 0.05,
    }


def seasonality_anova(years_data: Dict[int, List[List[int]]]) -> Dict:
    """
    Use ANOVA to test if months have significantly different event counts.
    
    H0: All months have the same mean
    H1: At least one month differs significantly
    
    Args:
        years_data: Dictionary with year -> data mapping
        
    Returns:
        Dictionary with ANOVA results and month statistics
    """
    if not years_data:
        return {}
    
    # Collect events per month across all years
    month_groups = [[] for _ in range(12)]
    
    for year_data in years_data.values():
        for month_idx, month_events in enumerate(year_data):
            month_groups[month_idx].append(len(month_events))
    
    # Perform ANOVA
    f_stat, p_value = f_oneway(*month_groups)
    
    # Calculate statistics per month
    month_stats = []
    for month_idx, group in enumerate(month_groups):
        if group:
            month_stats.append({
                'month': month_idx + 1,
                'mean': round(statistics.mean(group), 2),
                'stdev': round(statistics.stdev(group), 2) if len(group) > 1 else 0.0,
                'min': min(group),
                'max': max(group),
            })
    
    return {
        'f_statistic': round(f_stat, 4),
        'p_value': round(p_value, 4),
        'significant': p_value < 0.05,
        'month_stats': month_stats,
        'interpretation': (
            'Strong seasonality detected' if p_value < 0.05 
            else 'No significant seasonality'
        ),
    }


def bootstrap_confidence_interval(data: List[List[int]], 
                                   n_bootstrap: int = 10000,
                                   confidence: float = 0.95) -> Dict:
    """
    Calculate bootstrap confidence interval for mean events per month.
    
    Args:
        data: List of 12 months with daily events
        n_bootstrap: Number of bootstrap samples
        confidence: Confidence level (0.95 for 95% CI)
        
    Returns:
        Dictionary with CI bounds and original mean
    """
    counts = total_per_month(data)
    original_mean = total_avg(data)
    
    bootstrap_means = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(counts, size=len(counts), replace=True)
        bootstrap_means.append(np.mean(sample))
    
    alpha = 1 - confidence
    lower = np.percentile(bootstrap_means, (alpha / 2) * 100)
    upper = np.percentile(bootstrap_means, (1 - alpha / 2) * 100)
    
    return {
        'original_mean': round(original_mean, 2),
        'lower_ci': round(lower, 2),
        'upper_ci': round(upper, 2),
        'confidence_level': confidence,
        'bootstrap_mean': round(np.mean(bootstrap_means), 2),
        'bootstrap_std': round(np.std(bootstrap_means), 2),
    }


def day_distribution_analysis(data: List[List[int]]) -> Dict:
    """
    Analyze how events are distributed across days of month (1-31).
    
    Args:
        data: List of 12 months with daily events
        
    Returns:
        Dictionary with distribution statistics
    """
    all_days = [d for m in data for d in m]
    day_counts = {}
    
    for day in range(1, 32):
        count = all_days.count(day)
        if count > 0:
            day_counts[day] = count
    
    if not day_counts:
        return {'message': 'No data available'}
    
    counts_list = list(day_counts.values())
    
    return {
        'total_unique_days': len(day_counts),
        'total_occurrences': sum(counts_list),
        'mean_per_day': round(statistics.mean(counts_list), 2),
        'median_per_day': round(statistics.median(counts_list), 2),
        'stdev_per_day': round(statistics.stdev(counts_list), 2) if len(counts_list) > 1 else 0.0,
        'most_common_day': max(day_counts, key=day_counts.get),
        'most_common_count': max(day_counts.values()),
        'least_common_day': min(day_counts, key=day_counts.get),
        'least_common_count': min(day_counts.values()),
        'first_week_events': sum(v for k, v in day_counts.items() if 1 <= k <= 7),
        'second_week_events': sum(v for k, v in day_counts.items() if 8 <= k <= 14),
        'third_week_events': sum(v for k, v in day_counts.items() if 15 <= k <= 21),
        'fourth_week_events': sum(v for k, v in day_counts.items() if 22 <= k <= 28),
        'end_month_events': sum(v for k, v in day_counts.items() if 29 <= k <= 31),
    }


def correlation_between_years(years_data: Dict[int, List[List[int]]]) -> Dict:
    """
    Calculate Pearson correlation between adjacent years' monthly patterns.
    
    Args:
        years_data: Dictionary with year -> data mapping
        
    Returns:
        Dictionary with correlation matrix and statistics
    """
    sorted_years = sorted(years_data.keys())
    
    correlations = []
    
    for i in range(len(sorted_years) - 1):
        year1 = sorted_years[i]
        year2 = sorted_years[i + 1]
        
        counts1 = np.array(total_per_month(years_data[year1]))
        counts2 = np.array(total_per_month(years_data[year2]))
        
        corr = round(np.corrcoef(counts1, counts2)[0, 1], 4)
        
        correlations.append({
            'pair': f'{year1}-{year2}',
            'correlation': corr,
            'relationship': classify_correlation(corr),
        })
    
    return {
        'correlations': correlations,
        'average_correlation': round(statistics.mean([c['correlation'] for c in correlations]), 4),
    }


def classify_correlation(corr: float) -> str:
    """Classify correlation strength."""
    abs_corr = abs(corr)
    if abs_corr >= 0.7:
        return 'strong'
    elif abs_corr >= 0.5:
        return 'moderate'
    elif abs_corr >= 0.3:
        return 'weak'
    else:
        return 'very weak/none'


def mann_whitney_test(data_a: List[List[int]], 
                      data_b: List[List[int]]) -> Dict:
    """
    Non-parametric Mann-Whitney U test comparing two year distributions.
    
    Useful when data might not be normally distributed.
    H0: Both distributions are the same
    
    Args:
        data_a: First year's data
        data_b: Second year's data
        
    Returns:
        Dictionary with test results
    """
    counts_a = np.array(total_per_month(data_a))
    counts_b = np.array(total_per_month(data_b))
    
    statistic, p_value = mannwhitneyu(counts_a, counts_b, alternative='two-sided')
    
    return {
        'statistic': round(statistic, 4),
        'p_value': round(p_value, 4),
        'significant': p_value < 0.05,
        'interpretation': (
            'Distributions are significantly different' if p_value < 0.05
            else 'No significant difference between distributions'
        ),
    }


def normality_test(data: List[List[int]]) -> Dict:
    """
    Shapiro-Wilk test for normality of monthly event counts.
    
    Args:
        data: List of 12 months with daily events
        
    Returns:
        Dictionary with test results
    """
    counts = np.array(total_per_month(data))
    
    statistic, p_value = scipy_stats.shapiro(counts)
    
    return {
        'statistic': round(statistic, 4),
        'p_value': round(p_value, 4),
        'normal': p_value > 0.05,
        'interpretation': (
            'Data appears normally distributed' if p_value > 0.05
            else 'Data significantly deviates from normality'
        ),
    }


def predictive_summary(years_data: Dict[int, List[List[int]]]) -> Dict:
    """
    Generate summary statistics useful for prediction.
    
    Args:
        years_data: Dictionary with year -> data mapping
        
    Returns:
        Dictionary with predictive metrics
    """
    trend = year_over_year_trend(years_data)
    seasonality = seasonality_anova(years_data)
    
    sorted_years = sorted(years_data.keys())
    recent_years_data = list(years_data.values())[-3:] if len(years_data) >= 3 else list(years_data.values())
    
    # Calculate average monthly pattern from recent years
    avg_per_month_recent = []
    for month_idx in range(12):
        month_totals = [len(year_data[month_idx]) for year_data in recent_years_data]
        avg_per_month_recent.append(round(statistics.mean(month_totals), 2))
    
    return {
        'trend_direction': trend['trend'],
        'trend_significance': trend['significant'],
        'trend_slope': trend['slope'],
        'seasonality_detected': seasonality['significant'],
        'avg_monthly_pattern_recent': avg_per_month_recent,
        'expected_annual_total': round(sum(avg_per_month_recent), 2),
    }


def comprehensive_analysis(years_data: Dict[int, List[List[int]]]) -> Dict:
    """
    Generate comprehensive advanced analysis report.
    
    Args:
        years_data: Dictionary with year -> data mapping
        
    Returns:
        Dictionary with all advanced statistics
    """
    return {
        'year_trend': year_over_year_trend(years_data),
        'seasonality': seasonality_anova(years_data),
        'correlations': correlation_between_years(years_data),
        'predictive_summary': predictive_summary(years_data),
    }
