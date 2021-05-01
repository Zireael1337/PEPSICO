# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3


sql = '''
select
r.week as Неделя,
u.name as Сотрудник,
sum(r.ФактичРабота)/60 as Часов,
u.week as Всего,
sum(r.ФактичРабота)*10/(6*u.week) as Процент
from users u
JOIN raw r on u.name = lower(r.Рабочее_место)
WHERE r.week = 36
GROUP by r.Рабочее_место'''

'''
raw_df = excel_to_df('Заказы не TOPO.xlsx', 'Лист1')

topo = set()
for j in raw_df.columns:
    for i in raw_df[j]:
        if not pd.isnull(i):
            topo.add(normalization(i))
'''
