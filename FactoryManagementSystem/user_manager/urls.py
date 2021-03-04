from django.urls import path
from .views import index,user_login, user_logout, fobiddn

urlpatterns = [
	path('',index, name='index'),
	path('login/',user_login, name='login'),
	path('logout/',user_logout, name='logout'),
	path('fobiddn/',fobiddn, name='fobiddn'),
]