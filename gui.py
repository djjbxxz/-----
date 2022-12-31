import sys
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication, QTableWidget, QLabel, QDateEdit, QGroupBox,
                               QVBoxLayout, QHBoxLayout, QDialog, QComboBox)
from pay_bill_cal import *
from PySide6.QtCore import QDate
from PySide6.QtCore import Qt
from record_rw import read, save
from utils import isDebug
from base import Force_two_decimal, Loan_record, EQUAL_PRINCIPAL, EQUAL_INTEREST
from base import QTableWidgetItem_Uneditable as QTableWidgetItem

class Payment_record(QDialog):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, payment_plan: np.ndarray, parent=None, title=None):
        super().__init__(parent)
        # if not isDebug():
        #     self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.resize(260, 400)
        self.setWindowTitle(title)
        layout = QVBoxLayout()

        table = QTableWidget()
        table.verticalHeader().setVisible(False)
        table.setRowCount(len(payment_plan))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["期数", "应还数额"])
        for index, i in enumerate(payment_plan):
            num_periods = QTableWidgetItem(str(index+1))
            amount = QTableWidgetItem(str(Force_two_decimal(i)))
            table.setItem(index, 0, num_periods)
            table.setItem(index, 1, amount)
        self.table = table
        layout.addWidget(self.table)
        self.setLayout(layout)


