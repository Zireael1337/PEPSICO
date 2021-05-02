
import re
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class SAPModel(db.Model):
    __tablename__ = 'sap'
    id = db.Column(db.Integer, primary_key=True)
    order_type = db.Column(db.String, nullable=False)
    worker = db.Column(db.String, nullable=False)
    operation = db.Column(db.String, nullable=True)
    data_start = db.Column(db.DateTime, nullable=True)
    data_end = db.Column(db.DateTime, nullable=True)
    work_hours = db.Column(db.Integer, nullable=False)
    place_code = db.Column(db.String, nullable=False)
    unit = db.Column(db.String, nullable=False)
    subunit = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=False)

    # записать в БД
    def update_sap(data):
        # удаление
        db.session.query(SAPModel).delete()
        db.session.commit()
        # запись
        for row in data:
            row['order_type'] = (lambda x: x.strip().lower() if x else None)(row['order_type'])
            row['worker'] = (lambda x: x.strip().lower() if x else None)(row['worker'])
            row['operation'] = (lambda x: x.strip().lower() if x else None)(row['operation'])
            row['data_start'] = (lambda x: datetime.strptime(x, "%d.%m.%Y") if x else None)(row['data_start'])
            row['data_end'] = (lambda x: datetime.strptime(x, "%d.%m.%Y") if x else None)(row['data_end'])
            row['work_hours'] = (lambda x: x.strip().lower() if x else None)(row['work_hours'])
            row['place_code'] = (lambda x: x.strip().lower() if x else None)(row['place_code'])
            row['unit'] = (lambda x: x.strip().lower() if x else None)(row['unit'])
            row['subunit'] = (lambda x: x.strip().lower() if x else None)(row['subunit'])
            row['status'] = (lambda x: x.strip().lower() if x else None)(row['status'])

            new = SAPModel(**row)
            db.session.add(new)

        db.session.commit()
