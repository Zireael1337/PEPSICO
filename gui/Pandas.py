import pandas as pd
import matplotlib.pyplot as plt
plt.close('all')

rawdata = pd.read_excel('C:\\Users\\Vitaly\\082020.xlsx', index_col = 0)
sumhour1 = rawdata.groupby("Рабочее место")["ФактичРабота"].sum() / 60
sumhour = pd.DataFrame(data=sumhour1)
promauto = sumhour.loc[["RUSVIT", "GORDMI", "ZHDAND", "GOLOLE","IVAPET", "STRVLA"], :]
promauto.plot(kind='bar');
writer = pd.ExcelWriter('pandas_chart.xlsx', engine='xlsxwriter')
promauto.to_excel(writer, sheet_name='Sheet1')
workbook  = writer.book
worksheet = writer.sheets['Sheet1']
chart = workbook.add_chart({'type': 'column'})
chart.add_series({'values': '=Sheet1!$B$2:$B$8'})
worksheet.insert_chart('D2', chart)
writer.save()
