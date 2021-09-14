from django import forms
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404, Http404, HttpResponseRedirect
from .models import Account
from django.contrib.auth.models import User
from .forms import AddAccountForm, CreateUserForm, ModifyAccountForm, RegisterForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages


User = get_user_model()


@login_required(login_url='login_page')
def accounts_list(request):
    accounts = Account.get_user_accounts(request.user)
    context = {
        'accounts': accounts
    }
    return render(request, 'accounts_list.html', context)


@login_required(login_url='login_page')
def add_account(request):
    if request.method == 'POST':
        form = AddAccountForm(request.POST)
        if form.is_valid:
            account = form.save(commit=False)
            account.belongs_to_id = request.user.id
            account.platform_slug = account.platform.replace(' ', '-')
            account.save()
            messages.success(request, 'Account & Password added successfully!!')
            return redirect('accounts_list')
        else:   # invalid form
            messages.warning(request, 'Please Provide proper information')
            return render(request, 'AddAccountForm.html', {'form': form})
    else:  # GET method
        form = AddAccountForm()
        return render(request, 'AddAccountForm.html', {'form': form})


def login_page(request):
    if request.user.is_authenticated:
        messages.info(request, f'Welcome! {request.user.username.capitalize()}')
        return redirect('accounts_list')

    else:  # If no User Logged In
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username.lower(), password=password)
            # print(f"=================ok  \nName: {username}\nPass: {password}\nUser: {user} ==============")
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome! {request.user.username.capitalize()}')
                return redirect('accounts_list')
            else:  # Wrong Password or Username
                messages.warning(request, 'Invalid Username or Password')
                return render(request, 'login_page.html')

        else:  # GET Method
            return render(request, 'login_page.html')


def logout_page(request):
    user = request.user.username
    logout(request)
    messages.success(request, f'Thank You {user.title()}! for being with us.')
    return redirect('login_page')


@login_required(login_url='login_page')
def modify_account(request, id):
    account = get_object_or_404(Account, id=id)
    if account.belongs_to != request.user:
        raise Http404
    if request.method == "POST":
        form = ModifyAccountForm(request.POST or None, instance=account)
        if form.is_valid():
            data = form.save(commit=False)
            data.platform_slug = data.platform.replace(' ', '-')
            data.save()
            messages.success(request, f"{data.platform} data updated")
            return redirect('accounts_list')
        else:   # invalid form
            messages.error(request, f"Failed to Update")
    else:   # GET Method
        form = ModifyAccountForm(instance=account)
        context = {
            'account': account,
            'form': form
        }
        return render(request, 'modify_account_page.html', context)


def delete_account(request, id):
    account = get_object_or_404(Account, id=id)
    account.delete()
    messages.warning(request, f"{account.platform} data deleted")
    return redirect('accounts_list')


def tryy(request):
    return render(request, 'tryy.html')


def Xsignup_page(request):
    empty_form = CreateUserForm()
    if request.user.is_authenticated:
        return redirect('accounts_list')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                messages.success(request, f"Thank You {user.username.title()} for joining us")
                return redirect('accounts_list')
            else:
                messages.error(request, f"Please provide proper information")
                return render(request, 'CreateUserForm.html', {'form': empty_form})
        else:
            return render(request, 'CreateUserForm.html', {'form': empty_form})


def Xregister_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid:
        username = form.cleaned_data["username"]
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1") 
        password2 = form.cleaned_data.get("password2")
        user = User.objects.create(username, email, password)
        try:
            #user = User.objects.create(username, email, password)
            pass
        except:
            user = None
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome! {request.user.username.capitalize()}')
            return redirect('accounts_list')
        else:  # Wrong Password or Username
            messages.warning(request, 'Invalid Username or Password')
            return render(request, 'login_page.html')


def signup_page(request):
    empty_form = CreateUserForm()
    if request.user.is_authenticated:
        return redirect('accounts_list')
    else:
        if request.method == 'POST':
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            username = request.POST.get("username")
            password = request.POST.get("password1")
            password2 = request.POST.get("password2")
            email = request.POST.get("email")
            qs = User.objects.filter(username__iexact = username)
            if qs.exists():
                messages.warning(request, f"Username Already Exist")
                return render(request, 'CreateUserForm.html', {'form': empty_form})
            else:
                xuser = User.objects.create_user(username.lower(), email, password)
                messages.success(request, f"Thank You {xuser.username.title()} for joining us")
                return redirect('accounts_list')


            # if form.is_valid():
            #     user = form.save(commit=False)
            #     user.username = user.username.lower()
            #     user.save()
            #     messages.success(request, f"Thank You {user.username.title()} for joining us")
            #     return redirect('accounts_list')
            # else:
            #     messages.error(request, f"Please provide proper information")
            #     return render(request, 'CreateUserForm.html', {'form': empty_form})
        else:
            return render(request, 'CreateUserForm.html', {'form': empty_form})
