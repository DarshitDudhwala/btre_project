from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from contacts.models import Contacts

def login(request):
    # Store Request Data
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invaild Credetials')
            return redirect('login')
    else:    
        return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        # Store Request Data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords matches
        if password == password2:
            # Check if User Exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username Already Exists')
                return redirect('register')
            else:
                # Check Email Exists
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email Already Used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

                    # Redirect to Home Page After Registration
                    # auth.login(request, user)
                    # messages.success(request, "You're Now Logged In")
                    # return redirect('index')

                    # Redirect to Login Page After Registration
                    user.save()
                    messages.success(request, "You're Now Registered and Now Log in")
                    return redirect('login')
        else:
            messages.error(request, 'Password does not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')
        return redirect('register')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "You are successfully Logged Out")
        return redirect('index')

def dashboard(request):
    user_contacts = Contacts.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }

    return render(request, 'accounts/dashboard.html', context)
