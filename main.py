from .data import DATA_BY_YEAR
from .stats import (
    view_data,
    avg_unique_days,
    common_days_across_years,
    std_dev_events_per_month,
    compare_years,
)


def run():
    # Per-year summaries
    for year in sorted(DATA_BY_YEAR.keys()):
        print(year, ':', sep='')
        view_data(DATA_BY_YEAR[year])
        print('-----------------------------------')

    # Aggregate analyses
    years_data = [DATA_BY_YEAR[y] for y in sorted(DATA_BY_YEAR.keys())]
    print(f'Average unique days per year: {avg_unique_days(years_data)}')
    print(f'Days appearing in all years: {common_days_across_years(years_data)}')
    print('Standard deviation of events per month:')
    for year in sorted(DATA_BY_YEAR.keys()):
        print(f'  {year}: {std_dev_events_per_month(DATA_BY_YEAR[year])}')

    # Adjacent comparisons
    years = sorted(DATA_BY_YEAR.keys())
    print('-----------------------------------')
    print('Adjacent year comparisons:')
    for a, b in zip(years, years[1:]):
        comp = compare_years(DATA_BY_YEAR[a], DATA_BY_YEAR[b], a, b)
        ta, tb = comp['total_events']
        aa, ab = comp['avg_per_month']
        print(f'Comparison {a} vs {b}:')
        print(f"  Total events: {a}={ta}, {b}={tb} (Δ {tb - ta:+d})")
        print(f"  Avg/month:   {a}={aa}, {b}={ab} (Δ {round(ab - aa, 2):+})")
        print(f"  Jaccard(similarity of unique days): {comp['jaccard_days']}")
        print(f"  Top3 days {a}: {comp[a]['top3']} | {b}: {comp[b]['top3']}")
        print(f"  Bottom3 days {a}: {comp[a]['bottom3']} | {b}: {comp[b]['bottom3']}")


if __name__ == '__main__':
    run()
