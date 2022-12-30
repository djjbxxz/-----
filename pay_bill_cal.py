import numpy as np
import time
import datetime
import calendar
from base import Loan_record
from PySide6.QtCore import QDate
datetime.datetime.now()
#月利率=年利率 ÷ 12
#日利率=月利率 ÷ 30
#日利率=年利率 ÷ 360
Annual_interest_rate = 0.04  # 4%
Monthly_interest_rate = Annual_interest_rate/12

principal = 100000
payback_months = 24


# 等额本金equal principal
# 等额本金计算公式：每月还款金额 =（贷款本金 ÷ 还款月数）+（本金 — 已归还本金累计额）×每月利率
def equal_principal(principal, payback_months, Monthly_interest_rate, pay_period=1) -> list[float]:
    payment = []
    unpaid_balance = principal
    principal_paid_monthly = principal/payback_months
    for i in range(payback_months):
        interest_paid_monthly = unpaid_balance*Monthly_interest_rate*pay_period
        r = principal_paid_monthly+interest_paid_monthly
        payment.append(r)
        unpaid_balance -= principal_paid_monthly
    return payment


# 等额本息equal interest
# 等额本息计算公式：〔贷款本金×月利率×(1＋月利率)^还款月数〕÷〔(1＋月利率)^还款月数 - 1〕
def equal_interest_payment(principal, payback_months, Monthly_interest_rate) -> list[float]:
    payment = []
    for i in range(payback_months):
        r = principal*Monthly_interest_rate * \
            (1+Monthly_interest_rate)**payback_months / \
            ((1+Monthly_interest_rate)**payback_months-1)
        payment.append(r)
    return payment


class A:
    def __init__(self, bill_paid_startdate: QDate,
                 pay_period: int, loan_list: list[Loan_record], year_interest: float, payback_months: int) -> None:
        self.paid_startdate = bill_paid_startdate
        self.pay_period = pay_period
        self.loan_list = loan_list
        # self.payment_method = payment_method
        self.year_interest = year_interest
        self.month_interest = year_interest/12
        self.payback_months = payback_months

    def launch(self):
        #Equal principal
        # 前期利息（开始还款之前产生的利息）
        interest_before_pay_start = 0
        payment = np.zeros(shape=(self.payback_months), dtype=float)
        for loan in self.loan_list:
            month = (self.paid_startdate.year()-loan.date.year())*12 + \
                (self.paid_startdate.month()-loan.date.month())
            if month > 0:
                month -= 1
            interest_before_pay_start += month*self.month_interest*loan.amount

        for loan in self.loan_list:
            payment += equal_principal(principal=loan.amount,
                                       payback_months=self.payback_months,
                                       Monthly_interest_rate=self.month_interest)
        payment+=interest_before_pay_start/self.payback_months
        return payment
        pass


if __name__ == "__main__":
    print(np.array(equal_principal(principal, payback_months, Monthly_interest_rate)))
    print("--------------")
    print(equal_interest_payment(principal, payback_months, Monthly_interest_rate))
