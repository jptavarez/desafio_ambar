import datetime
def str_to_date(date, format='%Y-%m-%d'):
    return datetime.datetime.strptime(date, format)