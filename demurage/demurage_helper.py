def amount_per_day(day, rates):
    return rates.filter(start_day_gte=day, end_day__lte=day).amount