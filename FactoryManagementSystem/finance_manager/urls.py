from django.urls import path
from .views import index, profit, bank, cashflow, pettycash, projectioncashflow

urlpatterns = [
	path('',index.index,name='finance-manager'),
	path('profit/',profit.profit,name='profit'),
	path('bank/',bank.bank,name='bank'),
	path('cashflow/',cashflow.cashflow,name='cashflow'),
	path('pettycash/',pettycash.pettycash,name='pettycash'),

	path('calculate-profit/',profit.calc_profit, name='calc-profit'),

	path('bank-add-deposit/',bank.deposit, name='deposit'),
	path('bank-add-withdraw/',bank.withdraw, name='withdraw'),
	path('bank-add-account/',bank.add_account, name='add-account'),

	path('bank-accounts/',bank.accounts, name='accounts'),
	path('bank-deposits/',bank.deposits, name='deposits'),
	path('bank-withdrawals/',bank.withdrawals, name='withdrawals'),

	path('bank-checks/',bank.checks, name='checks'),

	path('cashflow-view-cash-in/',cashflow.view_cash_in, name='view-cash-in'),
	path('cashflow-view-cash-out/',cashflow.view_cash_out, name='view-cash-out'),

	path('cashflow-add-cash-in/',cashflow.add_cash_in, name='cash-in'),
	path('cashflow-add-cash-out/',cashflow.add_cash_out, name='cash-out'),

	path('pettycash-issuings/',pettycash.issuings, name='pettycash-issuings'),
	path('pettycash-add-expense/',pettycash.add_expense, name='pettycash-add-expense'),
	path('pettycash-add-issue/',pettycash.issue_pettycash, name='pettycash-issue'),
	path('pettycash-expenses/',pettycash.expeses, name='pettycash-expenses'),

	path('projectioncashflow/',projectioncashflow.index, name='projectioncashflow'),

	path('projectioncashflow/add-cash-in/',projectioncashflow.add_cash_in, name='projectioncashflow-add-cash-in'),
	path('projectioncashflow/add-cash-out/',projectioncashflow.add_cash_out, name='projectioncashflow-add-cash-out'),

	path('projectioncashflow/cash-ins/',projectioncashflow.view_cash_in, name='projectioncashflow-cash-in'),
	path('projectioncashflow/cash-outs/',projectioncashflow.view_cash_out, name='projectioncashflow-cash-out'),
]