from typing import Dict, List

# Months labels
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

# Datasets by year
from .conteo import (
    data_2020,
    data_2021,
    data_2022,
    data_2023,
    data_2024,
    data_2025,
)

DATA_BY_YEAR: Dict[int, List[List[int]]] = {
    2020: data_2020,
    2021: data_2021,
    2022: data_2022,
    2023: data_2023,
    2024: data_2024,
    2025: data_2025,
}
