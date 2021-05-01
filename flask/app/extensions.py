from flask_sqlalchemy import SQLAlchemy
import csv
from io import TextIOWrapper
from secrets import choice
import string
from pathlib import Path
db = SQLAlchemy()


# класс для обслуживания файла ДБ
class ServiceDB():
    @staticmethod
    def get_path_url(entry, filename):
        cwd = Path(entry).parent
        return f"sqlite:///{str(cwd.joinpath(filename))}"

    @staticmethod
    def gen_key():
        return ''.join([choice(string.ascii_letters + string.digits) for _ in range(20)])


def read_csv(file):
    csvfile = TextIOWrapper(file, "cp1251", errors='ignore', newline=None)
    next(csvfile)
    fieldnames = ['order_type', 'worker', 'operation', 'data_start', 'data_end',
                  'work_hours', 'place_code', 'unit', 'subunit', 'status']
    reader = csv.DictReader(csvfile, fieldnames=fieldnames,
                            delimiter=';', skipinitialspace=True)
    # тут должна быть нормализация
    gen = [row for row in reader]
    return gen
