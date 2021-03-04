import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from inventory_manager.models import Customer, Sell, OtherSell, SellPayment, SellUpdate, Product, ProductIssue, ProductIssueNote, ProductStock, SellDispatch

from inventory_manager.forms import (AddCustomerForm, AddSaleForm, AddPaymentForm,
									 AddProductForm, AddSellDispatchForm,
									 AddStockForm, AddOtherSaleForm, AddIssueNoteForm)

from user_manager.getuser import get_user

from finance_manager.models import Deposit, Withdraw, CashIn, CashOut, Check
from finance_manager.views import bank, cashflow

#inventory_manager final product section seviews


############## retrive data ###############

#PRODUCT VIEW
@login_required(login_url='/login')
def product_view(request):
	return render(request, 'inventory_manager/product.html')

#CUSTOMER VIEW
@login_required(login_url='/login')
def customer_view(request):
	customers = Customer.objects.all()
	context = {'customers':customers}
	return render(request, 'inventory_manager/product/customer.html', context)

#SPECIAL FUNCTION
def get_sales(table=Sell,name='',start_date='',end_date=''):
	'''returns filterd data of sales'''
	
	if name != '' and start_date != '' and end_date != '':
		sales = Sell.objects.filter(customer__name=name,date__range=[start_date,end_date])
	elif start_date != '' and end_date != '':
		sales = table.objects.filter(date__range=[start_date,end_date])
	elif name != '':
		sales = Sell.objects.filter(customer__name=name)
	elif start_date != '':
		sales = table.objects.filter(date=start_date)
	else:
		sales = table.objects.all()

	return sales.order_by('-id')

#SPECIAL FUNCTION
def calc_total(data):
	'''returns total of amounts'''
	total = 0
	for element in data:
		total += element.amount

	return total

#SALES VIEW
@login_required(login_url='/login')
def sales_view(request):
	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']
		cust_name = request.POST['cust_name']

		sales = get_sales(Sell,cust_name,start_date,end_date)
		total = calc_total(sales)
		context = {'sales':sales, 'total':total}
		return render(request, 'inventory_manager/product/sale.html', context)
	else:
		sales = get_sales()
		total = calc_total(sales)
		context = {'sales':sales, 'total':total}
		return render(request, 'inventory_manager/product/sale.html', context)

#OTHER SALES VIEW
@login_required(login_url='/login')
def other_sales_view(request):
	if request.method == 'POST':
		start_date = request.POST['start_date']
		end_date = request.POST['end_date']

		sales = get_sales(OtherSell,'',start_date,end_date)
		total = calc_total(sales)
		context = {'sales':sales, 'total':total}
		return render(request, 'inventory_manager/product/other_sale.html', context)
	else:
		sales = get_sales(OtherSell)
		total = calc_total(sales)
		context = {'sales':sales, 'total':total}
		return render(request, 'inventory_manager/product/other_sale.html', context)

class ProductQty:
	def __init__(self,product,qty):
		self.product = product
		self.qty = qty

#PRODUCT VIEW
@login_required(login_url='/login')
def products_view(request):
	products = Product.objects.all()
	product_list = []
	
	for product in products:
		stock = ProductStock.objects.filter(product=product)
		qty = 0

		for item in stock:
			qty += item.qty

		product_list.append(ProductQty(product,qty))

	context = {'products':product_list}
	return render(request, 'inventory_manager/product/product.html', context)

#STOCK VIEW
@login_required(login_url='/login')
def stock_view(request):
	stocks = ProductStock.objects.all()
	context = {'stocks':stocks}
	return render(request, 'inventory_manager/product/stock.html', context)

#PAYMENT VIEW
@login_required(login_url='/login')
def payments_view(request, id=0):
	sale = Sell.objects.get(pk=id)
	payments = SellPayment.objects.filter(sale=sale)
	context = {'payments':payments}
	return render(request, 'inventory_manager/product/payment.html', context)

#DISPATCH NOTE VIEW
@login_required(login_url='/login')
def dispatch_note_view(request):
	if request.method == 'POST':
		dispatch_note_num = request.POST.get('dispatch_note_num')
		if dispatch_note_num:
			dispatch_note_num = int(dispatch_note_num)
			recodes = SellDispatch.objects.filter(dispatch_note_num=dispatch_note_num)
		else:
			recodes = None

		return render(request,'inventory_manager/product/dispatch.html', {'recodes':recodes})
	else:
		return render(request,'inventory_manager/product/dispatch.html')

