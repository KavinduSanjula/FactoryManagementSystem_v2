from django.contrib import admin
from .models import PaymentMethod, PettyCashIssue, PettyCash, PettyCashExpense, Cash, CashIn, CashOut, Bank, Check, Deposit, Withdraw, Profit, ProjectionCashIn, ProjectionCashOut

admin.site.register(PaymentMethod)
admin.site.register(PettyCashIssue)
admin.site.register(PettyCash)
admin.site.register(PettyCashExpense)
admin.site.register(Cash)
admin.site.register(CashIn)
admin.site.register(CashOut)
admin.site.register(Bank)
admin.site.register(Check)
admin.site.register(Deposit)
admin.site.register(Withdraw)
admin.site.register(Profit)
admin.site.register(ProjectionCashIn)
admin.site.register(ProjectionCashOut)

