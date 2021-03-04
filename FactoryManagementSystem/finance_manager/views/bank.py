from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user_manager.getuser import get_user

from finance_manager.models import Bank, Deposit, Withdraw, CashIn, CashOut, Check
from finance_manager.views import cashflow
from finance_manager.forms import AddDepositForm, AddWithdrawForm, AddAccountForm

#main view
@login_required(login_url='/login')
def bank(request):
	user = get_user(request)
	if not user.is_staff:
		return redirect('/fobiddn/')

	return render(request,'finance_manager/bank/bank.html')

#SPECIAL FUNCTION
def calc_total(data):
	'''returns total of amounts'''
	total = 0
	for element in data:
		total += element.amount

	return total

#add account
@login_required(login_url='/login')
def add_account(request):

	user = get_user(request)
	if not user.is_staff:
		return redirect('/fobiddn/')

	if request.method == 'POST':
		form = AddAccountForm(request.POST)

		if form.is_valid():
			form.save()

		return redirect('/finance-manager/bank-accounts/')
	else:
		form = AddAccountForm()
		context = {'formname':'Add Account','form':form}
		return render(request,'finance_manager/bank/form_template.html', context)

#make deposit
def make_deposit(deposit):

	if deposit.payment_method.name.lower() == 'cash':
		if deposit.amount == None:
			return None
		else:
			deposit.save()
			acc = deposit.account
			acc.amount += deposit.amount
			acc.save()
			#make cash out
			cash_out = CashOut(desc=deposit.desc,date=deposit.date,amount=deposit.amount)
			cashflow.make_cash_out(cash_out)
			return True

	elif deposit.payment_method.name.lower() == 'check':
		if deposit.ref_num == None:
			return None
		else:
			check = None
			try:
				check = Check.objects.get(ref_num=deposit.ref_num)
			except:
				return None
			if check:
				deposit.amount = check.amount
				acc = deposit.account
				acc.amount += deposit.amount

				acc.save()
				deposit.save()
				check.delete()

				return True
			else:
				return None
	else:
		if deposit.amount == None:
			return None
		else:
			deposit.save()
			acc = deposit.account
			acc.amount += deposit.amount
			acc.save()
			return True

#make withdraw
def make_withdraw(withdraw):

	if withdraw.payment_method.name.lower() == 'cash':
		if withdraw.amount == None:
			return None
		else:
			withdraw.save()
			acc = withdraw.account
			acc.amount -= withdraw.amount
			acc.save()
			#make cash in
			cash_in = CashIn(desc=withdraw.desc,date=withdraw.date,amount=withdraw.amount)
			cashflow.make_cash_in(cash_in)
			return True
	else:
		if withdraw.amount == None:
			return None
		else:
			withdraw.save()
			acc = withdraw.account
			acc.amount -= withdraw.amount
			acc.save()
			return True


#deposit
@login_required(login_url='/login')
def deposit(request):
	user = get_user(request)
	if not user.is_staff:
		return redirect('/fobiddn/')

	if request.method == 'POST':
		form = AddDepositForm(request.POST)
		if form.is_valid():
			deposit = form.save(commit=False)
			result = make_deposit(deposit)

			if not result:
				messages.add_message(request,messages.WARNING, 'Deposit unsuccessfull!')

		return redirect('/finance-manager/bank-deposits/')

	else:
		form = AddDepositForm()
		context = {'formname':'Deposit','form':form}
		return render(request,'finance_manager/bank/form_template.html', context)

#withdraw
@login_required(login_url='/login')
def withdraw(request):
	user = get_user(request)
	if not user.is_staff:
		return redirect('/fobiddn/')

	if request.method == 'POST':
		form = AddWithdrawForm(request.POST)
		if form.is_valid():
			withdraw = form.save(commit=False)
			result = make_withdraw(withdraw)

			if not result:
				messages.add_message(request,messages.WARNING, 'Withdraw unsuccessfull!')
		return redirect('/finance-manager/bank-withdrawals/')

	else:
		form = AddWithdrawForm()
		context = {'formname':'Withdraw','form':form}
		return render(request,'finance_manager/bank/form_template.html', context)

#accounts view
@login_required(login_url='/login')
def accounts(request):
	user = get_user(request)
	if not user.is_staff:
		return redirect('/fobiddn/')

	recodes = Bank.objects.all().order_by('-id')
	context = {'recodes':recodes}
	return render(request,'finance_manager/bank/accounts.html', context)

#diposits view
@login_required(login_url='/login')
def deposits(request):
	user = get_user(request)
	if not user.is_staff:
		return redirect('/fobiddn/')

	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']

		recodes = None

		if start_date == '' or end_date == '':
			recodes = Deposit.objects.all().order_by('-id')
		else:
			recodes = Deposit.objects.filter(date__range=[start_date,end_date]).order_by('-id')

		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/bank/deposits.html', context)
	else:
		recodes = Deposit.objects.all().order_by('-id')
		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/bank/deposits.html', context)

#withdrawals view
@login_required(login_url='/login')
def withdrawals(request):
	user = get_user(request)
	if not user.is_staff:
		return redirect('/fobiddn/')

	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']

		recodes = None

		if start_date == '' or end_date == '':
			recodes = Withdraw.objects.all().order_by('-id')
		else:
			recodes = Withdraw.objects.filter(date__range=[start_date,end_date]).order_by('-id')

		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/bank/withdrawals.html', context)
	else:
		recodes = Withdraw.objects.all().order_by('-id')
		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/bank/withdrawals.html', context)

@login_required(login_url='/login')
def checks(request):
	user = get_user(request)
	if not user.is_staff:
		return redirect('/fobiddn/')
		
	recodes = Check.objects.all().order_by('-id')
	context = {'recodes':recodes}
	return render(request,'finance_manager/bank/checks.html', context)

