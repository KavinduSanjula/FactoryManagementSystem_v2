from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from inventory_manager.models import Supplire, Buy, BuyPayment, BuyUpdate, Material, MaterialIssue, MaterialStock, BuyDispatch
from inventory_manager.forms import (AddSupplireForm, AddMaterialForm, AddMaterialStockForm, AddReceiveForm,
									 AddBuyPaymentForm, AddBuyDispatchForm, AddIssueForm)

from user_manager.getuser import get_user

from finance_manager.models import Deposit, Withdraw, CashIn, CashOut
from finance_manager.views import bank, cashflow

#inventory_manager raw material section views


############## retrive data ###############

#PRODUCT VIEW
@login_required(login_url='/login')
def material_view(request):
	return render(request, 'inventory_manager/material.html')

#SUPPLIRES VIEW
@login_required(login_url='/login')
def supplire_view(request):
	supplires = Supplire.objects.all()
	context = {'supplires':supplires}
	return render(request, 'inventory_manager/material/supplire.html', context)

#special function
def get_receives(name='',start_date='',end_date=''):
	''' filter and send receives data '''
	if name != '' and start_date != '' and end_date != '':
		receives = Buy.objects.filter(supolire__name=name,date__range=[start_date,end_date])
	elif start_date != '' and end_date != '':
		receives = Buy.objects.filter(date__range=[start_date,end_date])
	elif name != '':
		receives = Buy.objects.filter(supolire__name=name)
	elif start_date != '':
		receives = Buy.objects.filter(date=start_date)
	else:
		receives = Buy.objects.all()

	return receives.order_by('-id')

#SEPCIAL FUNCTION
def calc_total(data):
	total = 0
	for element in data:
		total += element.amount

	return total

#RECEIVES VIEW
@login_required(login_url='/login')
def receives_view(request):
	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']
		supplire_name = request.POST['supplire_name']

		receives = get_receives(supplire_name,start_date,end_date)
		total = calc_total(receives)
		context = {'receives':receives, 'total':total}
		return render(request, 'inventory_manager/material/receive.html', context)
	else:
		receives = get_receives()
		total = calc_total(receives)
		context = {'receives':receives, 'total':total}
		return render(request, 'inventory_manager/material/receive.html', context)

#MATERIAL VIEW
@login_required(login_url='/login')
def materials_view(request):
	materials = None
	if request.method == 'POST':
		category = request.POST['category']
		if category == 'all':
			materials = Material.objects.all()
		else:
			materials = Material.objects.filter(category__name=category)
	else:
		materials = Material.objects.all()
	context = {'materials':materials.order_by('-id')}
	return render(request, 'inventory_manager/material/material.html', context)

#STOCK VIEW
@login_required(login_url='/login')
def stock_view(request):
	stocks = None
	if request.method == 'POST':
		category = request.POST['category']
		if category == 'all':
			stocks = MaterialStock.objects.all().order_by('-id')
		else:
			stocks = MaterialStock.objects.filter(material__category__name=category)
	else:
		stocks = MaterialStock.objects.all().order_by('-id')
	context = {'stocks':stocks}
	return render(request, 'inventory_manager/material/stock.html', context)

#PAYMENT VIEW
@login_required(login_url='/login')
def payments_view(request, id=0):
	buy = Buy.objects.get(pk=id)
	payments = BuyPayment.objects.filter(buy=buy)
	context = {'payments':payments}
	return render(request, 'inventory_manager/material/payment.html', context)

#DISPATCH NOTE VIEW
@login_required(login_url='/login')
def dispatch_note_view(request):
	if request.method == 'POST':
		dispatch_note_num = request.POST.get('dispatch_note_num')
		if dispatch_note_num:
			dispatch_note_num = int(dispatch_note_num)
			recodes = BuyDispatch.objects.filter(dispatch_note_num=dispatch_note_num)
		else:
			recodes = None

		return render(request,'inventory_manager/material/dispatch.html', {'recodes':recodes})
	else:
		return render(request,'inventory_manager/material/dispatch.html')

