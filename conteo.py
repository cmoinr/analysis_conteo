import collections
import matplotlib.pyplot as plt
import statistics

data_2020 = [
    [3, 9, 11, 13, 15, 17, 17, 20],
    [6, 7, 9, 14, 14, 18, 18, 19],
    [7, 9, 10, 18, 22, 25, 30],
    [6, 11, 13, 14, 18, 24],
    [5, 7, 18, 18, 21, 25, 26],
    [1, 1, 4, 9, 9, 15, 18, 19, 23, 27, 29],
    [3, 3, 12, 13, 20, 20, 22, 27, 29, 31, 31],
    [1, 4, 4, 6, 14, 15, 15, 18, 21, 21, 25, 26, 29],
    [1, 1, 5, 9, 12, 17, 19, 21, 22, 26, 27, 29, 30],
    [6, 7, 9, 15, 16, 18, 20, 21, 22, 24, 24],
    [2, 3, 4, 5, 6, 12, 14, 14, 16, 19, 23, 26, 30],
    [1, 1, 3, 3, 6, 8, 10, 15, 17, 18, 18, 24, 24, 26, 27, 27, 27, 29, 31]
]

data_2021 = [
    [2, 3, 6, 9, 9, 15, 16, 20, 21, 25, 26, 27],
    [4, 5, 13, 15, 15, 16, 20, 24, 25, 25],
    [4, 6, 7, 10, 10, 16, 17, 20, 24, 27, 28, 30, 31],
    [2, 5, 6, 15, 15, 17, 20, 20, 22, 23, 28, 28, 30],
    [1, 3, 4, 7, 11, 11, 14, 17, 21, 24, 25, 31],
    [3, 4, 7, 11, 15, 19, 23, 24, 28],
    [2, 4, 5, 11, 12, 15, 16, 21, 23, 24, 28],
    [2, 6, 9, 10, 13, 16, 22, 22, 23, 24, 27, 29],
    [3, 4, 5, 6, 10, 10, 10, 11, 12, 19, 20, 21, 26, 27],
    [1, 1, 3, 4, 5, 7, 9, 10, 11, 13, 16, 17, 22, 23, 24, 29, 31],
    [3, 5, 5, 10, 12, 13, 14, 15, 16, 18, 20, 22, 22, 25, 25, 30, 30],
    [2, 6, 7, 9, 10, 13, 17, 19, 20, 22, 24, 26, 27, 27, 29, 30]
]

data_2022 = [
    [1, 3, 5, 5, 7, 9, 14, 18, 24, 24, 27, 29, 29, 30, 31],
    [8, 8, 10, 11, 15, 17, 17, 24, 25, 25, 26],
    [2, 3, 7, 8, 9, 10, 14, 18, 18, 21, 22, 23, 26, 26],
    [1, 4, 6, 7, 19, 20, 26],
    [3, 5, 9, 9, 12, 16, 18, 23, 25],
    [1, 2, 5, 7, 9, 12, 14, 17, 21, 22, 22, 23, 27],
    [4, 7, 8, 9, 12, 19, 21, 25, 26, 31],
    [1, 1, 4, 9, 10, 11, 11, 17, 20, 26, 31],
    [2, 9, 11, 13, 14, 15, 19, 30],
    [1, 2, 6, 13, 14, 18, 22, 24, 28, 29, 31],
    [3, 4, 13, 14, 14, 17, 17, 18, 26, 28],
    [4, 5, 6, 8, 9, 10, 12, 17, 20, 20, 21, 28, 30, 31]
]

data_2023 = [
    [1, 3, 4, 5, 7, 8, 12, 13, 15, 18, 18, 19, 21, 23, 25, 26, 28, 29],
    [2, 2, 4, 5, 9, 11, 14, 15, 19, 19, 24, 27, 28],
    [2, 6, 9, 11, 15, 16, 18, 20, 25, 25, 28, 30],
    [3, 4, 9, 13, 18, 25, 26, 30],
    [4, 7, 8, 10, 11, 14, 16, 16, 20, 23, 25, 25, 27, 30, 30],
    [1, 5, 8, 8, 12, 14, 15, 16, 16, 18, 18, 22, 25, 27, 29, 29],
    [3, 6, 6, 12, 13, 17, 18, 18, 21, 22, 24, 25, 26, 27, 28, 29],
    [1, 3, 5, 6, 7, 8, 9, 9, 12, 13, 19, 19, 21, 25, 30],
    [1, 3, 5, 5, 10, 11, 14, 17, 23, 24, 24, 27, 29],
    [1, 3, 7, 9, 11, 11, 12, 20, 21, 24, 26, 30, 31],
    [1, 3, 7, 10, 15, 23, 24, 25, 27, 29],
    [8, 9, 11, 11, 12, 19, 21, 23, 26, 30, 31]
]

