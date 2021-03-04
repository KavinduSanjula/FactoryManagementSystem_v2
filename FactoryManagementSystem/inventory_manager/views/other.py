from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from inventory_manager.models import OtherIncome, Expense, Salery, Employee
from inventory_manager.forms import AddOtherIncomeForm, AddExpenseForm, AddEmployeeForm, AddSaleryForm

from user_manager.getuser import get_user

from finance_manager.models import Deposit, Withdraw, CashIn, CashOut, Check
from finance_manager.views import bank, cashflow

#inventory_manager final product section seviews


############## retrive data ###############

#PRODUCT VIEW
@login_required(login_url='/login')
def index(request):
	return render(request,'inventory_manager/other.html')

#SEPCIAL FUNCTION
def calc_total(data):
	total = 0
	for element in data:
		total += element.amount

	return total

@login_required(login_url='/login')
def view_otherincomes(request):
	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']

		recodes = None

		if start_date == '' or end_date == '':
			recodes = OtherIncome.objects.all().order_by('-id')
		else:
			recodes = OtherIncome.objects.filter(date__range=[start_date,end_date]).order_by('-id')

		total = calc_total(recodes)
		return render(request,'inventory_manager/other/other_income.html', {'recodes':recodes, 'total':total})
	
	else:
		recodes = OtherIncome.objects.all().order_by('-id')
		total = calc_total(recodes)
		return render(request,'inventory_manager/other/other_income.html', {'recodes':recodes, 'total':total})

@login_required(login_url='/login')
def view_expenses(request):
	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']

		recodes = None

		if start_date == '' or end_date == '':
			recodes = Expense.objects.all().order_by('-id')
		else:
			recodes = Expense.objects.filter(date__range=[start_date,end_date]).order_by('-id')

		total = calc_total(recodes)
		return render(request,'inventory_manager/other/expenses.html', {'recodes':recodes, 'total':total})
	
	else:
		recodes = Expense.objects.all().order_by('-id')
		total = calc_total(recodes)
		return render(request,'inventory_manager/other/expenses.html', {'recodes':recodes, 'total':total})


@login_required(login_url='/login')
def view_salery(request):
	if request.method == 'POST':
		emp_name = request.POST['emp_name']
		emp_code = request.POST['emp_code']
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']

		recodes = None

		if emp_name != '' and start_date != '' and end_date != '':
			recodes = Salery.objects.filter(employee__name=emp_name, date__range=[start_date,end_date])
		elif emp_code != '' and start_date != '' and end_date != '':
			recodes = Salery.objects.filter(employee__code=emp_code, date__range=[start_date,end_date])
		elif start_date != '' and end_date != '':
			recodes = Salery.objects.filter(date__range=[start_date,end_date])
		elif emp_name != '':
			recodes = Salery.objects.filter(employee__name=emp_name)
		elif emp_code != '':
			recodes = Salery.objects.filter(employee__code=emp_code)
		else:
			recodes = Salery.objects.all()

		total = calc_total(recodes)
		return render(request,'inventory_manager/other/salery.html', {'recodes':recodes.order_by('-id'), 'total':total})

	else:
		recodes = Salery.objects.all()
		total = calc_total(recodes)
		return render(request,'inventory_manager/other/salery.html', {'recodes':recodes.order_by('-id'), 'total':total})


@login_required(login_url='/login')
def view_employes(request):
	if request.method == 'POST':
		emp_name = request.POST['emp_name']
		emp_code = request.POST['emp_code']
		emp_type = request.POST['emp_type']

		recodes = None

		if emp_code != '':
			recodes = Employee.objects.filter(code=emp_code)
		elif emp_name != '':
			recodes = Employee.objects.filter(name=emp_name)
		elif emp_type == 'perm':
			recodes = Employee.objects.filter(is_permenet=True)
		elif emp_type == 'temp':
			recodes = Employee.objects.filter(is_permenet=False)
		else:
			recodes = Employee.objects.all()

		return render(request,'inventory_manager/other/employee.html', {'recodes':recodes.order_by('-id')})
	else:
		recodes = Employee.objects.all()
		return render(request,'inventory_manager/other/employee.html', {'recodes':recodes.order_by('-id')})
		

