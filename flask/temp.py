import csv

csvname = '082020.csv'

with open(csvname, newline='') as csvfile:
    fieldnames = ['order_type', 'worker', 'order_type', 'worker', 'operation', 'data_start', 'data_end', 'work_hours', 'place_code', 'unit','subunit','status']
    reader = csv.DictReader(csvfile, fieldnames=fieldnames,
                            delimiter=';', skipinitialspace=True)
    # тут должна быть нормализация
    return [row for row in reader]
