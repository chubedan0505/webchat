from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.template.loader import render_to_string

from django.contrib.auth import authenticate,login,logout

def homechat (request):
    context={}
    return render(request,'app/homechat.html',context)
def register(request):
       # form = CreateUserForm()
  #  if request.method == "POST":
   #     form = CreateUserForm(request.POST)
    #    if form.is_valid():
    #        form.save()   
     #       return redirect('login')
   # context ={'form':form}
   # return render(request,'app/register.html',context)
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Đánh dấu tài khoản chưa được kích hoạt
            user.save()
            send_confirmation_email(request, user)  # Gửi email xác nhận
            return render(request, 'app/login.html')
    else:
        form = CreateUserForm()
    return render(request, 'app/register.html', {'form': form})
    
def loginPage(request):
    if request.user.is_authenticated:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username =username,password =password)
        if user is not None: 
            login(request,user)
            return redirect('homechat')
        else: messages.info(request,'user or password not correct!')
    context ={}
    return render(request,'app/login.html',context)
def send_confirmation_email(request, user):
    subject = 'Xác nhận tài khoản của bạn'
    message = render_to_string('Email.html', {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'confirm_url': request.build_absolute_uri(reverse('confirm_email', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })),
    })
    send_mail(subject, message, 'chaugiathinh2020gmail.com', [user.email])
def confirm_email(request, uidb64, token):
    # Xử lý xác nhận email ở đây
    return render(request, 'Email.html')