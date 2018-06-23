
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse


from user.models import UserModel, UserTicketModel

from utils.functions import get_ticket


def register(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html', )
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        icon = request.FILES.get('icon')

        if not all([username, email, password, icon]):
            msg = '请填写数据'
            return render(request, 'user/user_register.html', {'msg':msg})
        password = make_password(password)
        UserModel.objects.create(username=username,
                                 password=password,
                                 email=email,
                                 icon=icon
                                 )
        return HttpResponseRedirect(reverse('user:login'))


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = UserModel.objects.filter(username=username).first()
        if user:
            if check_password(password, user.password):
                ticket = get_ticket()
                response = HttpResponseRedirect(reverse('axf:mine'))
                out_time = datetime.now() + timedelta(days=1)
                response.set_cookie('ticket', ticket, expires=out_time)
                UserTicketModel.objects.create(user=user,
                                               out_time=out_time,
                                               ticket=ticket)
                return response
            else:
                msg = '密码错误'
                return render(request, 'user/user_login.html', {'msg': msg})
        else:
            msg = '用户不存在'
            return render(request, 'user/user_login.html', {'msg': msg})

def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect(reverse('user:login'))
        response.delete_cookie('ticket')
        return response
