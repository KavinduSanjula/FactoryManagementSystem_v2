from django.db import models
 

class Profit(models.Model):
	date = models.DateField(auto_now_add=True)
	desc = models.CharField(max_length=500)
	start_date = models.DateField()
	end_date = models.DateField()
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	remarks = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return f'Profit - {self.amount} | {self.date}'

		
#payment method
class PaymentMethod(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

#Petty Cash
class PettyCashIssue(models.Model):
	ref_num = models.IntegerField(null=True)
	date = models.DateField()
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	start_date = models.DateField()
	end_date = models.DateField()
	remarks = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return f'PettyCashIssue-{self.date}'

class PettyCashExpense(models.Model):
	ref_num = models.IntegerField(null=True)
	desc = models.CharField(max_length=200)
	date = models.DateField()
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	remarks = models.CharField(max_length=500, null=True, blank=True)

class PettyCash(models.Model):
	amount = models.DecimalField(max_digits=15, decimal_places=2)

	def __str__(self):
		return f'PettyCash Rs.{self.amount}'


#Cash Flow
class Cash(models.Model):
	amount = models.DecimalField(max_digits=15, decimal_places=2)

	def __str__(self):
		return f'Cash - Rs.{self.amount}'

class CashIn(models.Model):
	desc = models.CharField(max_length=200)
	date = models.DateField()
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	remarks = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return f'CashIn- Rs.{self.amount} | {self.date}'

class CashOut(models.Model):
	desc = models.CharField(max_length=200)
	date = models.DateField()
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	remarks = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return f'CashOut- Rs.{self.amount} | {self.date}'

class ProjectionCashIn(models.Model):
	desc = models.CharField(max_length=200)
	date = models.DateField()
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	remarks = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return f'ProjectionCashIn- Rs.{self.amount} | {self.date}'

class ProjectionCashOut(models.Model):
	desc = models.CharField(max_length=200)
	date = models.DateField()
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	remarks = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return f'ProjectionCashOut- Rs.{self.amount} | {self.date}'


#Bank
class Bank(models.Model):
	acc_num = models.IntegerField(unique=True)
	acc_name = models.CharField(max_length=100)
	desc = models.CharField(max_length=200, null=True, blank=True)
	amount = models.DecimalField(max_digits=15, decimal_places=2)

	def __str__(self):
		return f'Account-{self.acc_num} | {self.acc_name}'

class Check(models.Model):
	date = models.DateField()
	ref_num = models.IntegerField(unique=True)
	eff_date = models.DateField()
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	
	def __str__(self):
		return f'Check - {self.ref_num}'


class Deposit(models.Model):
	account = models.ForeignKey(Bank, null=True, on_delete=models.SET_NULL)
	desc = models.CharField(max_length=200, null=True, blank=True)
	date = models.DateField()
	amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True)
	payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL)
	ref_num = models.IntegerField(null=True, blank=True)
	remarks = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return f'Deposit- Rs.{self.amount} | {self.date}'

class Withdraw(models.Model):
	account = models.ForeignKey(Bank, null=True, on_delete=models.SET_NULL)
	desc = models.CharField(max_length=200, null=True, blank=True)
	date = models.DateField()
	amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True)
	payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL)
	ref_num = models.IntegerField(null=True, blank=True)
	remarks = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return f'Withdraw- Rs.{self.amount} | {self.date}'