data_2024 = [
    [2, 3, 5, 9, 10, 12, 21, 23, 26, 30, 31],
    [6, 9, 9, 11, 11, 15, 16, 17, 25, 26],
    [1, 2, 4, 7, 7, 8, 9, 11, 15, 15, 16, 19, 25, 28, 29, 31],
    [4, 5, 6, 7, 16, 16, 20, 21, 26, 29],
    [1, 2, 7, 9, 13, 14, 15, 20, 20, 20, 22, 24, 26, 29, 31],
    [6, 6, 9, 10, 13, 13, 17, 21, 23, 25, 26, 29],
    [5, 7, 14, 17, 18, 20, 25, 27, 28, 30, 31],
    [3, 7, 9, 14, 18, 21, 22, 25, 28],
    [1, 4, 7, 12, 16, 17, 18, 19, 22, 29],
    [1, 4, 5, 8, 9, 11, 16, 19, 23, 24, 27, 31],
    [3, 9, 10, 15, 17, 17, 21, 22, 24, 26, 28],
    [3, 5, 7, 7, 9, 14, 20, 21, 22, 24, 30, 31]
]

data_2025 = [
    [6, 7, 10, 13, 17, 18, 24, 26, 28, 30],
    [3, 6, 7, 9, 10, 10, 15, 17, 18, 21, 22, 25, 25, 26, 27],
    [4, 5, 8, 10, 10, 10, 11, 14, 14, 15, 21, 22, 25, 28, 30, 30],
    [2, 3, 6, 7, 10, 12, 19, 19, 30],
    [1, 3, 5, 5, 7, 10, 11, 16, 18, 20, 24, 26],
    [4, 6, 6, 11, 14, 16, 23, 26, 27, 28, 30],
    [2, 4, 5, 6, 12, 12, 17, 19, 25, 26, 30],
    [3, 7, 9, 10, 13, 14, 16, 19, 25, 28, 29, 30, 30],
    [1, 2, 5, 10, 20, 20, 22, 23, 24, 29, 30]
]

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def total_avg(data):
    """Calculate the data average"""
    total = []
    for month in data:
        total.append(len(month))

    acum = 0
    for month in range(len(total)):
        acum += total[month]
    average = acum / len(data)
    
    return round(average, 2)


def total_per_month(data):
    """Calcute the total data per each month"""
    total = []
    for i in range(len(data)):
        total.append(len(data[i]))
        # total.append(f'{MONTHS[i]}: {len(data[i])}')
    
    return total


def total(data):
    """Calculate data total quantity"""
    acum = 0
    for i in data:
        acum += len(i)

    return acum


def peak_month(data):
    """Find the month with highest quantity data"""
    ordered = total_per_month(data)
    ordered.sort(reverse=True)
    highest = ordered[0]

    months = total_per_month(data)
    for month in range(len(months)):
        if months[month] == highest:
            month_index = month
   
    return MONTHS[month_index]


def lowest_month(data):
    """Find the month with lowest quantity data"""
    ordered = total_per_month(data)
    ordered.sort()
    lowest = ordered[0]

    months = total_per_month(data)
    for month in range(len(months)):
        if months[month] == lowest:
            month_index = month
   
    return MONTHS[month_index]


def top_repeated_days(data):
    """Find the top 3 most repeated days and their counts"""
    flat = [day for month in data for day in month]
    counter = collections.Counter(flat)
    top3 = counter.most_common(3)
    return top3

def least_repeated_days(data, n: int = 3):
    """Find the n days with the fewest occurrences, counting zeros."""
    flat = [day for month in data for day in month]
    counter = collections.Counter(flat)
    all_days = [(day, counter.get(day, 0)) for day in range(1, 32)]
    all_days.sort(key=lambda x: (x[1], x[0]))
    return all_days[:n]


def unique_days_per_month(data):
    """Calculate the number of unique days per month"""
    unique_counts = []
    for month in data:
        unique_counts.append(len(set(month)))
    return unique_counts


def plot_monthly_totals(data, year):
    """Plot a bar chart of total events per month"""
    totals = total_per_month(data)
    months = MONTHS[:len(data)]  # In case not all 12 months
    plt.figure(figsize=(10, 5))
    plt.bar(months, totals, color='skyblue')
    plt.title(f'Total Events per Month - {year}')
    plt.xlabel('Month')
    plt.ylabel('Total Events')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def avg_unique_days(years_data):
    """Calculate average unique days per year across all years"""
    all_uniques = []
    for data in years_data:
        uniques = unique_days_per_month(data)
        all_uniques.extend(uniques)
    return round(statistics.mean(all_uniques), 2)


