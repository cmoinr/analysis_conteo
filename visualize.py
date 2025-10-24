from typing import List
import matplotlib.pyplot as plt

from .data import MONTHS
from .stats import total_per_month


def plot_monthly_totals(data: List[List[int]], year: str) -> None:
    totals = total_per_month(data)
    months = MONTHS[:len(data)]
    plt.figure(figsize=(10, 5))
    plt.bar(months, totals, color='skyblue')
    plt.title(f'Total Events per Month - {year}')
    plt.xlabel('Month')
    plt.ylabel('Total Events')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
