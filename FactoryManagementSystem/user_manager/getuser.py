from django.contrib.auth.models import User

def get_user(request):
	user_id = request.session.get('user_id',None)
	if user_id:
		user = User.objects.get(pk=user_id)
		return user
	else:
		return None