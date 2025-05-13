from datetime import date, timedelta

def get_date_range(start: date, end: date) -> list[date]:
    return [start + timedelta(days=x) for x in range((end - start).days + 1)]