@login_required(login_url='/login')
def add_otherincome(request, id=0):
	if request.method == 'POST':
		if id == 0:
			form = AddOtherIncomeForm(request.POST)
		else:
			instance = OtherIncome.objects.get(pk=id)
			form = AddOtherIncomeForm(request.POST,instance=instance)

		payment_accepted = False

		if form.is_valid():
			other_income = form.save(commit=False)

			payment_method = other_income.payment_method
			ref_num = other_income.ref_num
			eff_date = other_income.eff_date

			if payment_method.name.lower() == 'credit':
				payment_accepted = True
				other_income.paid = False
			elif payment_method.name.lower() == 'cash':
				payment_accepted = True
				#add cash in
				desc = f'Other Income: {other_income.name}'
				cash_in = CashIn(desc=desc,date=other_income.date,amount=other_income.amount)
				cashflow.make_cash_in(cash_in)
				other_income.paid = True

			elif payment_method.name.lower() == 'check':
				if ref_num == None or eff_date == None:
					payment_accepted = False
				else:
					payment_accepted = True
					#add check to check table
					check = Check(date=other_income.date,ref_num=ref_num,eff_date=eff_date,amount=other_income.amount)
					check.save()
					other_income.paid = True
			else:
				payment_accepted = True
				#add deposit
				desc = f'Othe Income: {other_income.name}'
				deposit = Deposit(account=other_income.account, desc=desc, date=other_income.date, amount=other_income.amount, payment_method=other_income.payment_method)
				bank.make_deposit(deposit)
				other_income.paid = True

			if payment_accepted:
				other_income.save()
			else:
				messages.add_message(request,messages.WARNING, 'Invalid Payment Details')

		return redirect('/inventory-manager/other-incomes/')
	else:
		form = None
		if id == 0:
			form = AddOtherIncomeForm()
		else:
			instance = OtherIncome.objects.get(pk=id)
			form = AddOtherIncomeForm(instance=instance)
		context = {'form':form, 'formname':'Add Other Income'}
		return render(request,'inventory_manager/other/form_template.html', context)

@login_required(login_url='/login')
def delete_otherincome(request, id=0):
	user = get_user(request)
	if not user.is_superuser:
		return redirect('/fobiddn/')

	if request.method == 'POST':
		other_income = OtherIncome.objects.get(pk=id)
		delete_accepted = False

		if other_income.payment_method.name.lower() == 'credit':
			delete_accepted = True
		elif other_income.payment_method.name.lower() == 'credit':
			delete_accepted = True
		elif other_income.payment_method.name.lower() == 'cash':
			delete_accepted = True
			# add cash out
			desc = f'Other Income Revert: {other_income.name}'
			cash_out = CashOut(desc=desc,date=other_income.date,amount=other_income.amount)
			cashflow.make_cash_out(cash_out)
		elif other_income.payment_method.name.lower() == 'check':
			if other_income.account == None:
				delete_accepted = False
			else:
				delete_accepted = True
				# add withdraw
				desc = f'Returned Check: {other_income.ref_num}'
				withdraw = Withdraw(account=other_income.account, 
									desc=desc, 
									date=other_income.date, 
									amount=other_income.amount, 
									payment_method=other_income.payment_method, 
									ref_num=other_income.ref_num)
				bank.make_withdraw(withdraw)
		else:
			if other_income.account == None:
				delete_accepted = False
			else:
				delete_accepted = True
				# add withdraw
				desc = f'Other Income Revert: {other_income.ref_num}'
				withdraw = Withdraw(account=other_income.account, 
									desc=desc, 
									date=other_income.date, 
									amount=other_income.amount, 
									payment_method=other_income.payment_method, 
									ref_num=other_income.ref_num)
				bank.make_withdraw(withdraw)

		if delete_accepted:
			other_income.delete()
		messages.add_message(request,messages.WARNING, 'Somthing went wrong!')
		return redirect('/inventory-manager/other-incomes/')