def common_days_across_years(years_data):
    """Find days that appear in all years"""
    if not years_data:
        return set()
    # Get unique days per year
    year_sets = [set(day for month in data for day in month) for data in years_data]
    # Intersect all
    common = set.intersection(*year_sets)
    return sorted(list(common))


def jaccard_similarity_days(data_a, data_b):
    """Jaccard similarity between the sets of unique days in two years."""
    set_a = {d for m in data_a for d in m}
    set_b = {d for m in data_b for d in m}
    union = set_a | set_b
    if not union:
        return 0.0
    inter = set_a & set_b
    return round(len(inter) / len(union), 2)


def compare_years(data_a, data_b, year_a, year_b):
    """Build a comparison summary between two years."""
    comp = {
        'years': (year_a, year_b),
        'total_events': (total(data_a), total(data_b)),
        'avg_per_month': (total_avg(data_a), total_avg(data_b)),
        'jaccard_days': jaccard_similarity_days(data_a, data_b),
        'top3_days': {year_a: top_repeated_days(data_a), year_b: top_repeated_days(data_b)},
        'bottom3_days': {year_a: least_repeated_days(data_a), year_b: least_repeated_days(data_b)}
    }
    return comp


def print_year_comparison(data_a, data_b, year_a, year_b):
    comp = compare_years(data_a, data_b, year_a, year_b)
    print(f'Comparison {year_a} vs {year_b}:')
    ta, tb = comp['total_events']
    aa, ab = comp['avg_per_month']
    print(f"  Total events: {year_a}={ta}, {year_b}={tb} (Δ {tb - ta:+d})")
    print(f"  Avg/month:   {year_a}={aa}, {year_b}={ab} (Δ {round(ab - aa, 2):+})")
    print(f"  Jaccard(similarity of unique days): {comp['jaccard_days']}")
    print(f"  Top3 days {year_a}: {comp['top3_days'][year_a]} | {year_b}: {comp['top3_days'][year_b]}")
    print(f"  Bottom3 days {year_a}: {comp['bottom3_days'][year_a]} | {year_b}: {comp['bottom3_days'][year_b]}")
    

def std_dev_events_per_month(data):
    """Calculate standard deviation of events per month"""
    totals = total_per_month(data)
    if len(totals) < 2:
        return 0.0
    return round(statistics.stdev(totals), 2)


def view_data(data):
    """View all data analysis"""
    print(f'Total: {total(data)}')
    print(f'Total AVG: {total_avg(data)}/month')
    print(f'Total per months: {total_per_month(data)}')
    print(f'Highest month: {peak_month(data)}')
    print(f'Lowest month: {lowest_month(data)}')
    print(f'Top 3 repeated days: {top_repeated_days(data)}')
    print(f'Bottom 3 least frequent days: {least_repeated_days(data)}')
    print(f'Unique days per month: {unique_days_per_month(data)}')


print('2020:')
view_data(data_2020)
print('-----------------------------------')
print('2021:')
view_data(data_2021)
print('-----------------------------------')
print('2022:')
view_data(data_2022)
print('-----------------------------------')
print('2023:')
view_data(data_2023)
print('-----------------------------------')
print('2024:')
view_data(data_2024)
print('-----------------------------------')
print('2025:')
view_data(data_2025)

# Uncomment to generate plots (requires GUI environment)
# plot_monthly_totals(data_2020, '2020')
# plot_monthly_totals(data_2021, '2021')
# plot_monthly_totals(data_2024, '2024')
# plot_monthly_totals(data_2025, '2025')

# Additional analyses
years_data = [data_2020, data_2021, data_2022, data_2023, data_2024, data_2025]
print('-----------------------------------')
print(f'Average unique days per year: {avg_unique_days(years_data)}')
print(f'Days appearing in all years: {common_days_across_years(years_data)}')
print('Standard deviation of events per month:')
for year, data in zip([2020, 2021, 2022, 2023, 2024, 2025], years_data):
    print(f'  {year}: {std_dev_events_per_month(data)}')

print('-----------------------------------')
print('Adjacent year comparisons:')
year_map = {
    2020: data_2020,
    2021: data_2021,
    2022: data_2022,
    2023: data_2023,
    2024: data_2024,
    2025: data_2025,
}
ordered_years = sorted(year_map.keys())
for prev, curr in zip(ordered_years, ordered_years[1:]):
    print_year_comparison(year_map[prev], year_map[curr], prev, curr)

print('-----------------------------------')
print('Long-span comparison:')
print_year_comparison(year_map[2020], year_map[2025], 2020, 2025)