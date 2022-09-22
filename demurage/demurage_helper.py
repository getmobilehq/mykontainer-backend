def amount_per_day(day, rates):
    return rates.get(start_day__lte=day, end_day__gte=day).price_per_day