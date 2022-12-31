import xlrd
import xlwt
import os
from base import Loan_record
import pathlib
from PySide6.QtCore import QDate
working_dir = pathlib.Path().resolve()
suffix = '.xls'
default_filename = '借款记录'+suffix
filepath = os.path.join(working_dir, default_filename)

# 数据存储格式：第一列是时间，第二列是数值
# Save到当前工作目录


def save(records: list[Loan_record]):
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet("Sheet1")
    for index, record in enumerate(records):
        date = record.date.toPython().strftime("%Y/%m/%d")
        amount = str(record.amount)
        worksheet.write(index, 0, date)
        worksheet.write(index, 1, amount)
    workbook.save(filepath)


def read() -> list[Loan_record]:
    records = []
    data = xlrd.open_workbook(filepath)
    table = data.sheets()[0]
    nrows = table.nrows
    for i in range(nrows):
        date = table.cell_value(i, 0)
        amount = table.cell_value(i, 1)
        records.append(
            Loan_record(QDate(*tuple([int(a)for a in date.split('/')])),
                        int(amount)))
    return records