#SALE INFO (update details)
@login_required(login_url='/login')
def sale_info(request, id=0):
	sale = Sell.objects.get(pk=id)
	dispatchs = SellDispatch.objects.filter(dispatch_note_num=sale.dispatch_note_num)
	recodes = SellUpdate.objects.filter(sale=sale)
	context = {'recodes':recodes, 'sale':sale, 'dispatchs':dispatchs}
	return render(request, 'inventory_manager/product/saleinfo.html', context)

@login_required(login_url='/login')
def issuing(request):
	recodes = ProductIssue.objects.all()
	context = {'recodes':recodes}
	return render(request,'inventory_manager/product/issuing.html', context)

@login_required(login_url='/login')
def view_issue_note(request, id=0):
	recodes = ProductIssueNote.objects.filter(issue_note_num=id)
	context = {'recodes':recodes}
	return render(request,'inventory_manager/product/issue_note.html', context)

############## retrive data ###############


############## add data ###################

#ADD CUSTOMER
@login_required(login_url='/login')
def add_customer(request, id=0):
	if request.method == 'POST':
		if id == 0:
			form = AddCustomerForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('/inventory-manager/customers/')
		else:
			instance = Customer.objects.get(pk=id)
			form = AddCustomerForm(request.POST, instance=instance)
			if form.is_valid():
				form.save()
				return redirect('/inventory-manager/customers/')
	else:
		if id == 0:
			form = AddCustomerForm()
			
		else: 
			instance = Customer.objects.get(pk=id)
			form = AddCustomerForm(instance=instance)

		context = {'formname':'Add Customer', 'form':form}
		return render(request, 'inventory_manager/product/form_template.html', context)

#ADD SALE
@login_required(login_url='/login')
def add_sale(request, id=0):
	if request.method == 'POST':

		currentuser = get_user(request)
		updated = False

		if id == 0:
			form = AddSaleForm(request.POST)
		else:
			updated = True
			instance = Sell.objects.get(pk=id)
			form = AddSaleForm(request.POST, instance=instance)

		if form.is_valid():
			
			sale = form.save(commit=False)

			total_amount = 0
			dispatch_note_num = sale.dispatch_note_num

			dispatchs = SellDispatch.objects.filter(dispatch_note_num=dispatch_note_num) #get all dipatch notes
			
			for dispatch in dispatchs:
				total_amount += dispatch.amount
				stock = dispatch.stock
				stock.qty -= dispatch.qty
				stock.save()

			if not updated:
				sale.created_user = currentuser
			else:
				update_note = SellUpdate(sale=sale,user=currentuser)
				update_note.save()

			sale.amount = total_amount
			sale.save()
		else:
			messages.add_message(request,messages.WARNING, 'Somthing Went Wrong')

		return redirect('/inventory-manager/sales/')

	else:
		if id == 0:
			form = AddSaleForm()
		else:
			instance = Sell.objects.get(pk=id)
			form = AddSaleForm(instance=instance)
		context = {'formname':'Add Sale', 'form':form}
		return render(request, 'inventory_manager/product/form_template.html', context)

