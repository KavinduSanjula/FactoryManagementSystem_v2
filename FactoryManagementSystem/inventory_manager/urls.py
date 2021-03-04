from django.urls import path
from .views import product,material,other

urlpatterns = [
	#product section

	path('product/',product.product_view, name='product'),
	path('customers/',product.customer_view, name='customers-view'),
	path('sales/',product.sales_view, name='sales-view'),
	path('other-sales/',product.other_sales_view, name='other-sales-view'),
	path('products/',product.products_view, name='products-view'),
	path('product-stock/',product.stock_view, name='product-stock-view'),

	path('payments/<int:id>',product.payments_view, name='payments'),
	path('sale-info/<int:id>',product.sale_info, name='sale-info'),

	path('add-customer/', product.add_customer, name='add-customer'),
	path('update-customer/<int:id>', product.add_customer, name='update-customer'),

	path('add-stock/', product.add_stock, name='add-stock'),
	path('update-stock/<int:id>', product.add_stock, name='update-stock'),

	path('add-sale/', product.add_sale, name='add-sale'),
	path('update-sale/<int:id>', product.add_sale, name='update-sale'),

	path('add-other-sale/', product.add_other_sale, name='add-other-sale'),
	path('update-other-sale/<int:id>', product.add_other_sale, name='update-other-sale'),
	path('delete-other-sale/<int:id>', product.delete_other_sale, name='delete-other-sale'),

	path('add-payment/<int:id>', product.add_payment, name='add-payment'),
	path('delete-sell-payment/<int:id>', product.delete_payment, name='delete-sell-payment'),

	path('add-product/', product.add_product, name='add-product'),
	path('update-product/<int:id>', product.add_product, name='update-product'),

	path('add-selldispatch/', product.add_sell_dispatch, name='add-selldispatch'),
	path('delete-selldispatch/<int:id>', product.delete_sell_dispatch, name='delete-selldispatch'),

	path('add-issue-note/', product.add_issue_note, name='add-issue-note'),
	path('view-issue-note/<int:id>', product.view_issue_note, name='view-issue-note'),
	path('delete-issue-note/<int:id>', product.delete_issue_note, name='delete-issue-note'),

	path('product-issuings/', product.issuing, name='issue-product-view'),

	path('selldispatchnote/', product.dispatch_note_view, name='selldispatch'),

	#material section
	path('material/',material.material_view, name='material'),
	path('supplires/',material.supplire_view, name='supplires-view'),
	path('receives/',material.receives_view, name='receives-view'),
	path('materials/',material.materials_view, name='materials-view'),
	path('material-stock/',material.stock_view, name='material-stock-view'),

	path('buy-payments/<int:id>',material.payments_view, name='buy-payments'),
	path('receive-info/<int:id>',material.receive_info, name='receive-info'),

	path('add-supplire/', material.add_supplire, name='add-supplire'),
	path('update-supplire/<int:id>', material.add_supplire, name='update-supplire'),

	path('add-material-stock/', material.add_stock, name='add-material-stock'),
	path('update-material-stock/<int:id>', material.add_stock, name='update-material-stock'),

	path('add-receive/', material.add_receive, name='add-receive'),
	path('update-receive/<int:id>', material.add_receive, name='update-receive'),

	path('add-buy-payment/<int:id>', material.add_payment, name='add-buy-payment'),
	path('delete-buy-payment/<int:id>', material.delete_payment, name='delete-buy-payment'),

	path('add-material/', material.add_material, name='add-material'),
	path('update-material/<int:id>', material.add_material, name='update-material'),

	path('add-buydispatch/', material.add_buy_dispatch, name='add-buydispatch'),
	path('delete-buydispatch/<int:id>', material.delete_buy_dispatch, name='delete-buydispatch'),

	path('buydispatchnote/', material.dispatch_note_view, name='buydispatch'),

	path('material-issuings/', material.issue_material_view, name='issue-material-view'),
	path('issue-material/', material.issue_material, name='issue-material'),

	path('other/', other.index, name='other'),

	path('other-incomes/', other.view_otherincomes, name='view-otherincome'),
	path('expenses/', other.view_expenses, name='view-expense'),

	path('employes/', other.view_employes, name='view-employes'),
	path('add-employee/', other.add_employee, name='add-employee'),
	path('update-employee/<int:id>', other.add_employee, name='update-employee'),

	path('salery/', other.view_salery, name='view-salery'),
	path('add-salery/', other.add_salery, name='add-salery'),
	path('update-salery/<int:id>', other.add_salery, name='update-salery'),
	path('delete-salery/<int:id>', other.delete_salery, name='delete-salery'),

	path('add-other-income/', other.add_otherincome, name='add-otherincome'),
	path('update-other-income/<int:id>', other.add_otherincome, name='update-otherincome'),
	path('delete-other-income/<int:id>', other.delete_otherincome, name='delete-otherincome'),

	path('add-expense/', other.add_expense, name='add-expense'),
	path('update-expense/<int:id>', other.add_expense, name='update-expense'),
	path('delete-expense/<int:id>', other.delete_expense, name='delete-expense'),
]

