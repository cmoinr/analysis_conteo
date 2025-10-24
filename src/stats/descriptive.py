"""Descriptive statistics for event data."""

import collections
import statistics
from typing import Dict, List, Tuple

from ..data.loader import MONTHS


def total_per_month(data: List[List[int]]) -> List[int]:
    """
    Calculate total events per month.
    
    Args:
        data: List of 12 months with daily events
        
    Returns:
        List with count for each month
    """
    return [len(m) for m in data]


def total(data: List[List[int]]) -> int:
    """
    Calculate total events across all months.
    
    Args:
        data: List of 12 months with daily events
        
    Returns:
        Total event count
    """
    return sum(len(m) for m in data)


def total_avg(data: List[List[int]]) -> float:
    """
    Calculate average events per month.
    
    Args:
        data: List of 12 months with daily events
        
    Returns:
        Average rounded to 2 decimals
    """
    counts = total_per_month(data)
    return round(sum(counts) / len(counts), 2) if counts else 0.0


def peak_month(data: List[List[int]]) -> str:
    """
    Find month with highest events.
    
    Args:
        data: List of 12 months with daily events
        
    Returns:
        Month name with maximum events
    """
    counts = total_per_month(data)
    idx = max(range(len(counts)), key=lambda i: counts[i])
    return MONTHS[idx]


def lowest_month(data: List[List[int]]) -> str:
    """
    Find month with lowest events.
    
    Args:
        data: List of 12 months with daily events
        
    Returns:
        Month name with minimum events
    """
    counts = total_per_month(data)
    idx = min(range(len(counts)), key=lambda i: counts[i])
    return MONTHS[idx]


def top_repeated_days(data: List[List[int]], n: int = 3) -> List[Tuple[int, int]]:
    """
    Find top N most repeated days with their counts.
    
    Args:
        data: List of 12 months with daily events
        n: Number of top days to return
        
    Returns:
        List of (day, count) tuples, sorted by frequency descending
    """
    flat = [d for m in data for d in m]
    return collections.Counter(flat).most_common(n)


def least_repeated_days(data: List[List[int]], n: int = 3) -> List[Tuple[int, int]]:
    """
    Find N least repeated days with their counts.
    
    Args:
        data: List of 12 months with daily events
        n: Number of least frequent days to return
        
    Returns:
        List of (day, count) tuples, sorted by frequency ascending
    """
    flat = [d for m in data for d in m]
    counter = collections.Counter(flat)
    return sorted(counter.items(), key=lambda x: (x[1], x[0]))[:n]


def unique_days_per_month(data: List[List[int]]) -> List[int]:
    """
    Calculate number of unique days per month.
    
    Args:
        data: List of 12 months with daily events
        
    Returns:
        List with unique day count for each month
    """
    return [len(set(m)) for m in data]


def unique_days_total(data: List[List[int]]) -> int:
    """
    Calculate total unique days across all months.
    
    Args:
        data: List of 12 months with daily events
        
    Returns:
        Count of unique days (1-31)
    """
    return len(set(d for m in data for d in m))


def avg_unique_days(years_data: List[List[List[int]]]) -> float:
    """
    Calculate average unique days per year across all years.
    
    Args:
        years_data: List of yearly data
        
    Returns:
        Average rounded to 2 decimals
    """
    all_uniques = [u for data in years_data for u in unique_days_per_month(data)]
    return round(statistics.mean(all_uniques), 2) if all_uniques else 0.0


def common_days_across_years(years_data: List[List[List[int]]]) -> List[int]:
    """
    Find days that appear in all years.
    
    Args:
        years_data: List of yearly data
        
    Returns:
        Sorted list of days present in every year
    """
    if not years_data:
        return []
    sets = [set(d for m in data for d in m) for data in years_data]
    common = set.intersection(*sets)
    return sorted(common)


def std_dev_events_per_month(data: List[List[int]]) -> float:
    """
    Calculate standard deviation of events per month.
    
    Args:
        data: List of 12 months with daily events
        
    Returns:
        Standard deviation rounded to 2 decimals
    """
    counts = total_per_month(data)
    return round(statistics.stdev(counts), 2) if len(counts) > 1 else 0.0


def coefficient_of_variation(data: List[List[int]]) -> float:
    """
    Calculate coefficient of variation (CV = stdev/mean * 100).
    
    Useful for comparing variability across datasets with different means.
    
    Args:
        data: List of 12 months with daily events
        
    Returns:
        CV percentage rounded to 2 decimals
    """
    avg = total_avg(data)
    if avg == 0:
        return 0.0
    
    stdev = std_dev_events_per_month(data)
    return round((stdev / avg) * 100, 2)


def jaccard_similarity_days(a: List[List[int]], b: List[List[int]]) -> float:
    """
    Calculate Jaccard similarity between unique days in two years.
    
    Jaccard = |intersection| / |union|
    
    Args:
        a: First year's data
        b: Second year's data
        
    Returns:
        Similarity score 0.0-1.0, rounded to 2 decimals
    """
    sa = {d for m in a for d in m}
    sb = {d for m in b for d in m}
    union = sa | sb
    return round(len(sa & sb) / len(union), 2) if union else 0.0


def compare_years(a: List[List[int]], b: List[List[int]], 
                  ya: int, yb: int) -> Dict:
    """
    Build comprehensive comparison between two years.
    
    Args:
        a: First year's data
        b: Second year's data
        ya: First year number
        yb: Second year number
        
    Returns:
        Dictionary with comparison metrics
    """
    return {
        'years': (ya, yb),
        'total_events': (total(a), total(b)),
        'avg_per_month': (total_avg(a), total_avg(b)),
        'std_dev': (std_dev_events_per_month(a), std_dev_events_per_month(b)),
        'cv': (coefficient_of_variation(a), coefficient_of_variation(b)),
        'jaccard_days': jaccard_similarity_days(a, b),
        ya: {
            'top3': top_repeated_days(a),
            'bottom3': least_repeated_days(a),
            'unique_days': unique_days_total(a),
        },
        yb: {
            'top3': top_repeated_days(b),
            'bottom3': least_repeated_days(b),
            'unique_days': unique_days_total(b),
        },
    }


def view_data(data: List[List[int]], year: int = None) -> None:
    """
    Print comprehensive year summary.
    
    Args:
        data: List of 12 months with daily events
        year: Year number (for display)
    """
    year_str = f" ({year})" if year else ""
    print(f'Total: {total(data)}{year_str}')
    print(f'Total AVG: {total_avg(data)}/month')
    print(f'Total per months: {total_per_month(data)}')
    print(f'Highest month: {peak_month(data)}')
    print(f'Lowest month: {lowest_month(data)}')
    print(f'Top 3 repeated days: {top_repeated_days(data)}')
    print(f'Bottom 3 least frequent days: {least_repeated_days(data)}')
    print(f'Unique days per month: {unique_days_per_month(data)}')
    print(f'Standard deviation: {std_dev_events_per_month(data)}')
    print(f'Coefficient of variation: {coefficient_of_variation(data)}%')