#ADD OTHER SALE
@login_required(login_url='/login')
def add_other_sale(request, id=0):
	if request.method == 'POST':

		currentuser = get_user(request)
		payment_accepted = False

		if id == 0:
			form = AddOtherSaleForm(request.POST)
		else:
			instance = OtherSell.objects.get(pk=id)
			form = AddOtherSaleForm(request.POST, instance=instance)

		other_sale = None

		if form.is_valid():
			other_sale = form.save(commit=False)

			total_amount = 0
			dispatch_note_num = other_sale.dispatch_note_num

			dispatchs = SellDispatch.objects.filter(dispatch_note_num=dispatch_note_num) #get all dipatch notes
			
			for dispatch in dispatchs:
				total_amount += dispatch.amount
			
			other_sale.created_user = currentuser
			other_sale.amount = total_amount

			payment_method = other_sale.payment_method
			ref_num = other_sale.ref_num
			eff_date = other_sale.eff_date

			if payment_method.name.lower() == 'credit':
				payment_accepted = True
				other_sale.paid = False
			elif payment_method.name.lower() == 'cash':
				payment_accepted = True
				#add cash in
				desc = f'Other Sale Payment: {other_sale.customer}'
				cash_in = CashIn(desc=desc,date=other_sale.date,amount=other_sale.amount)
				cashflow.make_cash_in(cash_in)
				other_sale.paid = True

			elif payment_method.name.lower() == 'check':
				if ref_num == None or eff_date == None:
					payment_accepted = False
				else:
					payment_accepted = True
					#add check to check table
					check = Check(date=other_sale.date,ref_num=ref_num,eff_date=eff_date,amount=other_sale.amount)
					check.save()
					other_sale.paid = True
			else:
				payment_accepted = True
				#add deposit
				desc = f'Other Sale Payment: {other_sale.customer}'
				deposit = Deposit(account=other_sale.account, desc=desc, date=other_sale.date, amount=other_sale.amount, payment_method=other_sale.payment_method)
				bank.make_deposit(deposit)
				other_sale.paid = True


			if payment_accepted:

				for dispatch in dispatchs:
					stock = dispatch.stock
					stock.qty -= dispatch.qty
					stock.save()

				other_sale.save()
				
			else:
				messages.add_message(request,messages.WARNING, 'Invalid Payment Details')
		else:
			messages.add_message(request,messages.WARNING, 'Form is Invalid')

		return redirect('/inventory-manager/other-sales/')

	else:
		if id == 0:
			form = AddOtherSaleForm()
		else:
			instance = OtherSell.objects.get(pk=id)
			form = AddOtherSaleForm(instance=instance)
		context = {'formname':'Add Other Sale', 'form':form}
		return render(request, 'inventory_manager/product/form_template.html', context)

@login_required(login_url='/login')
def delete_other_sale(request, id=0):
	user = get_user(request)
	if not user.is_superuser:
		return redirect('/fobiddn/')

	if request.method == 'POST':
		other_sale = OtherSell.objects.get(pk=id)
		delete_accepted = False

		if other_sale.payment_method.name.lower() == 'credit':
			delete_accepted = True
		elif other_sale.payment_method.name.lower() == 'cash':
			delete_accepted = True
			# add cash out
			desc = f'Other Sale Revert: {other_sale.customer}'
			cash_out = CashOut(desc=desc,date=other_sale.date,amount=other_sale.amount)
			cashflow.make_cash_out(cash_out)
		elif other_sale.payment_method.name.lower() == 'check':
			if other_sale.account == None:
				delete_accepted = False
			else:
				delete_accepted = True
				# add withdraw
				desc = f'Returned Check: {other_sale.ref_num}'
				withdraw = Withdraw(account=other_sale.account, 
									desc=desc, 
									date=other_sale.date, 
									amount=other_sale.amount, 
									payment_method=other_sale.payment_method, 
									ref_num=other_sale.ref_num)
				bank.make_withdraw(withdraw)
		else:
			if other_sale.account == None:
				delete_accepted = False
			else:
				delete_accepted = True
				# add withdraw
				desc = f'Other Sale Revert: {other_sale.ref_num}'
				withdraw = Withdraw(account=other_sale.account, 
									desc=desc, 
									date=other_sale.date, 
									amount=other_sale.amount, 
									payment_method=other_sale.payment_method, 
									ref_num=other_sale.ref_num)
				bank.make_withdraw(withdraw)

		if delete_accepted:
			other_sale.delete()
		else:
			messages.add_message(request,messages.WARNING, 'Somthing went wrong!')
		return redirect('/inventory-manager/other-sales/')

