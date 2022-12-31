from PySide6.QtCore import QDate
from PySide6.QtCore import Qt
from PySide6.QtWidgets import  QTableWidgetItem
class Loan_record:
    def __init__(self, date: QDate, amount: int) -> None:
        assert isinstance(date, QDate) and isinstance(
            amount, int), "Wrong type!!"
        self.date: QDate = date
        self.amount: int = amount
    
    def __repr__(self):
        return f'{self.date.toPython().strftime("%Y/%m/%d"), self.amount}'

class Force_two_decimal(float):
    # For currency only
    def __str__(self):
        return f'{self:.2f}'

class QTableWidgetItem_Uneditable(QTableWidgetItem):

    def __init__(self,*arg) -> None:
        super().__init__(*arg)
        self.setFlags(self.flags() & ~Qt.ItemIsEditable)
        self.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)


class EQUAL_PRINCIPAL_str:
    str = '等额本金'

class EQUAL_INTEREST_str:
    str = '等额本息'