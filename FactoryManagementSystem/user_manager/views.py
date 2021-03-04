from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .getuser import get_user

#user_manager views

@login_required(login_url='/login')
def index(request):
	user = get_user(request)
	username = ''
	if user:
		username = user.username

	return render(request,'user_manager/index.html', {'username':username})

def fobiddn(request):
	return render(request,'user_manager/fobiddn.html')

def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request,user)
				request.session['user_id'] = user.id
				return redirect('/')

			else:
				return HttpResponse('User is not active.')

		else:
			return HttpResponse('Invalid login details.')

		return render(request,'user_manager/login.html')
	else:
		return render(request,'user_manager/login.html')

@login_required
def user_logout(request):
	#request.session.pop('user_id')
	logout(request)
	return redirect('/')
