"""Advanced visualizations for event data."""

from typing import List, Dict
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

from ..data.loader import MONTHS
from ..stats.descriptive import total_per_month
from ..stats import advanced

# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)


def plot_heatmap_days_vs_years(years_data: Dict[int, List[List[int]]], 
                               save_path: str = None, show: bool = True) -> None:
    """
    Plot heatmap showing intensity of events across months and years.
    
    Args:
        years_data: Dictionary with year -> data mapping
        save_path: Path to save figure
        show: Whether to display plot
    """
    sorted_years = sorted(years_data.keys())
    months_range = list(range(1, 13))
    
    # Create data matrix (years x months)
    data_matrix = []
    for year in sorted_years:
        data_matrix.append(total_per_month(years_data[year]))
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    im = sns.heatmap(data_matrix, xticklabels=MONTHS, yticklabels=sorted_years,
                     cmap='YlOrRd', cbar_kws={'label': 'Events'}, ax=ax,
                     annot=True, fmt='d', linewidths=0.5)
    
    ax.set_title('Event Intensity Heatmap: Years vs Months', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month', fontsize=11)
    ax.set_ylabel('Year', fontsize=11)
    plt.setp(ax.get_xticklabels(), rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_trend_with_regression(years_data: Dict[int, List[List[int]]], 
                               save_path: str = None, show: bool = True) -> None:
    """
    Plot year-over-year totals with linear regression line.
    
    Args:
        years_data: Dictionary with year -> data mapping
        save_path: Path to save figure
        show: Whether to display plot
    """
    trend = advanced.year_over_year_trend(years_data)
    
    years = np.array(trend['years'])
    totals = np.array(trend['totals'])
    x = np.arange(len(years))
    
    # Calculate fitted line
    fitted = trend['intercept'] + trend['slope'] * x
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.scatter(x, totals, s=100, alpha=0.7, label='Actual', color='steelblue')
    ax.plot(x, fitted, 'r--', linewidth=2, label=f'Trend (slope={trend["slope"]:.3f})')
    
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_title(f'Annual Events Trend (p-value: {trend["p_value"]:.4f})', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Year', fontsize=11)
    ax.set_ylabel('Total Events', fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Add annotation
    trend_text = f'Trend: {trend["trend"]}\n$R^2$ = {trend["r_squared"]:.4f}'
    ax.text(0.02, 0.98, trend_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_day_distribution(data: List[List[int]], year: int = None,
                         save_path: str = None, show: bool = True) -> None:
    """
    Plot bar chart showing which days of month are most common.
    
    Args:
        data: List of 12 months with daily events
        year: Year number for title
        save_path: Path to save figure
        show: Whether to display plot
    """
    day_dist = advanced.day_distribution_analysis(data)
    
    all_days = [d for m in data for d in m]
    day_counts = {}
    for day in range(1, 32):
        count = all_days.count(day)
        if count > 0:
            day_counts[day] = count
    
    days = sorted(day_counts.keys())
    counts = [day_counts[d] for d in days]
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    colors = ['red' if d == day_dist['most_common_day'] else 'steelblue' for d in days]
    ax.bar(days, counts, color=colors, alpha=0.7, edgecolor='navy')
    
    year_str = f' - {year}' if year else ''
    ax.set_title(f'Event Distribution by Day of Month{year_str}', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Day of Month', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.set_xticks(range(1, 32, 1))
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_correlation_matrix(years_data: Dict[int, List[List[int]]], 
                            save_path: str = None, show: bool = True) -> None:
    """
    Plot correlation matrix between monthly patterns of years.
    
    Args:
        years_data: Dictionary with year -> data mapping
        save_path: Path to save figure
        show: Whether to display plot
    """
    sorted_years = sorted(years_data.keys())
    
    # Create correlation matrix
    corr_matrix = np.zeros((len(sorted_years), len(sorted_years)))
    
    for i, year1 in enumerate(sorted_years):
        for j, year2 in enumerate(sorted_years):
            data1 = np.array(total_per_month(years_data[year1]))
            data2 = np.array(total_per_month(years_data[year2]))
            corr_matrix[i, j] = np.corrcoef(data1, data2)[0, 1]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                xticklabels=sorted_years, yticklabels=sorted_years,
                center=0, vmin=-1, vmax=1, square=True, ax=ax,
                cbar_kws={'label': 'Correlation'})
    
    ax.set_title('Correlation Matrix: Monthly Patterns Between Years', 
                 fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_kde_comparison(years_data: Dict[int, List[List[int]]], 
                       save_path: str = None, show: bool = True) -> None:
    """
    Plot KDE (kernel density estimation) comparing monthly event distributions.
    
    Args:
        years_data: Dictionary with year -> data mapping
        save_path: Path to save figure
        show: Whether to display plot
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for year in sorted(years_data.keys()):
        counts = total_per_month(years_data[year])
        # Plot KDE
        data = np.array(counts)
        from scipy import stats as scipy_stats
        kde = scipy_stats.gaussian_kde(data)
        x_range = np.linspace(min(data) - 2, max(data) + 2, 100)
        ax.plot(x_range, kde(x_range), label=str(year), linewidth=2)
    
    ax.set_title('Distribution Density: Monthly Events Across Years', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Events per Month', fontsize=11)
    ax.set_ylabel('Density', fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()


def generate_all_plots(years_data: Dict[int, List[List[int]]], 
                      output_dir: str = 'outputs') -> None:
    """
    Generate all visualizations and save to output directory.
    
    Args:
        years_data: Dictionary with year -> data mapping
        output_dir: Directory to save plots
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print("Generating visualizations...")
    
    # Basic plots per year
    for year in sorted(years_data.keys()):
        from ..viz.basic import plot_monthly_totals
        plot_monthly_totals(years_data[year], year, 
                          save_path=str(output_path / f'monthly_totals_{year}.png'),
                          show=False)
        print(f"✓ monthly_totals_{year}.png")
    
    # Comparison plots
    from ..viz.basic import plot_year_comparison, plot_distribution_histogram, plot_box_comparison
    from ..viz.advanced import plot_heatmap_days_vs_years, plot_trend_with_regression
    from ..viz.advanced import plot_day_distribution, plot_correlation_matrix, plot_kde_comparison
    
    plot_year_comparison(years_data, 
                        save_path=str(output_path / 'year_comparison.png'),
                        show=False)
    print("✓ year_comparison.png")
    
    plot_distribution_histogram(years_data,
                               save_path=str(output_path / 'distribution_histogram.png'),
                               show=False)
    print("✓ distribution_histogram.png")
    
    plot_box_comparison(years_data,
                       save_path=str(output_path / 'box_comparison.png'),
                       show=False)
    print("✓ box_comparison.png")
    
    plot_heatmap_days_vs_years(years_data,
                              save_path=str(output_path / 'heatmap_intensity.png'),
                              show=False)
    print("✓ heatmap_intensity.png")
    
    plot_trend_with_regression(years_data,
                              save_path=str(output_path / 'trend_analysis.png'),
                              show=False)
    print("✓ trend_analysis.png")
    
    plot_day_distribution(years_data[sorted(years_data.keys())[-1]],
                         year=sorted(years_data.keys())[-1],
                         save_path=str(output_path / 'day_distribution_recent.png'),
                         show=False)
    print("✓ day_distribution_recent.png")
    
    plot_correlation_matrix(years_data,
                           save_path=str(output_path / 'correlation_matrix.png'),
                           show=False)
    print("✓ correlation_matrix.png")
    
    plot_kde_comparison(years_data,
                       save_path=str(output_path / 'kde_comparison.png'),
                       show=False)
    print("✓ kde_comparison.png")
    
    print(f"\nAll visualizations saved to {output_path}/")
