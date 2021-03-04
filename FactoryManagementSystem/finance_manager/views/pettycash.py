from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user_manager.getuser import get_user

from finance_manager.models import PettyCash, PettyCashExpense, PettyCashIssue, CashOut
from finance_manager.forms import PettyCashIssueForm, AddPettyCashExpenseForm
from finance_manager.views.cashflow import make_cash_out

def get_pettycash_object():
	try:
		cash = PettyCash.objects.get(pk=1)
		return cash
	except:
		return None

#SPECIAL FUNCTION
def calc_total(data):
	'''returns total of amounts'''
	total = 0
	for element in data:
		total += element.amount

	return total

@login_required(login_url='/login')
def pettycash(request):
	cash = get_pettycash_object()
	if cash:
		total_cash = cash.amount
	else:
		total_cash = 0
	context = {'total_cash':total_cash}
	return render(request,'finance_manager/pettycash/pettycash.html', context)

@login_required(login_url='/login')
def issue_pettycash(request):
	if request.method == 'POST':
		form = PettyCashIssueForm(request.POST)
		if form.is_valid():
			issue = form.save()
			cash = get_pettycash_object()
			if cash:
				cash.amount += issue.amount
				cash_out = CashOut(desc='Petty Cash Issue',date=issue.date,amount=issue.amount)
				make_cash_out(cash_out)
			else:
				cash = PettyCash(id=1,amount=issue.amount)
			cash.save()
			return redirect('/finance-manager/pettycash-issuings/')
	else:
		form = PettyCashIssueForm()
		context = {'formname':'Issue Petty Cash', 'form':form}
		return render(request,'finance_manager/pettycash/form_template.html', context)

@login_required(login_url='/login')
def add_expense(request):
	if request.method == 'POST':
		form = AddPettyCashExpenseForm(request.POST)
		if form.is_valid():
			expense = form.save()
			cash = get_pettycash_object()
			if cash:
				cash.amount -= expense.amount
				cash.save()
			else:
				expense.delete()
			return redirect('/finance-manager/pettycash-expenses/')
	else:
		form = AddPettyCashExpenseForm()
		context = {'formname':'Add Expense','form':form}
		return render(request,'finance_manager/pettycash/form_template.html', context)

@login_required(login_url='/login')
def issuings(request):
	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']

		recodes = None

		if start_date == '' or end_date == '':
			recodes = PettyCashIssue.objects.all().order_by('-id')
		else:
			recodes = PettyCashIssue.objects.filter(date__range=[start_date,end_date]).order_by('-id')

		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/pettycash/issuing.html', context)
	else:
		recodes = PettyCashIssue.objects.all().order_by('-id')
		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/pettycash/issuing.html', context)

@login_required(login_url='/login')
def expeses(request):
	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']

		recodes = None

		if start_date == '' or end_date == '':
			recodes = PettyCashExpense.objects.all().order_by('-id')
		else:
			recodes = PettyCashExpense.objects.filter(date__range=[start_date,end_date]).order_by('-id')

		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/pettycash/expense.html', context)
	else:
		recodes = PettyCashExpense.objects.all().order_by('-id')
		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/pettycash/expense.html', context)