#RECEIVE INFO (update details)
@login_required(login_url='/login')
def receive_info(request, id=0):
	buy = Buy.objects.get(pk=id)
	dispatchs = BuyDispatch.objects.filter(dispatch_note_num=buy.dispatch_note_num)
	recodes = BuyUpdate.objects.filter(buy=buy)
	return render(request, 'inventory_manager/material/receiveinfo.html', {'recodes':recodes, 'receive':buy, 'dispatchs':dispatchs})

#SPECIAL FUNCTION
def get_issuings(material='',start_date='',end_date=''):
	issuings = None
	if material != '' and start_date != '' and end_date != '':
		issuings = MaterialIssue.objects.filter(stock__material__name=material,date__range=[start_date,end_date])
	elif start_date != '' and end_date != '':	
		issuings = MaterialIssue.objects.filter(date__range=[start_date,end_date])
	elif start_date != '':
		issuings = MaterialIssue.objects.filter(date=start_date)
	elif material != '':
		issuings = MaterialIssue.objects.filter(stock__material__name=material)
	else:
		issuings = MaterialIssue.objects.all()
	return issuings.order_by('-id')

@login_required(login_url='/login')
def issue_material_view(request):
	if request.method == 'POST':
		material = request.POST['material_name']
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']

		issuings = get_issuings(material,start_date,end_date)
		total = calc_total(issuings)
		context = {'issuings': issuings, 'total':total}
		return render(request,'inventory_manager/material/issue.html', context)
	else:
		issuings = get_issuings()
		total = calc_total(issuings)
		context = {'issuings': issuings, 'total':total}
		return render(request,'inventory_manager/material/issue.html', context)
############## retrive data ###############


############## add data ###################

#ADD SUPPLIRE
@login_required(login_url='/login')
def add_supplire(request, id=0):
	if request.method == 'POST':
		if id == 0:
			form = AddSupplireForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('/inventory-manager/supplires/')
		else:
			instance = Supplire.objects.get(pk=id)
			form = AddSupplireForm(request.POST, instance=instance)
			if form.is_valid():
				form.save()
				return redirect('/inventory-manager/supplires/')
	else:
		if id == 0:
			form = AddSupplireForm()
			
		else: 
			instance = Supplire.objects.get(pk=id)
			form = AddSupplireForm(instance=instance)

		context = {'formname':'Add Supplire', 'form':form}
		return render(request, 'inventory_manager/material/form_template.html', context)

#ADD RECEIVE
@login_required(login_url='/login')
def add_receive(request, id=0):
	if request.method == 'POST':

		currentuser = get_user(request)
		updated = False

		if id == 0:
			form = AddReceiveForm(request.POST)
		else:
			updated = True
			instance = Buy.objects.get(pk=id)
			form = AddReceiveForm(request.POST, instance=instance)

		if form.is_valid():
			
			receive = form.save(commit=False)

			total_amount = 0
			dispatch_note_num = receive.dispatch_note_num

			dispatchs = BuyDispatch.objects.filter(dispatch_note_num=dispatch_note_num) #get all dipatch notes
			
			for dispatch in dispatchs:
				total_amount += dispatch.amount
				
				stock = MaterialStock(material=dispatch.material,
									  batch_num=dispatch.batch_num,
									  unit_price=dispatch.unit_price,
									  qty=dispatch.qty)

				stock.save()
				

			if not updated:
				receive.created_user = currentuser
			else:
				update_note = BuyUpdate(buy=receive,user=currentuser)
				update_note.save()

			receive.amount = total_amount
			receive.save()
		else:
			print('form not valid')

		return redirect('/inventory-manager/receives/')

	else:
		if id == 0:
			form = AddReceiveForm()
		else:
			instance = Buy.objects.get(pk=id)
			form = AddReceiveForm(instance=instance)
		context = {'formname':'Add receive', 'form':form}
		return render(request, 'inventory_manager/material/form_template.html', context)

