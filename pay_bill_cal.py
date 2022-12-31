import numpy as np
import datetime
from base import Loan_record
from PySide6.QtCore import QDate
from base import EQUAL_INTEREST_str, EQUAL_PRINCIPAL_str
# 月利率=年利率 ÷ 12
# 日利率=月利率 ÷ 30
# 日利率=年利率 ÷ 360


# 等额本金equal principal
# 等额本金计算公式：每月还款金额 =（贷款本金 ÷ 还款月数）+（本金 — 已归还本金累计额）×每月利率
def equal_principal(principal, payback_months, Monthly_interest_rate, pay_period=1) -> tuple[list[float], list[float], list[float]]:
    payment_all = []
    unpaid_balance = principal
    principal_paid_monthly = principal/payback_months
    for i in range(payback_months):
        interest_paid_monthly = unpaid_balance*Monthly_interest_rate*pay_period
        r = principal_paid_monthly+interest_paid_monthly
        payment_all.append(r)
        unpaid_balance -= principal_paid_monthly
    payment_principal = [principal_paid_monthly]*payback_months
    payment_interest = np.array(payment_all)-np.array(payment_principal)
    return payment_all, payment_principal, list(payment_interest)


# 等额本息equal interest
# 等额本息计算公式：〔贷款本金×月利率×(1＋月利率)^还款月数〕÷〔(1＋月利率)^还款月数 - 1〕
def equal_interest(principal, payback_months, Monthly_interest_rate) -> tuple[list[float], list[float], list[float]]:
    payment_all = []
    payment_interest = []
    payment_principal = []
    principal_to_pay = principal
    for i in range(payback_months):
        r = principal*Monthly_interest_rate * \
            (1+Monthly_interest_rate)**payback_months / \
            ((1+Monthly_interest_rate)**payback_months-1)
        payment_all.append(r)
        payment_interest.append(principal_to_pay*Monthly_interest_rate)
        payment_principal.append(r-payment_interest[-1])
        principal_to_pay -= payment_principal[-1]
    return payment_all, payment_principal, payment_interest


class EQUAL_PRINCIPAL(EQUAL_PRINCIPAL_str):
    target: callable = equal_principal


class EQUAL_INTEREST(EQUAL_INTEREST_str):
    target: callable = equal_interest


class PaymentCalculator:
    def __init__(self, bill_paid_startdate: QDate,
                 pay_period: int,
                 loan_list: list[Loan_record],
                 year_interest: float,
                 payback_months: int,
                 payback_method) -> None:
        self.paid_startdate = bill_paid_startdate
        self.pay_period = pay_period
        self.loan_list = loan_list
        self.payback_method = payback_method
        self.year_interest = year_interest
        self.month_interest = year_interest/12
        self.payback_months = payback_months

    def early_interest(self) -> float:
        # 前期总利息（开始还款之前产生的利息）
        interest_before_pay_start = 0
        for loan in self.loan_list:
            month = (self.paid_startdate.year()-loan.date.year())*12 + \
                (self.paid_startdate.month()-loan.date.month())
            assert month > 0, "还款日必须在借款时间之后"
            month -= 1
            interest_before_pay_start += month*self.month_interest*loan.amount
        return interest_before_pay_start

    def launch(self) -> tuple[np.ndarray[float],np.ndarray[float],np.ndarray[float],np.ndarray[float]]:
        if self.payback_method is EQUAL_INTEREST:
            target = equal_interest
        elif self.payback_method is EQUAL_PRINCIPAL:
            target = equal_principal
        else:
            assert False, "Unsupported payback method!"
        payment_all = np.zeros(shape=(self.payback_months), dtype=float)
        payment_principal = np.zeros(shape=(self.payback_months), dtype=float)
        payment_interest = np.zeros(shape=(self.payback_months), dtype=float)
        early_interest = np.ones(shape=(
            self.payback_months), dtype=float)*self.early_interest()/self.payback_months
        for loan in self.loan_list:
            r = target(principal=loan.amount,
                       payback_months=self.payback_months,
                       Monthly_interest_rate=self.month_interest)
            payment_all += r[0]
            payment_principal += r[1]
            payment_interest += r[2]
        # spread out early interest equally over entire payback months
        payment_all += self.early_interest()/self.payback_months
        return payment_all, payment_principal, payment_interest, early_interest
