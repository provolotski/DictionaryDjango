from django.shortcuts import render, redirect
from .auth_backends import ActiveDirectorySessionBackend
from .models import BelstatUser
import logging

# logger = logging.getLogger(__name__)
logger = logging.getLogger('special.view')
def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        auth = ActiveDirectorySessionBackend()
        user = BelstatUser(auth.authenticate(request, username, password))

        if user:
            logger.info('походу совсем законнектились')
            return redirect('home')
        else:
            logger.error('вылетели в ошибку')
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('login')