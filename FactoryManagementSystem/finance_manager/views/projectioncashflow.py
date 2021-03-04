from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user_manager.getuser import get_user

from finance_manager.models import ProjectionCashIn, ProjectionCashOut
from finance_manager.forms import AddProjectionCashInForm, AddProjectionCashOutForm


#SPECIAL FUNCTION
def calc_total(data):
	'''returns total of amounts'''
	total = 0
	for element in data:
		total += element.amount

	return total


@login_required(login_url='/login')
def index(request):
	return render(request,'finance_manager/projectioncashflow/projectioncashflow.html')

@login_required(login_url='/login')
def add_cash_in(request):
	if request.method == 'POST':
		form = AddProjectionCashInForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/finance-manager/projectioncashflow/cash-ins/')
	else:
		form = AddProjectionCashInForm()
		context = {'formname':'Projection Cash In', 'form':form}
		return render(request,'finance_manager/projectioncashflow/form_template.html', context)


@login_required(login_url='/login')
def add_cash_out(request):
	if request.method == 'POST':
		form = AddProjectionCashOutForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/finance-manager/projectioncashflow/cash-outs/')
	else:
		form = AddProjectionCashOutForm()
		context = {'formname':'Projection Cash Out', 'form':form}
		return render(request,'finance_manager/projectioncashflow/form_template.html', context)


@login_required(login_url='/login')
def view_cash_in(request):
	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']

		recodes = None
		if start_date == '' or end_date == '':
			recodes = ProjectionCashIn.objects.all().order_by('-id')
		else:
			recodes = ProjectionCashIn.objects.filter(date__range=[start_date,end_date])

		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/projectioncashflow/cash_in.html', context)

	else:

		recodes = ProjectionCashIn.objects.all().order_by('-id')
		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/projectioncashflow/cash_in.html', context)

@login_required(login_url='/login')
def view_cash_out(request):
	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']

		recodes = None
		if start_date == '' or end_date == '':
			recodes = ProjectionCashOut.objects.all().order_by('-id')
		else:
			recodes = ProjectionCashOut.objects.filter(date__range=[start_date,end_date])

		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/projectioncashflow/cash_out.html', context)

	else:

		recodes = ProjectionCashOut.objects.all().order_by('-id')
		total = calc_total(recodes)
		context = {'recodes':recodes, 'total':total}
		return render(request,'finance_manager/projectioncashflow/cash_out.html', context)