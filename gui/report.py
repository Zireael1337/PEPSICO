# -*- coding: utf-8 -*-
import re
import numpy as np
import pandas as pd
import sqlite3
from configparser import ConfigParser, Error
from pathlib import Path
import matplotlib.pyplot as plt


def excel_to_df(file_name, sheet_name):
    df = pd.read_excel(io=file_name, sheet_name=sheet_name)
    for i in df.values:
        print(i)
    return df


def get_config():
    config = ConfigParser(allow_no_value=True)
    config['readme'] = {'''
#hpw - working hours per week
#hpm - working hours per month
                        '''.strip(): None}
    config['hpw'] = {'RUSVIT': 40,
                     'GORDMI': 40,
                     'ZHDAND': 40,
                     'GOLOLE': 40,
                     'IVAPET': 40,
                     'STRVLA': 40}
    config['hpm'] = {'RUSVIT': 168,
                     'GORDMI': 152,
                     'ZHDAND': 168,
                     'GOLOLE': 136,
                     'IVAPET': 152,
                     'STRVLA': 136}
    config['report'] = {'week': 1, 'month': 1}
    config['notopo'] = {'notopo':'''
Участие в производственном процессе
Заполнение отчетов/SAP
Помощь оператору в приёме щелочи/кислоты
Формирование заявки на закупку запчастей
Заполнение сопров. докум-ции АСУТПиКИП
Подгот оборудования к отправке в поверку
Прохождение аудита
Обучение/тренинги/аттестация
Подмена оператора/наладчика
Создание заявки в РМЦ
Инвентаризация
Работа в SAP/MyBuy
Совещание
Работы по настройке ПК
Смена формата/настройки после см формата
Работа в командах по улучшению/ЭВРИКА
Распечатка мойки А3Flex (для ЦСП)
Погрузочно-разгрузочные работы
Анализ простоев/мониторинг работы оборуд
Осмотр емкостей/отбор анализов
Анализ алгоритмов работы систем АСУТП
Мойка, чистка, уборка
Прием-передача смены
Осмотр автоцистерн
Работа с документацией, изучение оборуд
Изготовление чертежей/эскизов
Тестирование материалов/форматов и т.п.
Создание заявки на закупку запчастей
Поддержка системы IVAMS
Написание SOPов/инструкций
Постановка оборудования на мойку'''.strip()}
    name = 'report.ini'
    path = Path(name)
    if path.is_file():
        config.read(name, encoding="cp1251")
    else:
        with open(name, 'w') as f:
            config.write(f)
    return config


def df_to_sql(conn, raw_df):
    sql = '''CREATE TABLE IF NOT EXISTS raw {0}'''.format(tuple(raw_df))
    conn.cursor().executescript(sql)
    raw_df.to_sql('raw', conn, if_exists='replace', index=False)
    conn.commit()


def normalization(row):
    if not pd.isna(row):
        #row1 = row
        row = re.sub(r'\s*/\s','/',row)
        row = re.sub(r'\s*[*]\s*','',row)
        row.strip()
        fw = re.match(r'^[а-я]', row)
        if fw:
            row = re.sub(r'^[а-я]', fw[0].upper(), row)
        #if row1 != row:
        #    print(row1)
        #    print(row,'\n')
    return row




def execute_sql(conn, sql):
    r = conn.cursor().execute(sql).fetchall()
    conn.commit()
    return r



def get_data_week(n_week):
    sql = '''select
a.name as 'Сотрудник',
(a.all_work-a.no_topo)*100/(a.week) as 'TOPO',
(a.no_topo)*100/(a.week) as 'НЕTOPO'
from (
select
u.name as name,
u.week*60 as week,
sum(r.ФактичРабота) as all_work,
(sum((select count(name) from notopo where r.КрТекстОперац =name) * r.ФактичРабота)) as no_topo
from users u
JOIN raw r on u.name = lower(r.Рабочее_место)
where r.week = {}
GROUP by r.Рабочее_место) a'''.format(n_week)
    return conn.cursor().execute(sql).fetchall()


