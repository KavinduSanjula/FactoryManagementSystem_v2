from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user_manager.getuser import get_user

from finance_manager.forms import CalcProfitForm

from inventory_manager.models import Sell, OtherSell, OtherIncome, Expense, MaterialIssue, Salery
from finance_manager.models import Profit, PettyCashExpense


@login_required(login_url='/login')
def profit(request):
	user = get_user(request)
	if not user.is_superuser:
		return redirect('/fobiddn/')

	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']
		recodes = None
		if start_date == '' or end_date == '':
			recodes = Profit.objects.all().order_by('-id')
		else:
			recodes = Profit.objects.filter(date__range=[start_date,end_date]).order_by('-id')
			
		return render(request,'finance_manager/profit/profit.html', {'recodes':recodes})
	else:
		recodes = Profit.objects.all().order_by('-id')
		return render(request,'finance_manager/profit/profit.html', {'recodes':recodes})

def calculate_profit(start_date,end_date,startup_unfinished,last_unfinished,startup_finished,last_finished,desc,remarks):
#calculate cost of sales
	#issued material cost
	issued_materials = MaterialIssue.objects.filter(date__range=[start_date,end_date])
	issued_material_cost = 0
	for issue in issued_materials:
		issued_material_cost += issue.amount
	print('Issued material cost:\t',issued_material_cost)

	#startup_unfinished - (param)
	#last_unfinished - (param)
	#startup_finished - (param)
	#last_finished - (param)
	
	cost_of_sales = issued_material_cost + startup_unfinished + startup_finished - (last_unfinished + last_finished)
	print('Cost of sales:\t',cost_of_sales)
#calculate gross profit
	#cost of sales - (calculated)
	#sales amount
	sales = Sell.objects.filter(date__range=[start_date,end_date])
	sales_amount = 0
	for sale in sales:
		sales_amount += sale.amount
	print('Sales:"\t',sales_amount)

	#other sales amount
	other_sales = OtherSell.objects.filter(date__range=[start_date,end_date])
	other_sales_amount = 0
	for other_sale in other_sales:
		other_sales_amount += other_sale.amount
	print('Other Sales:\t',other_sales_amount)

#calculate profit
	#gross profit
	gross_profit = (sales_amount + other_sales_amount) - cost_of_sales
	print('Gross Profit:\t',gross_profit)

	#other income
	other_incomes = OtherIncome.objects.filter(date__range=[start_date,end_date])
	other_incomes_amount = 0
	for other_income in other_incomes:
		other_incomes_amount += other_income.amount
	print('Other Income:\t',other_incomes_amount)

	#expenses
	expenses = Expense.objects.filter(date__range=[start_date,end_date])
	expenses_amount = 0
	for expense in expenses:
		expenses_amount += expense.amount
	print('Expenses:\t',expenses_amount)

	salery_expenses = Salery.objects.filter(date__range=[start_date,end_date])
	salery_expenses_amount = 0
	for salery in salery_expenses:
		salery_expenses_amount += salery.amount
	print('Salery Expenses:\t',salery_expenses_amount)

	#pettycash expenses
	pettycash_expenses = PettyCashExpense.objects.filter(date__range=[start_date,end_date])
	pettycash_expenses_amount = 0
	for pettycash_expense in pettycash_expenses:
		pettycash_expenses_amount += pettycash_expense.amount
	print('PettyCash Expenses:\t',pettycash_expenses_amount)

	#calculating profit
	profit = gross_profit + other_incomes_amount - (expenses_amount + pettycash_expenses_amount + salery_expenses_amount)
	print('Profit:\t',profit)

	profit_object = Profit(desc=desc, amount=profit,start_date=start_date,end_date=end_date,remarks=remarks)
	profit_object.save()
	

@login_required(login_url='/login')
def calc_profit(request):
	user = get_user(request)
	if not user.is_superuser:
		return redirect('/fobiddn/')
		
	if request.method == 'POST':
		form = CalcProfitForm(request.POST)
		if form.is_valid():
			start_date = form.cleaned_data.get('start_date')
			end_date = form.cleaned_data.get('end_date')
			startup_unfinished = form.cleaned_data.get('startup_unfinished')
			last_unfinished = form.cleaned_data.get('last_unfinished')
			startup_finished = form.cleaned_data.get('startup_finished')
			last_finished = form.cleaned_data.get('last_finished')
			desc = form.cleaned_data.get('desc')
			remarks = form.cleaned_data.get('remarks')

			calculate_profit(start_date,end_date,startup_unfinished,last_unfinished,startup_finished,last_finished,desc,remarks)
		return redirect('/finance-manager/profit/')
	else:
		form = CalcProfitForm()
		context = {'formname':'Calculate Profit','form':form}
		return render(request,'finance_manager/profit/form_template.html', context)
