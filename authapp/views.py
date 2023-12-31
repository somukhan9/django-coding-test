from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm


def login(request):
    if request.user.is_authenticated:
        return redirect('tasks:home')

    context = dict()
    form = LoginForm()
    context['form'] = form

    if request.method == 'POST':
        form = LoginForm(request.POST)
        context['form'] = form

        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            user = auth.authenticate(
                request, username=username_or_email, password=password)

            if user is not None:
                auth.login(request, user)

                messages.success(request, 'Successfully Logged In!')
                return redirect('tasks:home')

            else:
                messages.error(request, 'Invalid credentials!')
                return render(request, 'authapp/login.html', context)

        else:
            messages.error(request, 'Invalid credentials!')
            return render(request, 'authapp/login.html', context)

    else:
        form = LoginForm()
        context['form'] = form

    return render(request, 'authapp/login.html', context)


def register(request):
    context = dict()
    form = RegisterForm()
    context['form'] = form

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        context['form'] = form

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)
                if user is not None:
                    form.errors['username'] = f'A user with user "{
                        username}" already exists.'
                    return render(request, 'authapp/register.html', context)
            except:
                pass

            try:
                user = User.objects.get(email=email)
                if user is not None:
                    form.errors['email'] = f'A user with email "{
                        email}" already exists.'
                    return render(request, 'authapp/register.html', context)
            except:
                pass

        else:
            messages.error(request, 'Something went wrong!')
            return render(request, 'authapp/register.html', context)

        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(request, 'User Created Successfully!')

        return redirect('authapp:login')

    else:
        form = RegisterForm()
        context['form'] = form

    return render(request, 'authapp/register.html', context)


@login_required(login_url='authapp:login')
def logout(request):
    auth.logout(request)
    return redirect('authapp:login')