#ADD PAYMENT
@login_required(login_url='/login')
def add_payment(request,id=0):
	if request.method == 'POST':
		form = AddBuyPaymentForm(request.POST)

		payment_accepted = False
		payment = None

		if form.is_valid():
			payment = form.save()
			receive = payment.buy
			payments = BuyPayment.objects.filter(buy=receive)

			total_payment = 0
			last_payment = None
			
			for payment in payments:
				total_payment += payment.amount
				last_payment = payment

			if total_payment > receive.amount:
				ddt = total_payment - receive.amount
				last_payment.amount -= ddt

			payment.amount = last_payment.amount

			payment_method = payment.payment_method
			ref_num = payment.ref_num
			eff_date = payment.eff_date

			if payment_method.name.lower() == 'credit':
				payment_accepted = True
			elif payment_method.name.lower() == 'cash':
				payment_accepted = True
				#add cash out
				desc = f'Receive Payment: {payment.buy.supplire}'
				cash_out = CashOut(desc=desc,date=payment.date,amount=payment.amount)
				cashflow.make_cash_out(cash_out)
			elif payment_method.name.lower() == 'check':
				if ref_num == None or eff_date == None or payment.account == None:
					payment_accepted = False
				else:
					payment_accepted = True
					#add withdraw
					desc = f'Receive Check Payment: {payment.ref_num}'
					withdraw = Withdraw(account=payment.account, 
										desc=desc, 
										date=payment.date, 
										amount=payment.amount, 
										payment_method=payment.payment_method, 
										ref_num=payment.ref_num)
					bank.make_withdraw(withdraw)
			else:
				payment_accepted = True
				#add withdraw
				desc = f'Receive Payment: {payment.buy.supplire}'
				withdraw = Withdraw(account=payment.account, 
									desc=desc, 
									date=payment.date, 
									amount=payment.amount, 
									payment_method=payment.payment_method, 
									ref_num=payment.ref_num)
				bank.make_withdraw(withdraw)
			

			if payment_accepted:
				payment.save()
				last_payment.save()

				if total_payment >= receive.amount:
					receive.paid = True
					receive.save()
			else:
				payment.delete()
				messages.add_message(request,messages.WARNING, 'Invalid Payment Details')

			
			return redirect('/inventory-manager/receives/')
	else:
		receive = Buy.objects.get(pk=id)
		data = {'buy':receive, 'date':receive.date, 'amount':receive.amount,}
		form = AddBuyPaymentForm(data)
		context = {'formname':'Add Payment', 'form':form}
		return render(request, 'inventory_manager/material/form_template.html', context)

#DELETE PAYMENT
@login_required(login_url='/login')
def delete_payment(request,id=0):
	user = get_user(request)
	if not user.is_superuser:
		return redirect('/fobiddn/')
		
	if request.method == 'POST':
		delete_accepted = False
		payment = BuyPayment.objects.get(pk=id)
		receive = payment.buy

		
		if payment.payment_method.name.lower() == 'credit':
			delete_accepted = True
		elif payment.payment_method.name.lower() == 'cash':
			delete_accepted = True
			desc = f'Receive Payment Revert: {payment.buy.supplire}'
			cash_in = CashIn(desc=desc,date=payment.date,amount=payment.amount)
			cashflow.make_cash_in(cash_in)
		elif payment.payment_method.name.lower() == 'check':
			#add deposti
			if payment.account == None:
				delete_accepted = False
			else:
				delete_accepted = True
				desc = f'Receive Check Returnd: {payment.ref_num}'
				deposit = Deposit(account=payment.account, 
									desc=desc, 
									date=payment.date, 
									amount=payment.amount, 
									payment_method=payment.payment_method, 
									ref_num=payment.ref_num)
				bank.make_deposit(deposit)
		else:
			#add deposti
			if payment.account == None:
				delete_accepted = False
			else:
				delete_accepted = True
				desc = f'Receive Payment Revert: {payment.ref_num}'
				deposit = Deposit(account=payment.account, 
									desc=desc, 
									date=payment.date, 
									amount=payment.amount, 
									payment_method=payment.payment_method, 
									ref_num=payment.ref_num)
				bank.make_deposit(deposit)
			


		if delete_accepted:	
			receive.paid = False
			receive.save()
			payment.delete()
		else:
			messages.add_message(request,messages.WARNING, 'Somthing went wrong!')

		url = f'/inventory-manager/receives/'
		return redirect(url)