class Load_record_table_widget:

    def __init__(self) -> None:
        self.tabel_widget = QTableWidget()
        self._loan_record: list[Loan_record] = [
            Loan_record(QDate(2020, 1, 1), 10000)]
        self.table_items_widget: dict[Loan_record:tuple[QTableWidgetItem, QTableWidgetItem]] = {
        }
        self.Refresh_widget()
        pass

    def add_record(self, date: QDate, amount: int):
        print(date, amount)
        self._loan_record.append(Loan_record(date, int(amount)))
        self.Refresh_widget()

    def del_record(self):
        for loan_record, item_widgets in self.table_items_widget.items():
            # only work when the whole row is selected
            if all([widget.isSelected() for widget in item_widgets]) == True:
                self._loan_record.remove(loan_record)
        pass
        self.Refresh_widget()

    def Refresh_widget(self):
        self.tabel_widget.setCornerButtonEnabled(True)
        self.table_items_widget.clear()
        # self.loan_table.setVisible(False)
        time_strformat_CHNS = "%Y年%m月%d日"
        self.tabel_widget.setRowCount(len(self._loan_record))
        self.tabel_widget.setColumnCount(2)
        self.tabel_widget.setHorizontalHeaderLabels(["时间", "借款数额"])
        for index, record in enumerate(self._loan_record):
            date: datetime.date = record.date.toPython()
            date_str = date.strftime(time_strformat_CHNS)
            amount = record.amount
            item_date = QTableWidgetItem(date_str)
            item_amount = QTableWidgetItem(str(amount))
            self.tabel_widget.setItem(index, 0, item_date)
            self.tabel_widget.setItem(index, 1, item_amount)
            self.table_items_widget[record] = (item_date, item_amount)
            pass
        self.tabel_widget.setColumnWidth(0, 150)
        self.tabel_widget.scrollToBottom()

        self.print_loan_record()

    def print_loan_record(self):
        for each in self._loan_record:
            print(each)

    def read(self):
        self._loan_record = read()
        self.Refresh_widget()

    def save(self):
        save(self._loan_record)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # if not isDebug():
        #     self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        layout = QVBoxLayout()

        # 还款设置
        payment_setting = QGroupBox("还款设置")
        payment_setting_layout = QHBoxLayout()
        payment_setting.setLayout(payment_setting_layout)
        payment_setting_layout.addWidget(QLabel("还款时间"))
        self._bill_pay_startdate = QDateEdit(
            date=QDate.currentDate(), displayFormat='yyyy/MM')
        payment_setting_layout.addWidget(self._bill_pay_startdate)
        payment_setting_layout.addWidget(QLabel("还款间隔(月)"))
        self._bill_pay_period = QLineEdit("1")
        self._bill_pay_period.setDisabled(True)
        self._bill_pay_period.setFixedWidth(40)
        self._bill_pay_period.setMaxLength(3)
        payment_setting_layout.addWidget(self._bill_pay_period)
        payment_setting_layout.addWidget(QLabel("年利率(%)"))
        self.year_interest = QLineEdit("4")
        self.year_interest.setFixedWidth(50)
        self.year_interest.setMaxLength(4)
        payment_setting_layout.addWidget(self.year_interest)
        payment_setting_layout.addWidget(QLabel("还款期数(月)"))
        self.payback_months = QLineEdit("10")
        self.payback_months.setFixedWidth(50)
        self.payback_months.setMaxLength(4)
        payment_setting_layout.addWidget(self.payback_months)
        payment_setting_layout.addWidget(QLabel("还款方式"))
        self.payment_method = QComboBox()
        self.payment_method.addItems(['等额本金', '等额本息'])
        payment_setting_layout.addWidget(self.payment_method)

        # 添加借款记录
        groupbox_loan_record = QGroupBox("添加借款记录")
        loan_record_layout = QVBoxLayout()
        groupbox_loan_record.setLayout(loan_record_layout)
        add_loan_record = QHBoxLayout()
        loan_record_layout.addLayout(add_loan_record)
        self.loan_table = Load_record_table_widget()

        add_loan_record.addWidget(QLabel("借款时间"))
        self._loan_add_date = QDateEdit(
            date=QDate.currentDate(), displayFormat='yyyy/MM/dd')
        add_loan_record.addWidget(self._loan_add_date)
        add_loan_record.addWidget(QLabel("借款数额(元)"))
        self._loan_add_amount = QLineEdit("0")
        add_loan_record.addWidget(self._loan_add_amount)
        add_record_button = QPushButton("添加(Enter)")
        add_record_button.setShortcut(Qt.Key.Key_Enter)
        add_record_button.clicked.connect(self.add_loan_record)
        add_loan_record.addWidget(add_record_button)
        del_record_button = QPushButton("删除(Del)")
        del_record_button.setShortcut(Qt.Key.Key_Delete)
        del_record_button.clicked.connect(self.loan_table.del_record)
        add_loan_record.addWidget(del_record_button)
        import_button = QPushButton("导入记录")
        import_button.clicked.connect(self.loan_table.read)
        add_loan_record.addWidget(import_button)
        export_button = QPushButton("导出记录")
        export_button.clicked.connect(self.loan_table.save)
        add_loan_record.addWidget(export_button)

        # 借款记录表格
        loan_record_layout.addWidget(self.loan_table.tabel_widget)
        # self._loan_record: list[Loan_record] = self.loan_table._loan_record

        button = QPushButton("计算")
        layout.addWidget(payment_setting)
        layout.addWidget(groupbox_loan_record)
        layout.addWidget(button)

        # Set dialog layout
        self.setLayout(layout)
        button.clicked.connect(self.Calculate)

    def Calculate(self):
        # close last windows (if exists)
        # if hasattr(self, 'payment_widget') and not self.payment_widget is None:
        #     self.payment_widget.close()

        # gather payment configuration
        try:
            pay_startdate = self._bill_pay_startdate.date()
            pay_period = int(self._bill_pay_period.text())
            loan_record = self.loan_table._loan_record
            year_interest = float(self.year_interest.text())/100
            payback_months = int(self.payback_months.text())
        except Exception:
            print('Illegal data!')

        # check data
        legal_flag = True

        # all loan should be borrowed before at least a Interest accrual cycle ago
        for loan in self.loan_table._loan_record:
            if (pay_startdate.toPython()-loan.date.toPython()).days < 30:
                legal_flag = False

        # check illgel flag
        if not legal_flag:
            return

        # call to execute
        calc = PaymentCalculator(bill_paid_startdate=pay_startdate,
                                 pay_period=pay_period,
                                 loan_list=loan_record,
                                 year_interest=year_interest,
                                 payback_months=payback_months)

        # payment method
        text = self.payment_method.currentText()
        if text == EQUAL_INTEREST.str:
            launch = calc.equal_interest
        elif text == EQUAL_PRINCIPAL.str:
            launch = calc.equal_principal
        else:
            launch = None
        # execute
        payment_plan = launch()
        self.payment_widget = Payment_record(
            parent=self,
            payment_plan=payment_plan,
            title=text)
        self.payment_widget.show()

    def add_loan_record(self):
        date = self._loan_add_date.date()
        amount = self._loan_add_amount.text()
        # check input
        try:
            int(amount)
        except:
            return
        self.loan_table.add_record(date, amount)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())
