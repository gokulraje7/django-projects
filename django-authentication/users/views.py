from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    return render(request,'users/index.html')
def home(request):
    if request.user.is_authenticated:
        return render(request,'users/home.html')
    return redirect('login')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect(reverse('home'))
        else:
            messages.error(request,'Invalid credentials')
            return redirect('login')
    return render(request,'users/login_view.html')
def logout_view(request):
    logout(request)
    messages.success(request,' ✔ you are logged out successfully')
    return redirect('login')
def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        

        if User.objects.filter(email=email):
            messages.error(request,' ❌ email already registered')
            return redirect(reverse('signup'))
        else:
            if pass1.isalnum() and pass1 == pass2:
                user = User.objects.create_user(username = email,password = pass1,email = email,first_name = firstname,last_name = lastname)
                user.save()
                messages.success(request,'✔ user account created succesfully')
                return redirect(reverse('login'))
            elif not pass1.isalnum():
                messages.error(request,' ❌ password must only alphanumeric ')
                return redirect(reverse('signup'))
            elif not pass1 == pass2 :
                messages.error(request,'❌ password and confirm password should match')
                return redirect(reverse('signup'))

    return render(request,'users/signup.html')
   