#ADD PAYMENT
@login_required(login_url='/login')
def add_payment(request,id=0):
	if request.method == 'POST':
		
		form = AddPaymentForm(request.POST)

		payment_accepted = False
		payment = None
		
		if form.is_valid():
			payment = form.save()
			sale = payment.sale
			payments = SellPayment.objects.filter(sale=sale)

			total_payment = 0
			last_payment = None
			
			for payment in payments:
				total_payment += payment.amount
				last_payment = payment

			if total_payment > sale.amount:
				ddt = total_payment - sale.amount
				last_payment.amount -= ddt

			payment.amount = last_payment.amount

			payment_method = payment.payment_method
			ref_num = payment.ref_num
			eff_date = payment.eff_date

			if payment_method.name.lower() == 'credit':
				payment_accepted = True
			elif payment_method.name.lower() == 'cash':
				payment_accepted = True
				#add cash in
				desc = f'Sale Payment: "{payment.sale.customer}"'
				cash_in = CashIn(desc=desc,date=payment.sale.date,amount=payment.amount)
				cashflow.make_cash_in(cash_in)

			elif payment_method.name.lower() == 'check':
				if ref_num == None or eff_date == None:
					payment_accepted = False
				else:
					payment_accepted = True
					#add check to check table
					check = Check(date=payment.date,ref_num=ref_num,eff_date=eff_date,amount=payment.amount)
					check.save()
			else:
				payment_accepted = True
				#add deposit
				desc = f'Sale Payment: "{payment.sale.customer}"'
				deposit = Deposit(account=payment.account, desc=desc, date=payment.date, amount=payment.amount, payment_method=payment.payment_method)
				bank.make_deposit(deposit)
		

		if payment_accepted:
			payment.save()
			last_payment.save()

			if total_payment >= sale.amount:
				sale.paid = True
				sale.save()
		else:
			payment.delete()
			messages.add_message(request,messages.WARNING, 'Invalid Payment Details')

		return redirect('/inventory-manager/sales/')
	else:
		sale = Sell.objects.get(pk=id)
		data = {'sale':sale, 'amount':sale.amount,}
		form = AddPaymentForm(data)
		context = {'formname':'Add Payment', 'form':form}
		return render(request, 'inventory_manager/product/form_template.html', context)

#DELETE PAYMENT
@login_required(login_url='/login')
def delete_payment(request,id=0):
	user = get_user(request)
	if not user.is_superuser:
		return redirect('/fobiddn/')
		
	if request.method == 'POST':
		delete_accepted = False
		payment = SellPayment.objects.get(pk=id)
		sale = payment.sale
		
		if payment.payment_method.name.lower() == 'credit':
			delete_accepted = True
		elif payment.payment_method.name.lower() == 'cash':
			delete_accepted = True
			#add cash out
			desc = f'Sale Payment Revert: {payment.sale.customer}'
			cash_out = CashOut(desc=desc,date=payment.date,amount=payment.amount)
			cashflow.make_cash_out(cash_out)
		elif payment.payment_method.name.lower() == 'check':
			if payment.account == None:
				delete_accepted = False
			else:
				delete_accepted = True
				#add withdraw
				desc = f'Sale Check Returnd: {payment.ref_num}'
				withdraw = Withdraw(account=payment.account, 
									desc=desc, 
									date=payment.date, 
									amount=payment.amount, 
									payment_method=payment.payment_method, 
									ref_num=payment.ref_num)
				bank.make_withdraw(withdraw)

		else:
			#add withdraw
			if payment.account == None:
				delete_accepted = False
			else:
				delete_accepted = True
				desc = f'Sale Payment Revert: {payment.sale.customer}'
				withdraw = Withdraw(account=payment.account, 
									desc=desc, 
									date=payment.date, 
									amount=payment.amount, 
									payment_method=payment.payment_method, 
									ref_num=payment.ref_num)
				bank.make_withdraw(withdraw)

		if delete_accepted:
			sale.paid = False
			sale.save()
			payment.delete()
		else:
			messages.add_message(request,messages.WARNING, 'Somthing went wrong!')
		url = f'/inventory-manager/sales/'
		return redirect(url)



#ADD PRODUCT
@login_required(login_url='/login')
def add_product(request, id=0):
	if request.method == 'POST':
		if id == 0:
			form = AddProductForm(request.POST)
		else:
			instance = Product.objects.get(pk=id)
			form = AddProductForm(request.POST, instance=instance)

		if form.is_valid():
			form.save()
			return redirect('/inventory-manager/products/')

	else:
		if id == 0:
			form = AddProductForm()
		else:
			instance = Product.objects.get(pk=id)
			form = AddProductForm(instance=instance)

		context = {'formname':'Add Product', 'form':form}
		return render(request, 'inventory_manager/product/form_template.html', context)

