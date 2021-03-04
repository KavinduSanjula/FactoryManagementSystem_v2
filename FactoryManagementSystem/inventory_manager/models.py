from django.db import models
from django.contrib.auth.models import User
from finance_manager.models import Bank, PaymentMethod

# Inventory Manager Models  

class Employee(models.Model):
	code = models.IntegerField(unique=True)
	name = models.CharField(max_length=100)
	addr = models.CharField(max_length=250, null=True, blank=True)
	phone = models.CharField(max_length=15, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	is_permenet = models.BooleanField()
	basic_salery = models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)

	def __str__(self):
		return f'{self.code} | {self.name} | { "Permenet" if self.is_permenet else "Temporary"}'

class Salery(models.Model):
	date = models.DateField()
	employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
	account = models.ForeignKey(Bank, null=True, on_delete=models.SET_NULL, blank=True)
	worked_days = models.IntegerField(null=True, blank=True)
	rate = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
	other_payments = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
	leave_ddt = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
	other_ddt = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL)
	ref_num = models.IntegerField(null=True, blank=True)
	eff_date = models.DateField(null=True, blank=True)
	remarks = models.CharField(max_length=500, null=True, blank=True)
	paid = models.BooleanField()

	def __str__(self):
		return f'{self.employee}'


class OtherIncome(models.Model):
	account = models.ForeignKey(Bank , null=True, on_delete=models.SET_NULL, blank=True)
	name = models.CharField(max_length=50)
	date = models.DateField()
	payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL)
	ref_num = models.IntegerField(null=True, blank=True)
	eff_date = models.DateField(null=True, blank=True)
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	paid = models.BooleanField(default=False, null=True, blank=True)
	remarks = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return self.name

class Expense(models.Model):
	account = models.ForeignKey(Bank , null=True, on_delete=models.SET_NULL, blank=True)
	name = models.CharField(max_length=50)
	date = models.DateField()
	payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL)
	ref_num = models.IntegerField(null=True, blank=True)
	eff_date = models.DateField(null=True, blank=True)
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	paid = models.BooleanField(default=True,blank=True)
	remarks = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return self.name


#product section models
class Product(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class ProductStock(models.Model):
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	batch_num = models.IntegerField()
	qty = models.IntegerField()

	def __str__(self):
		return f'{self.product.name} | {self.batch_num} | {self.qty}'


class Customer(models.Model):
	name = models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	email = models.EmailField(null=True, blank=True)
	addr = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Sell(models.Model):
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	date = models.DateField()
	dispatch_note_num = models.IntegerField()
	created_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	paid = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.customer} | {self.date} | {self.amount}'

class OtherSell(models.Model):
	account = models.ForeignKey(Bank , null=True, on_delete=models.SET_NULL, blank=True)
	customer = models.CharField(max_length=20)
	date = models.DateField()
	dispatch_note_num = models.IntegerField()
	payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL)
	ref_num = models.IntegerField(null=True, blank=True)
	eff_date = models.DateField(null=True, blank=True)
	created_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	paid = models.BooleanField(default=False)
	amount = models.DecimalField(max_digits=15, decimal_places=2)

	def __str__(self):
		return f'{self.customer} | {self.date} | {self.amount}'


class SellPayment(models.Model):
	account = models.ForeignKey(Bank, null=True, on_delete=models.SET_NULL, blank=True)
	sale = models.ForeignKey(Sell, null=True, on_delete=models.SET_NULL )
	date = models.DateField()
	ref_num = models.IntegerField(null=True, blank=True)
	eff_date = models.DateField(null=True, blank=True)
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	remarks = models.CharField(max_length=500, null=True, blank=True)
	payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL)
	ref_num = models.IntegerField(null=True, blank=True)

	def __str__(self):
			return f'{self.id} | {self.date} | {self.amount}'


class SellUpdate(models.Model):
	sale = models.ForeignKey(Sell, null=True, on_delete=models.SET_NULL)
	user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.user.username


class SellDispatch(models.Model):
	stock = models.ForeignKey(ProductStock, null=True, on_delete=models.SET_NULL)
	unit_price = models.DecimalField(max_digits=15, decimal_places=2)
	qty = models.IntegerField()
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	dispatch_note_num = models.IntegerField()

	def __str__(self):
		return f'SellDispatch - {self.stock}'

class ProductIssueNote(models.Model):
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	issue_note_num = models.IntegerField()
	batch_num = models.IntegerField()
	qty = models.IntegerField()

	def __str__(self):
		return f'ProductIssue - {self.product} | {self.batch_num}'

class ProductIssue(models.Model):
	issue_note_num = models.IntegerField()
	date = models.DateField()
	remarks = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return f'Issue | {self.issue_note_num}'


#material section models

class Material(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class MaterialStock(models.Model):
	material = models.ForeignKey(Material, null=True, on_delete=models.SET_NULL)
	batch_num = models.IntegerField()
	unit_price = models.DecimalField(max_digits=15, decimal_places=2)
	qty = models.IntegerField()

	def __str__(self):
		return f'{self.material.name} | {self.batch_num} | {self.unit_price}'

class MaterialIssue(models.Model):
	stock = models.ForeignKey(MaterialStock, null=True, on_delete=models.SET_NULL)
	production_batch_number = models.IntegerField()
	qty = models.IntegerField()
	amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
	date = models.DateField()
	remarks = models.CharField(max_length=500,null=True,blank=True)

	def __str__(self):
		return f'{self.stock.material.name} | {self.production_batch_number} | {self.qty}'

class Supplire(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	addr = models.CharField(max_length=200)
	phone = models.CharField(max_length=15)

	def __str__(self):
		return self.name

class Buy(models.Model):
	supplire = models.ForeignKey(Supplire, null=True, on_delete=models.SET_NULL)
	date = models.DateField()
	dispatch_note_num = models.IntegerField()
	amount = models.DecimalField(max_digits=15,decimal_places=2)
	created_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	grn = models.CharField(max_length=10, null=True, blank=True)
	invoice = models.CharField(max_length=10, null=True, blank=True)
	payment_voucher = models.CharField(max_length=10, null=True, blank=True)
	paid = models.BooleanField(default=False, null=True, blank=True)

	def __str__(self):
		return f'{self.supplire} | {self.date} | {self.amount}'

class BuyPayment(models.Model):
	account = models.ForeignKey(Bank, null=True, on_delete=models.SET_NULL, blank=True)
	buy = models.ForeignKey(Buy, null=True, on_delete=models.SET_NULL)
	date = models.DateField()
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL)
	ref_num = models.CharField(max_length=20,null=True, blank=True)
	eff_date = models.DateField(null=True, blank=True)
	remarks = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return f'{self.id} | {self.date} | {self.amount}'

class BuyUpdate(models.Model):
	buy = models.ForeignKey(Buy, null=True, on_delete=models.SET_NULL)
	user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.user.username

class BuyDispatch(models.Model):
	material = models.ForeignKey(Material, null=True, on_delete=models.SET_NULL)
	dispatch_note_num = models.IntegerField()
	batch_num = models.IntegerField()
	unit_price = models.DecimalField(max_digits=15,decimal_places=2)
	qty = models.IntegerField()
	amount = models.DecimalField(max_digits=15,decimal_places=2)

	def __str__(self):
		return f'BuyDispatch - {self.material}'
