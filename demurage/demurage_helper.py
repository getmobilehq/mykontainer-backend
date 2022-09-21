def amount_per_day(day, rates):
    return rates.get(start_day__gte=day, end_day__lte=day).price_per_day