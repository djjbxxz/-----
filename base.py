from PySide6.QtCore import QDate


class Loan_record:
    def __init__(self, date: QDate, amount: int) -> None:
        assert isinstance(date, QDate) and isinstance(
            amount, int), "Wrong type!!"
        self.date: QDate = date
        self.amount: int = amount

class Force_two_decimal(float):
    # For currency only
    def __str__(self):
        return f'{self:.2f}'  