def get_data_month(n_month):
    sql = '''select
a.name as 'Сотрудник',
(a.all_work-a.no_topo)*100/(a.month) as 'TOPO',
(a.no_topo)*100/(a.month) as 'НЕ TOPO'
from (
select
u.name as name,
u.month*60 as month,
sum(r.ФактичРабота) as all_work,
(sum((select count(name) from notopo where r.КрТекстОперац =name) * r.ФактичРабота)) as no_topo
from users u
JOIN raw r on u.name = lower(r.Рабочее_место)
where strftime('%m', r.ФактичДатаКонца) = '{}'
GROUP by r.Рабочее_место) a'''.format(n_month)

    return conn.cursor().execute(sql).fetchall()






def create_graph(data_week, data_month):
    width = 0.35       # the width of the bars: can also be len(x) sequence
    fig, (ax1, ax2) = plt.subplots(nrows=2,ncols = 1)
    fig.subplots_adjust(hspace=0.5)
    ax1.set_title('Недельный график')
    ax2.set_title('Месячный график')

    for i,j in zip([ax1, ax2],[data_week, data_month]):
        labels, value1, value2 = [],[],[]
        for data in j:
            labels.append(data[0].upper())
            value1.append(data[1])
            value2.append(data[2])
        i.set_ylim(ymax=120)
        i.bar(labels, value2, width, label='Не TOPO')
        i.bar(labels, value1, width, bottom=value2, label='TOPO')
        i.legend()
        i.grid(axis='y')
        i.set_ylabel('Процент')
        i.set_xlabel('Сотрудник')

    plt.show()
    fig.savefig('report.pdf')


if __name__ == '__main__':
    config = get_config()

    pd.set_option('display.max_rows', None)

    raw_df = excel_to_df('082020.xlsx', 'Сырые данные')
    raw_df.columns = raw_df.columns.str.replace(" ", "_")
    raw_df['week'] = raw_df['ФактичДатаКонца'].dt.week
    raw_df['КрТекстОперац'] = raw_df['КрТекстОперац'].apply(normalization)

    for i in raw_df['КрТекстОперац']:
        normalization(i)


    conn = sqlite3.connect('report.db')
    df_to_sql(conn, raw_df)

    # шлаебонь #########################################
    sql = '''DROP TABLE IF EXISTS "users"'''
    conn.cursor().execute(sql)
    sql = '''CREATE TABLE IF NOT EXISTS "users" ('name' TEXT UNIQUE, 'week' INT, 'month' INT)'''
    conn.cursor().execute(sql)
    conn.commit()
    for i in config.items('hpw'):
        sql = '''INSERT INTO 'users' (name, week) VALUES {}'''.format(i)
        conn.cursor().execute(sql)
    conn.commit()
    for i in config.items('hpm'):
        sql = '''UPDATE 'users' SET month = {1} WHERE name = '{0}' '''.format(i[0], i[1])
        conn.cursor().execute(sql)
    conn.commit()
    ##############################################

    sql = '''CREATE TABLE IF NOT EXISTS "notopo" ('name' TEXT UNIQUE)'''
    conn.cursor().execute(sql)
    for i in config['notopo']['notopo'].split('\n'):
        sql = '''INSERT OR IGNORE INTO 'notopo' (name) VALUES ('{}')'''.format(str(i))
        conn.cursor().execute(sql)
        conn.commit()

    sql = '''select max(r.week)from raw r'''
    n_week = conn.cursor().execute(sql).fetchall()[0][0]
    sql = '''select strftime('%m', max(r.ФактичДатаКонца)) from raw r'''
    n_month = conn.cursor().execute(sql).fetchall()[0][0]

    n_week = 36
    n_month = '08'

    data_week = get_data_week(n_week)
    data_month = get_data_month(n_month)

    create_graph(data_week, data_month)
