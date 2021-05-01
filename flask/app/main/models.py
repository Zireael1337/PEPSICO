
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

    # запись в БД
    def save_sap(data):
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

            print(row)
            new = SAPModel(**row)
            db.session.add(new)

        db.session.commit()




    # запись в БД
    def save_sap111(data):
        kwargs = {}
        kwargs['username'] = current_user.username
        kwargs['ref_name'] = form.get('ref_name')
        kwargs['full_name'] =       (lambda x: x.strip().lower().title() if x else None)(form.get('full_name'))
        kwargs['email'] =           (lambda x: x.strip() if x else None)(form.get('email'))
        kwargs['phone_number'] =    (lambda x: re.sub(r'(?<!\d)7', '8', re.sub(r'[ ()+-]', '', x), count=1) if x else None)(form.get('phone_number'))
        kwargs['account'] =         (lambda x: x.strip() if x else None)(form.get('account'))
        kwargs['address'] =         (lambda x: x.strip() if x else None)(form.get('address'))
        kwargs['court_order'] =     (lambda x: x.strip().replace(' ', '') if x else None)(form.get('court_order'))
        kwargs['area'] =            (lambda x: x.strip(' -').replace(',', '.') if x else None)(form.get('area'))
        kwargs['contribution'] =    (lambda x: x.strip(' +').replace(',', '.') if x else None)(form.get('contribution'))
        kwargs['fine'] =            (lambda x: x.strip(' +').replace(',', '.') if x else None)(form.get('fine'))
        kwargs['state_duty'] =      (lambda x: x.strip(' +').replace(',', '.') if x else None)(form.get('state_duty'))
        new_ref = RefModel(**kwargs)
        try:
            db.session.add(new_ref)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return e
        return new_ref.id
