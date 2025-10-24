"""Data loader for JSON event files with validation."""

import json
from pathlib import Path
from typing import Dict, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

EXPECTED_MONTHS = 12
VALID_DAYS_RANGE = (1, 31)


def get_data_path(filename: str = 'events.json') -> Path:
    """Get path to data file relative to this module."""
    current_dir = Path(__file__).parent
    return current_dir.parent.parent / 'data' / 'raw' / filename


def load_events_data(filename: str = 'events.json') -> Dict[int, List[List[int]]]:
    """
    Load event data from JSON file.
    
    Args:
        filename: Name of JSON file in data/raw/
        
    Returns:
        Dictionary with year as key and list of monthly events as value
        
    Raises:
        FileNotFoundError: If data file not found
        json.JSONDecodeError: If JSON is malformed
        ValueError: If data validation fails
    """
    data_path = get_data_path(filename)
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {filename}: {e.msg}", e.doc, e.pos)
    
    # Extract events and validate
    if 'events' not in raw_data:
        raise ValueError("JSON must contain 'events' key")
    
    events = raw_data['events']
    data_by_year = {}
    
    for year_str, monthly_data in events.items():
        try:
            year = int(year_str)
            validated_data = validate_data(monthly_data, year)
            data_by_year[year] = validated_data
        except (ValueError, TypeError) as e:
            logger.warning(f"Skipping year {year_str}: {e}")
            continue
    
    logger.info(f"Loaded data for years: {sorted(data_by_year.keys())}")
    return data_by_year


def validate_data(data: List[List[int]], year: int = None) -> List[List[int]]:
    """
    Validate event data structure.
    
    Args:
        data: List of 12 months, each containing day numbers
        year: Year being validated (for error messages)
        
    Returns:
        Validated data (same structure)
        
    Raises:
        ValueError: If validation fails
    """
    year_str = f"Year {year}: " if year else ""
    
    if not isinstance(data, list):
        raise ValueError(f"{year_str}Data must be a list of months")
    
    if len(data) != EXPECTED_MONTHS:
        raise ValueError(f"{year_str}Expected {EXPECTED_MONTHS} months, got {len(data)}")
    
    validated = []
    for month_idx, month_data in enumerate(data):
        if not isinstance(month_data, list):
            raise ValueError(f"{year_str}Month {month_idx + 1} must be a list")
        
        # Validate each day
        validated_month = []
        for day in month_data:
            if not isinstance(day, int):
                raise ValueError(f"{year_str}Month {month_idx + 1} contains non-integer: {day}")
            
            if not (VALID_DAYS_RANGE[0] <= day <= VALID_DAYS_RANGE[1]):
                raise ValueError(
                    f"{year_str}Month {month_idx + 1} day {day} out of range "
                    f"{VALID_DAYS_RANGE[0]}-{VALID_DAYS_RANGE[1]}"
                )
            
            validated_month.append(day)
        
        validated.append(validated_month)
    
    return validated


def get_data_by_year(data: Dict[int, List[List[int]]], year: int) -> List[List[int]]:
    """
    Get data for a specific year.
    
    Args:
        data: Full data dictionary
        year: Year to retrieve
        
    Returns:
        Monthly data for that year
        
    Raises:
        KeyError: If year not found
    """
    if year not in data:
        available = sorted(data.keys())
        raise KeyError(f"Year {year} not available. Available years: {available}")
    
    return data[year]


def get_years(data: Dict[int, List[List[int]]]) -> List[int]:
    """Get sorted list of available years."""
    return sorted(data.keys())


def get_month_name(month_index: int) -> str:
    """
    Get month name from index (0-11).
    
    Args:
        month_index: Month index (0 = January)
        
    Returns:
        Month name
    """
    if not (0 <= month_index < 12):
        raise ValueError(f"Month index must be 0-11, got {month_index}")
    
    return MONTHS[month_index]


def export_to_json(data: Dict[int, List[List[int]]], output_path: Path) -> None:
    """
    Export data to JSON file.
    
    Args:
        data: Data dictionary
        output_path: Path where to save JSON
    """
    output = {
        'metadata': {
            'description': 'Daily events data collected on a specific day of each month',
            'event_type': 'recurring_monthly_event'
        },
        'events': {str(year): monthly_data for year, monthly_data in data.items()}
    }
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Data exported to {output_path}")
