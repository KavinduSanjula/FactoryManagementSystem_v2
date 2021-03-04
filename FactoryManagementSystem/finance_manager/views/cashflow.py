from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user_manager.getuser import get_user

from finance_manager.models import Cash, CashIn, CashOut
from finance_manager.forms import AddCashInForm, AddCashOutForm

def get_cash_object():
	try:
		cash = Cash.objects.get(pk=1)
		return cash
	except:
		pass
	
	return None

#SPECIAL FUNCTION
def calc_total(data):
	'''returns total of amounts'''
	total = 0
	for element in data:
		total += element.amount

	return total

@login_required(login_url='/login')
def cashflow(request):
	cash = get_cash_object()

	if cash:
		total_cash = cash.amount
	else:
		total_cash = 0
	
	context = {'total_cash':total_cash}
	return render(request,'finance_manager/cashflow/cashflow.html', context)

def make_cash_in(cash_in):
	cash = get_cash_object()
	if cash:
		cash.amount += cash_in.amount
		cash.save()
		cash_in.save()
		return True

	return None

def make_cash_out(cash_out):
	cash = get_cash_object()
	if cash:
		cash.amount -= cash_out.amount
		cash.save()
		cash_out.save()
		return True

	return None


@login_required(login_url='/login')
def add_cash_in(request):
	if request.method == 'POST':
		form = AddCashInForm(request.POST)
		if form.is_valid():
			cash_in = form.save(commit=False)
			result = make_cash_in(cash_in)
			if not result:
				messages.add_message(request,messages.WARNING, 'Cash in unsuccessfull!')
		return redirect('/')
			
	else:
		form = AddCashInForm()
		context = {'formname':'Cash In', 'form':form}
		return render(request,'finance_manager/cashflow/form_template.html', context)

@login_required(login_url='/login')
def add_cash_out(request):
	if request.method == 'POST':
		form = AddCashOutForm(request.POST)
		if form.is_valid():
			cash_out = form.save(commit=False)
			result = make_cash_in(cash_out)
			if not result:
				messages.add_message(request,messages.WARNING, 'Cash out unsuccessfull!')
		return redirect('/')
			
	else:
		form = AddCashOutForm()
		context = {'formname':'Cash Out', 'form':form}
		return render(request,'finance_manager/cashflow/form_template.html', context)

@login_required(login_url='/login')
def view_cash_in(request):
	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']

		recodes = None

		if start_date == '' or end_date == '':
			recodes = CashIn.objects.all().order_by('-id')
		else:
			recodes = CashIn.objects.filter(date__range=[start_date,end_date]).order_by('-id')

		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/cashflow/cash_in.html', context)
	else:
		recodes = CashIn.objects.all().order_by('-id')
		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/cashflow/cash_in.html', context)

@login_required(login_url='/login')
def view_cash_out(request):
	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']

		recodes = None

		if start_date == '' or end_date == '':
			recodes = CashOut.objects.all().order_by('-id')
		else:
			recodes = CashOut.objects.filter(date__range=[start_date,end_date]).order_by('-id')

		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/cashflow/cash_out.html', context)
	else:
		recodes = CashOut.objects.all().order_by('-id')
		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/cashflow/cash_out.html', context)