@login_required(login_url='/login')
def add_expense(request, id=0):
	if request.method == 'POST':
		if id == 0:
			form = AddExpenseForm(request.POST)
		else:
			instance = Expense.objects.get(pk=id)
			form = AddExpenseForm(request.POST, instance=instance)

		payment_accepted = False

		if form.is_valid():
			expense = form.save(commit=False)

			payment_method = expense.payment_method
			ref_num = expense.ref_num
			eff_date = expense.eff_date
			if payment_method.name.lower() == 'credit':
				payment_accepted = True
				expense.paid = False
			elif payment_method.name.lower() == 'cash':
				payment_accepted = True
				#add cash out
				desc = f'Expense Payment: {expense.name}'
				cash_out = CashOut(desc=desc,date=expense.date,amount=expense.amount)
				cashflow.make_cash_out(cash_out)
				expense.paid = True

			elif payment_method.name.lower() == 'check':
				if ref_num == None or eff_date == None:
					payment_accepted = False
				else:
					payment_accepted = True
					# make Withdraw
					desc = f'Expense Check Payment: {expense.ref_num}'
					withdraw = Withdraw(account=expense.account, 
										desc=desc, 
										date=expense.date, 
										amount=expense.amount, 
										payment_method=expense.payment_method, 
										ref_num=expense.ref_num)
					bank.make_withdraw(withdraw)
					expense.paid = True
			else:
				payment_accepted = True
				#make withdraw
				desc = f'Expense Payment: {expense.name}'
				withdraw = Withdraw(account=expense.account, 
									desc=desc, 
									date=expense.date, 
									amount=expense.amount, 
									payment_method=expense.payment_method, 
									ref_num=expense.ref_num)
				bank.make_withdraw(withdraw)
				expense.paid = True

			if payment_accepted:
				expense.save()
			else:
				messages.add_message(request,messages.WARNING, 'Invalid Payment Details')

		return redirect('/inventory-manager/expenses/')
	else:
		if id == 0:
			form = AddExpenseForm()
		else:
			instance = Expense.objects.get(pk=id)
			form = AddExpenseForm(instance=instance)
		context = {'form':form, 'formname':'Add Expense'}
		return render(request,'inventory_manager/other/form_template.html', context)

@login_required(login_url='/login')
def delete_expense(request, id=0):
	user = get_user(request)
	if not user.is_superuser:
		return redirect('/fobiddn/')

	if request.method == 'POST':
		expense = Expense.objects.get(pk=id)
		delete_accepted = False

		if expense.payment_method.name.lower() == 'credit':
			delete_accepted = True
		elif expense.payment_method.name.lower() == 'cash':
			delete_accepted = True
			# add cash out
			desc = f'Expense Revert: {expense.name}'
			cash_in = CashIn(desc=desc,date=expense.date,amount=expense.amount)
			cashflow.make_cash_in(cash_in)
		elif expense.payment_method.name.lower() == 'check':
			if expense.account == None:
				delete_accepted = False
			else:
				delete_accepted = True
				# add deposit
				desc = f'Returned Check: {expense.ref_num}'
				deposit = Deposit(account=expense.account, 
									desc=desc, 
									date=expense.date, 
									amount=expense.amount, 
									payment_method=expense.payment_method, 
									ref_num=expense.ref_num)
				bank.make_withdraw(deposit)
		else:
			if expense.account == None:
				delete_accepted = False
			else:
				delete_accepted = True
				# add deposit
				desc = f'Expense Revert: {expense.ref_num}'
				deposit = Deposit(account=expense.account, 
									desc=desc, 
									date=expense.date, 
									amount=expense.amount, 
									payment_method=expense.payment_method, 
									ref_num=expense.ref_num)
				bank.make_withdraw(deposit)

		if delete_accepted:
			expense.delete()
		else:
			messages.add_message(request,messages.WARNING, 'Somthing went wrong!')
		return redirect('/inventory-manager/expenses/')

