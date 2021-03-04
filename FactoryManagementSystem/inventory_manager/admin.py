from django.contrib import admin
from .models import (Customer, Sell, OtherSell, SellUpdate, SellPayment, SellDispatch, Product, ProductIssue, ProductIssueNote, ProductStock,
					 Material, MaterialIssue, MaterialStock, Supplire, Buy, BuyPayment, BuyDispatch, BuyUpdate,
					 OtherIncome, Expense, Employee, Salery)
# Register your models here.

admin.site.register(Customer)
admin.site.register(Sell)
admin.site.register(OtherSell)
admin.site.register(SellUpdate)
admin.site.register(SellPayment)
admin.site.register(SellDispatch)
admin.site.register(Product)
admin.site.register(ProductStock)
admin.site.register(ProductIssue)
admin.site.register(ProductIssueNote)
admin.site.register(Employee)
admin.site.register(Salery)

admin.site.register(Material)
admin.site.register(MaterialIssue)
admin.site.register(MaterialStock)
admin.site.register(Supplire)
admin.site.register(Buy)
admin.site.register(BuyPayment)
admin.site.register(BuyDispatch)
admin.site.register(BuyUpdate)

admin.site.register(OtherIncome)
admin.site.register(Expense)