#ADD_STOCK
@login_required(login_url='/login')
def add_stock(request, id=0):
	if request.method == 'POST':
		if id == 0:
			form =AddStockForm(request.POST)
		else:
			instance = ProductIssue.objects.get(pk=id)
			form = AddStockForm(request.POST, instance=instance)

		if form.is_valid():
			issue = form.save()
			issuing_notes = ProductIssueNote.objects.filter(issue_note_num=issue.issue_note_num)

			for issuing_note in issuing_notes:
				stock = None
				try:
					stock = ProductStock.objects.get(product=issuing_note.product,batch_num=issuing_note.batch_num)
				except:
					pass

				if stock:
					stock.qty += issuing_note.qty
				else:
					stock = ProductStock(product=issuing_note.product,
										 batch_num=issuing_note.batch_num,
										 qty=issuing_note.qty)
				stock.save()
			return redirect('/inventory-manager/product-issuings')

	else:
		if id == 0:
			form = AddStockForm()
		else:
			instance = ProductIssue.objects.get(pk=id)
			form = AddStockForm(instance=instance)

		context = {'formname':'Add Stock', 'form':form}
		return render(request, 'inventory_manager/product/form_template.html', context)



#ADD SELLDISPATCH
@login_required(login_url='/login')
def add_sell_dispatch(request):
	if request.method == 'POST':
		form = AddSellDispatchForm(request.POST)

		if form.is_valid():
			print('form is valid')
			stock = form.cleaned_data['stock']
			dispatch_note_num = form.cleaned_data['dispatch_note_num']
			unit_price = form.cleaned_data['unit_price']
			qty = form.cleaned_data['qty']

			if stock.qty >= qty:
				amount = unit_price * qty

				dispatch = form.save(commit=False)
				dispatch.amount = amount
				dispatch.save()
			else:
				messages.add_message(request,messages.WARNING, 'Stock Error!')

			recodes = SellDispatch.objects.filter(dispatch_note_num=dispatch_note_num)
			form = AddSellDispatchForm()

			context = {'form':form, 'recodes':recodes ,'dispatch_note_num':dispatch_note_num}
			return render(request, 'inventory_manager/product/add_dispatch_note.html', context)

	else:
		form = AddSellDispatchForm()
		context = {'form':form}
		return render(request, 'inventory_manager/product/add_dispatch_note.html', context)

#DELETE SELLDISPATCH
@login_required(login_url='/login')
def delete_sell_dispatch(request, id=0):
	dispatch = SellDispatch.objects.get(pk=id)
	dispatch_note_num = dispatch.dispatch_note_num

	dispatch.delete()

	recodes = SellDispatch.objects.filter(dispatch_note_num=dispatch_note_num)
	form = AddSellDispatchForm()

	context = {'form':form, 'recodes':recodes, 'dispatch_note_num':dispatch_note_num}
	return render(request, 'inventory_manager/product/add_dispatch_note.html', context)


#ADD PRODUCT ISSUE
@login_required(login_url='/login')
def add_issue_note(request):
	if request.method == 'POST':
		form = AddIssueNoteForm(request.POST)

		if form.is_valid():
			print('valid')
			issue_note = form.save()

			recodes = ProductIssueNote.objects.filter(issue_note_num=issue_note.issue_note_num)
			form = AddIssueNoteForm()

			context = {'form':form, 'recodes':recodes ,'issue_note_num':issue_note.issue_note_num}
			return render(request, 'inventory_manager/product/add_product_issue_note.html', context)

		else:
			return HttpResponse('form is invalid')
	else:
		form = AddIssueNoteForm()
		context = {'form':form}
		return render(request, 'inventory_manager/product/add_product_issue_note.html', context)


#DELETE PRODUCT ISSUE
@login_required(login_url='/login')
def delete_issue_note(request, id=0):
	issue = ProductIssueNote.objects.get(pk=id)
	issue_note_num = issue.issue_note_num

	issue.delete()

	recodes = ProductIssueNote.objects.filter(issue_note_num=issue_note_num)
	form = AddIssueNoteForm()

	context = {'form':form, 'recodes':recodes ,'issue_note_num':issue_note_num}
	return render(request, 'inventory_manager/product/add_product_issue_note.html', context)