@login_required(login_url='/login')
def add_salery(request, id=0):
	if request.method == 'POST':
		if id == 0:
			form = AddSaleryForm(request.POST)
		else:
			salery = Salery.objects.get(pk=id)
			form = AddSaleryForm(request.POST, instance=salery)

		payment_accepted = False

		if form.is_valid():
			salery = form.save(commit=False)

			worked_days = salery.worked_days
			rate = salery.rate

			leave_ddt = salery.leave_ddt
			other_ddt = salery.other_ddt
			other_payments = salery.other_payments

			if salery.employee.is_permenet:
				salery_amount = salery.employee.basic_salery

			else:
				if worked_days == None or rate == None:
					payment_accepted = False
					return redirect('/inventory-manager/salery/')
				else:
					salery_amount = rate * worked_days


			if other_payments:
				salery_amount += other_payments

			if leave_ddt:
				salery_amount -= leave_ddt

			if other_ddt:
				salery_amount -= other_ddt

			#adding salery
			salery.amount = salery_amount


			payment_method = salery.payment_method
			ref_num = salery.ref_num
			eff_date = salery.eff_date

			if payment_method.name.lower() == 'credit':
				payment_accepted = True
				salery.paid = False
			elif payment_method.name.lower() == 'cash':
				payment_accepted = True
				#add cash out
				desc = f'Salery Payment: emp_code - {salery.employee.code}'
				cash_out = CashOut(desc=desc,date=salery.date,amount=salery.amount)
				cashflow.make_cash_out(cash_out)
				salery.paid = True

			elif payment_method.name.lower() == 'check':
				if ref_num == None or eff_date == None:
					payment_accepted = False
				else:
					payment_accepted = True
					# make Withdraw
					desc = f'Salery Check Payment: emp_code - {salery.employee.code}'
					withdraw = Withdraw(account=salery.account, 
										desc=desc, 
										date=salery.date, 
										amount=salery.amount, 
										payment_method=salery.payment_method, 
										ref_num=salery.ref_num)
					bank.make_withdraw(withdraw)
					salery.paid = True
			else:
				payment_accepted = True
				#make withdraw
				desc = f'Salery Payment: emp_code - {salery.employee.code}'
				withdraw = Withdraw(account=salery.account, 
									desc=desc, 
									date=salery.date, 
									amount=salery.amount, 
									payment_method=salery.payment_method, 
									ref_num=salery.ref_num)
				bank.make_withdraw(withdraw)
				salery.paid = True

			if payment_accepted:
				salery.save()
			else:
				messages.add_message(request,messages.WARNING, 'Invalid Payment Details')

		return redirect('/inventory-manager/salery/')
	else:
		if id == 0:
			form = AddSaleryForm()
		else:
			salery = Salery.objects.get(pk=id)
			form = AddSaleryForm(instance=salery)

		context = {'formname':'Add Salery', 'form':form}
		return render(request,'inventory_manager/other/form_template.html', context)


@login_required(login_url='/login')
def delete_salery(request, id=0):
	user = get_user(request)
	if not user.is_superuser:
		return redirect('/fobiddn/')
		
	if request.method == 'POST':
		salery = Salery.objects.get(pk=id)
		delete_accepted = False

		if salery.payment_method.name.lower() == 'credit':
			delete_accepted = True
		elif salery.payment_method.name.lower() == 'cash':
			delete_accepted = True
			# add cash out
			desc = f'Salery Revert: emp_code - {salery.employee.code}'
			cash_in = CashIn(desc=desc,date=salery.date,amount=salery.amount)
			cashflow.make_cash_in(cash_in)
		elif salery.payment_method.name.lower() == 'check':
			if salery.account == None:
				delete_accepted = False
			else:
				delete_accepted = True
				# add deposit
				desc = f'Salery Returnd Check: emp_code - {salery.employee.code}'
				deposit = Deposit(account=salery.account, 
									desc=desc, 
									date=salery.date, 
									amount=salery.amount, 
									payment_method=salery.payment_method, 
									ref_num=salery.ref_num)
				bank.make_withdraw(deposit)
		else:
			if salery.account == None:
				delete_accepted = False
			else:
				delete_accepted = True
				# add deposit
				desc = f'Salery Revert: emp_code - {salery.employee.code}'
				deposit = Deposit(account=salery.account, 
									desc=desc, 
									date=salery.date, 
									amount=salery.amount, 
									payment_method=salery.payment_method, 
									ref_num=salery.ref_num)
				bank.make_withdraw(deposit)

		if delete_accepted:
			salery.delete()
		else:
			messages.add_message(request,messages.WARNING, 'Somthing went wrong!')
		return redirect('/inventory-manager/salery/')


@login_required(login_url='/login')
def add_employee(request, id=0):
	if request.method == 'POST':
		if id == 0:
			form = AddEmployeeForm(request.POST)
		else:
			employee = Employee.objects.get(pk=id)
			form = AddEmployeeForm(request.POST, instance=employee)

		if form.is_valid():
			form.save()

		return redirect('/inventory-manager/employes/')
	else:
		if id == 0:
			form = AddEmployeeForm()
		else:
			employee = Employee.objects.get(pk=id)
			form = AddEmployeeForm(instance=employee)

		context = {'formname':'Add Employee', 'form':form}
		return render(request,'inventory_manager/other/form_template.html', context)