#ADD MATERIAL
@login_required(login_url='/login')
def add_material(request, id=0):
	if request.method == 'POST':
		if id == 0:
			form = AddMaterialForm(request.POST)
		else:
			instance = Material.objects.get(pk=id)
			form = AddMaterialForm(request.POST, instance=instance)

		if form.is_valid():
			form.save()
			return redirect('/inventory-manager/materials/')

	else:
		if id == 0:
			form = AddMaterialForm()
		else:
			instance = Material.objects.get(pk=id)
			form = AddMaterialForm(instance=instance)

		context = {'formname':'Add Material', 'form':form}
		return render(request, 'inventory_manager/material/form_template.html', context)

#ADD_STOCK
@login_required(login_url='/login')
def add_stock(request, id=0):
	if request.method == 'POST':
		if id == 0:
			form =AddMaterialStockForm(request.POST)
		else:
			instance = MaterialStock.objects.get(pk=id)
			form = AddMaterialStockForm(request.POST, instance=instance)

		if form.is_valid():
			form.save()
			return redirect('/inventory-manager/material-stock')

	else:
		if id == 0:
			form = AddMaterialStockForm()
		else:
			instance = MaterialStock.objects.get(pk=id)
			form = AddMaterialStockForm(instance=instance)

		context = {'formname':'Add Stock', 'form':form}
		return render(request, 'inventory_manager/material/form_template.html', context)



#ADD BUYDISPATCH
@login_required(login_url='/login')
def add_buy_dispatch(request):
	if request.method == 'POST':
		form = AddBuyDispatchForm(request.POST)

		if form.is_valid():
			print('form is valid')
			dispatch_note_num = form.cleaned_data['dispatch_note_num']
			unit_price = form.cleaned_data['unit_price']
			qty = form.cleaned_data['qty']
			amount = unit_price * qty

			dispatch = form.save(commit=False)
			dispatch.amount = amount
			dispatch.save()

			recodes = BuyDispatch.objects.filter(dispatch_note_num=dispatch_note_num)
			form = AddBuyDispatchForm({'dispatch_note_num':dispatch_note_num})

			context = {'form':form, 'recodes':recodes ,'dispatch_note_num':dispatch_note_num}
			return render(request, 'inventory_manager/material/add_dispatch_note.html', context)

	else:
		form = AddBuyDispatchForm()
		context = {'form':form}
		return render(request, 'inventory_manager/material/add_dispatch_note.html', context)


#DELETE BUYDISPATCH
@login_required(login_url='/login')
def delete_buy_dispatch(request, id=0):
	dispatch = BuyDispatch.objects.get(pk=id)
	dispatch_note_num = dispatch.dispatch_note_num

	dispatch.delete()

	recodes = BuyDispatch.objects.filter(dispatch_note_num=dispatch_note_num)
	form = AddBuyDispatchForm({'dispatch_note_num':dispatch_note_num})

	context = {'form':form, 'recodes':recodes, 'dispatch_note_num':dispatch_note_num}
	return render(request, 'inventory_manager/material/add_dispatch_note.html', context)

@login_required(login_url='/login')
def issue_material(request):
	if request.method == 'POST':
		form = AddIssueForm(request.POST)
		if form.is_valid():
			issue = form.save(commit=False)
			stock = issue.stock 
			amount = issue.stock.unit_price * issue.qty
			stock.qty -= issue.qty
			issue.amount = amount
			issue.save()
			stock.save()
			return redirect('/inventory-manager/material-issuings/')
		else:
			pass
	else:
		form = AddIssueForm()
		context = {'form':form}
		return render(request, 'inventory_manager/material/form_template.html', context)
