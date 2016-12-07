data = [
    {'id':u'1','name':u'Jeff'},
    {'id':u'2','name':'Carlo'},
]

import xlwt

w = xlwt.Workbook()
ws = w.add_sheet('sheet1')

columns = list(data[0].keys()) # list() is not need in Python 2.x
for i, row in enumerate(data):
    for j, col in enumerate(columns):
        ws.write(i, j, row[col])

w.save('data.xls')