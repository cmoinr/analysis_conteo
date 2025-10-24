"""Basic visualizations for event data."""

from typing import List, Dict
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from ..data.loader import MONTHS
from ..stats.descriptive import total_per_month

# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def plot_monthly_totals(data: List[List[int]], year: int, 
                       save_path: str = None, show: bool = True) -> None:
    """
    Plot bar chart of total events per month.
    
    Args:
        data: List of 12 months with daily events
        year: Year number for title
        save_path: Path to save figure (optional)
        show: Whether to display plot
    """
    totals = total_per_month(data)
    months = MONTHS[:len(data)]
    
    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(months, totals, color='steelblue', alpha=0.8, edgecolor='navy')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9)
    
    ax.set_title(f'Total Events per Month - {year}', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month', fontsize=11)
    ax.set_ylabel('Number of Events', fontsize=11)
    ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_year_comparison(years_data: Dict[int, List[List[int]]], 
                        save_path: str = None, show: bool = True) -> None:
    """
    Plot line chart comparing monthly patterns across years.
    
    Args:
        years_data: Dictionary with year -> data mapping
        save_path: Path to save figure
        show: Whether to display plot
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    months_range = range(1, 13)
    
    for year in sorted(years_data.keys()):
        totals = total_per_month(years_data[year])
        ax.plot(months_range, totals, marker='o', label=str(year), linewidth=2)
    
    ax.set_title('Monthly Events Trend Across Years', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month', fontsize=11)
    ax.set_ylabel('Number of Events', fontsize=11)
    ax.set_xticks(months_range)
    ax.set_xticklabels(MONTHS, rotation=45)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_distribution_histogram(years_data: Dict[int, List[List[int]]], 
                               save_path: str = None, show: bool = True) -> None:
    """
    Plot histogram of events per month distribution.
    
    Args:
        years_data: Dictionary with year -> data mapping
        save_path: Path to save figure
        show: Whether to display plot
    """
    all_counts = []
    
    for year_data in years_data.values():
        all_counts.extend(total_per_month(year_data))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(all_counts, bins=15, color='steelblue', alpha=0.7, edgecolor='navy')
    
    ax.axvline(sum(all_counts) / len(all_counts), color='red', 
               linestyle='--', linewidth=2, label=f'Mean: {sum(all_counts) / len(all_counts):.1f}')
    
    ax.set_title('Distribution of Monthly Event Counts', fontsize=14, fontweight='bold')
    ax.set_xlabel('Events per Month', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_box_comparison(years_data: Dict[int, List[List[int]]], 
                       save_path: str = None, show: bool = True) -> None:
    """
    Plot box plot comparing distributions across years.
    
    Args:
        years_data: Dictionary with year -> data mapping
        save_path: Path to save figure
        show: Whether to display plot
    """
    data_list = []
    labels = []
    
    for year in sorted(years_data.keys()):
        data_list.append(total_per_month(years_data[year]))
        labels.append(str(year))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bp = ax.boxplot(data_list, labels=labels, patch_artist=True)
    
    # Color boxes
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
        patch.set_alpha(0.7)
    
    ax.set_title('Distribution Comparison Across Years', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year', fontsize=11)
    ax.set_ylabel('Events per Month', fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()
