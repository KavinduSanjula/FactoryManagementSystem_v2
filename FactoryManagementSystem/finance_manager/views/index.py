from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user_manager.getuser import get_user

@login_required(login_url='/login')
def index(request):
	return render(request,'finance_manager/finance.html')

