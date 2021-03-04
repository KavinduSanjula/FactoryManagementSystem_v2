from django import forms
from .models import (Customer, Employee, Sell, OtherSell, SellPayment, Product, ProductIssue, ProductIssueNote, SellDispatch, ProductStock,
					 Supplire, Material, MaterialStock, Buy, BuyPayment, BuyDispatch, MaterialIssue,
					 OtherIncome, Expense, Salery)

class AddCustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ('name','addr','email','phone')
		widgets = {
			'name':forms.TextInput(attrs={'class':'input-text'}),
			'addr':forms.TextInput(attrs={'class':'input-text'}),
			'phone':forms.TextInput(attrs={'class':'input-text'}),
			'email':forms.TextInput(attrs={'class':'input-text'}),
		}

class AddEmployeeForm(forms.ModelForm):
	class Meta:
		model = Employee
		fields = ('code','name','addr','phone','email','is_permenet','basic_salery')
		widgets = {
			'code':forms.TextInput(attrs={'class':'input-text'}),
			'name':forms.TextInput(attrs={'class':'input-text'}),
			'addr':forms.TextInput(attrs={'class':'input-text'}),
			'phone':forms.TextInput(attrs={'class':'input-text'}),
			'email':forms.TextInput(attrs={'class':'input-text'}),
			'basic_salery':forms.TextInput(attrs={'class':'input-text'}),
		}

class AddSaleryForm(forms.ModelForm):
	class Meta:
		model = Salery
		fields = ('date','employee','account','worked_days','rate','other_payments','leave_ddt','other_ddt','payment_method','ref_num','eff_date','remarks')
		widgets = {
			'date':forms.DateInput(attrs={'type':'date'}),
			'eff_date':forms.DateInput(attrs={'type':'date'}),
		}


class AddSaleForm(forms.ModelForm):
	class Meta:
		model = Sell
		fields = ('customer','dispatch_note_num','date')

		widgets = {
			'date':forms.DateInput(attrs={'type':'date'}),
		}

class AddOtherSaleForm(forms.ModelForm):
	class Meta:
		model = OtherSell
		fields = ('customer','dispatch_note_num','account','date', 'payment_method','ref_num','eff_date')

		widgets = {
			'date':forms.DateInput(attrs={'type':'date'}),
			'eff_date':forms.DateInput(attrs={'type':'date'}),
		}


class AddPaymentForm(forms.ModelForm):
	class Meta:
		model = SellPayment
		fields = ('sale','account','date','amount','payment_method','ref_num','eff_date','remarks')

		widgets = {
			'date':forms.DateInput(attrs={'type':'date'}),
			'eff_date':forms.DateInput(attrs={'type':'date'}),
		}

class AddProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ('name',)
		widgets = {'name':forms.TextInput(attrs={'class':'input-text'})}

class AddStockForm(forms.ModelForm):
	class Meta:
		model = ProductIssue
		fields = ('issue_note_num','date','remarks')

		widgets = {
			'date':forms.DateInput(attrs={'type':'date'}),
		}


class AddSellDispatchForm(forms.ModelForm):
	class Meta:
		model = SellDispatch
		fields = ('dispatch_note_num','stock','unit_price','qty')

class AddIssueNoteForm(forms.ModelForm):
	class Meta:
		model = ProductIssueNote
		fields = ('product','issue_note_num','batch_num','qty')



#material section

class AddSupplireForm(forms.ModelForm):
	class Meta:
		model = Supplire
		fields = ('name','addr', 'email','phone')
		widgets = {
			'name':forms.TextInput(attrs={'class':'input-text'}),
			'addr':forms.TextInput(attrs={'class':'input-text'}),
			'phone':forms.TextInput(attrs={'class':'input-text'}),
			'email':forms.EmailInput(attrs={'class':'input-text'}),
		}

class AddMaterialForm(forms.ModelForm):
	class Meta:
		model = Material
		fields = ('name',)
		widgets = {'name':forms.TextInput(attrs={'class':'input-text'})}

class AddMaterialStockForm(forms.ModelForm):
	class Meta:
		model = MaterialStock
		fields = ('material','batch_num','qty')


class AddReceiveForm(forms.ModelForm):
	class Meta:
		model = Buy
		fields = ('supplire','dispatch_note_num','date','grn','invoice','payment_voucher')
		widgets = {
			'date':forms.DateInput(attrs={'type':'date'}),
		}

class AddBuyPaymentForm(forms.ModelForm):
	class Meta:
		model = BuyPayment
		fields = ('buy','account','date','amount','payment_method','ref_num','eff_date','remarks')

		widgets = {
			'date':forms.DateInput(attrs={'type':'date'}),
			'eff_date':forms.DateInput(attrs={'type':'date'}),
		}

class AddBuyDispatchForm(forms.ModelForm):
	class Meta:
		model = BuyDispatch
		fields = ('dispatch_note_num','material','batch_num','unit_price','qty')


class AddIssueForm(forms.ModelForm):
	class Meta:
		model = MaterialIssue
		fields = ('stock', 'date', 'production_batch_number', 'qty', 'remarks')
		widgets = {
			'date':forms.DateInput(attrs={'type':'date'}),
		}

#other

class AddOtherIncomeForm(forms.ModelForm):
	class Meta:
		model = OtherIncome
		fields = ('name','account','date','amount','payment_method','ref_num','eff_date','remarks')
		widgets = {
			'date':forms.DateInput(attrs={'type':'date'}),
			'eff_date':forms.DateInput(attrs={'type':'date'}),
		}

class AddExpenseForm(forms.ModelForm):
	class Meta:
		model = Expense
		fields = ('name','account','date','amount','payment_method','ref_num','eff_date','remarks')
		widgets = {
			'date':forms.DateInput(attrs={'type':'date'}),
		}