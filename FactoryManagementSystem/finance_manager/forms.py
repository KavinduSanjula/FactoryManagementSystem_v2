from django import forms
from .models import CashIn, CashOut, PettyCashIssue, PettyCashExpense, Bank, Deposit, Withdraw, ProjectionCashIn, ProjectionCashOut, Profit


class CalcProfitForm(forms.Form):
	desc = forms.CharField(max_length=500)
	start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
	end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
	startup_unfinished = forms.DecimalField()
	last_unfinished = forms.DecimalField()
	startup_finished = forms.DecimalField()
	last_finished = forms.DecimalField()
	remarks = forms.CharField(max_length=200, required=False)


class AddCashInForm(forms.ModelForm):
	class Meta:
		model = CashIn
		fields = ('desc', 'date', 'amount', 'remarks')
		widgets = {
			'date':forms.DateInput(attrs={'type':'date'})
		}

class AddCashOutForm(forms.ModelForm):
	class Meta:
		model = CashOut
		fields = ('desc', 'date', 'amount', 'remarks')
		widgets = {
			'date':forms.DateInput(attrs={'type':'date'})
		}

class AddProjectionCashInForm(forms.ModelForm):
	class Meta:
		model = ProjectionCashIn
		fields = ('desc', 'date', 'amount', 'remarks')
		widgets = {
			'date':forms.DateInput(attrs={'type':'date'})
		}

class AddProjectionCashOutForm(forms.ModelForm):
	class Meta:
		model = ProjectionCashOut
		fields = ('desc', 'date', 'amount', 'remarks')
		widgets = {
			'date':forms.DateInput(attrs={'type':'date'})
		}

class PettyCashIssueForm(forms.ModelForm):
	class Meta:
		model = PettyCashIssue
		fields = ('ref_num','date','amount','start_date','end_date','remarks')
		widgets = {
				'date':forms.DateInput(attrs={'type':'date'}),
				'start_date':forms.DateInput(attrs={'type':'date'}),
				'end_date':forms.DateInput(attrs={'type':'date'}),
			}

class AddPettyCashExpenseForm(forms.ModelForm):
	class Meta:
		model = PettyCashExpense
		fields = ('ref_num','desc','date','amount','remarks')
		widgets = {
				'date':forms.DateInput(attrs={'type':'date'})
			}

class AddDepositForm(forms.ModelForm):
	class Meta:
		model = Deposit
		fields = ('account','desc','date','amount','ref_num','payment_method','remarks')
		widgets = {
				'date':forms.DateInput(attrs={'type':'date'})
			}

class AddWithdrawForm(forms.ModelForm):
	class Meta:
		model = Withdraw
		fields = ('account','desc','date','amount','ref_num','payment_method','remarks')
		widgets = {
				'date':forms.DateInput(attrs={'type':'date'})
			}

class AddAccountForm(forms.ModelForm):
	class Meta:
		model = Bank
		fields = ('acc_num', 'acc_name', 'desc','amount')