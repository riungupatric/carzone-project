from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from contacts.models import Contact


def login(request):
    # if trying to login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # the user
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # login user
            auth.login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('dashboard')
        else:
            messages.error(request, 'Wrong username or password')
            return redirect('login')
    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # passwords must match
        if password == confirm_password:
            # check if username exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists!")
                    return redirect('register')
                else:
                    # no error so far, store the data
                    user = User.objects.create_user(
                        first_name=firstname, last_name=lastname, username=username, email=email, password=password)
                    user.save()
                    # auto-login the user
                    auth.login(request, user)
                    messages.success(request, 'Logged in successfully!')
                    return redirect('dashboard')
                    # OR redirect the user to login
                    # messages.success(request, 'registered successfully!')
                    # return redirect('login')

        else:
            messages.error(request, 'passwords do not match')
            return redirect('register')

    return render(request, 'accounts/register.html')


@login_required(login_url='login')
def dashboard(request):
    # only show user-specific inquiries
    user_inquiry = Contact.objects.order_by(
        '-created_date').filter(user_id=request.user.id)
    # context
    data = {
        'user_inquiry': user_inquiry,
    }
    return render(request, 'accounts/dashboard.html', data)


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        # messages.success(request, 'Logged out successfully!')
        return redirect('home')
    return redirect('home')
