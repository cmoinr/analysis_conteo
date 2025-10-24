import collections
import statistics
from typing import Dict, List, Tuple

from .data import MONTHS


def total_per_month(data: List[List[int]]) -> List[int]:
    return [len(m) for m in data]


def total(data: List[List[int]]) -> int:
    return sum(len(m) for m in data)


def total_avg(data: List[List[int]]) -> float:
    counts = total_per_month(data)
    return round(sum(counts) / len(counts), 2) if counts else 0.0


def peak_month(data: List[List[int]]) -> str:
    counts = total_per_month(data)
    idx = max(range(len(counts)), key=lambda i: counts[i])
    return MONTHS[idx]


def lowest_month(data: List[List[int]]) -> str:
    counts = total_per_month(data)
    idx = min(range(len(counts)), key=lambda i: counts[i])
    return MONTHS[idx]


def top_repeated_days(data: List[List[int]], n: int = 3) -> List[Tuple[int, int]]:
    flat = [d for m in data for d in m]
    return collections.Counter(flat).most_common(n)


def least_repeated_days(data: List[List[int]], n: int = 3) -> List[Tuple[int, int]]:
    flat = [d for m in data for d in m]
    counter = collections.Counter(flat)
    return sorted(counter.items(), key=lambda x: (x[1], x[0]))[:n]


def unique_days_per_month(data: List[List[int]]) -> List[int]:
    return [len(set(m)) for m in data]


def avg_unique_days(years_data: List[List[List[int]]]) -> float:
    all_uniques = [u for data in years_data for u in unique_days_per_month(data)]
    return round(statistics.mean(all_uniques), 2) if all_uniques else 0.0


def common_days_across_years(years_data: List[List[List[int]]]) -> List[int]:
    if not years_data:
        return []
    sets = [set(d for m in data for d in m) for data in years_data]
    common = set.intersection(*sets)
    return sorted(common)


def std_dev_events_per_month(data: List[List[int]]) -> float:
    counts = total_per_month(data)
    return round(statistics.stdev(counts), 2) if len(counts) > 1 else 0.0


def jaccard_similarity_days(a: List[List[int]], b: List[List[int]]) -> float:
    sa = {d for m in a for d in m}
    sb = {d for m in b for d in m}
    union = sa | sb
    return round(len(sa & sb) / len(union), 2) if union else 0.0


def compare_years(a: List[List[int]], b: List[List[int]], ya: int, yb: int) -> Dict:
    return {
        'years': (ya, yb),
        'total_events': (total(a), total(b)),
        'avg_per_month': (total_avg(a), total_avg(b)),
        'jaccard_days': jaccard_similarity_days(a, b),
        ya: {
            'top3': top_repeated_days(a),
            'bottom3': least_repeated_days(a),
        },
        yb: {
            'top3': top_repeated_days(b),
            'bottom3': least_repeated_days(b),
        },
    }


def view_data(data: List[List[int]]) -> None:
    print(f'Total: {total(data)}')
    print(f'Total AVG: {total_avg(data)}/month')
    print(f'Total per months: {total_per_month(data)}')
    print(f'Highest month: {peak_month(data)}')
    print(f'Lowest month: {lowest_month(data)}')
    print(f'Top 3 repeated days: {top_repeated_days(data)}')
    print(f'Bottom 3 least frequent days: {least_repeated_days(data)}')
    print(f'Unique days per month: {unique_days_per_month(data)}')
