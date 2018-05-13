from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from social_django.models import UserSocialAuth

from .forms import LoginForm,UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

# Create your views here.
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user =  authenticate(username = cd["username"],password = cd["password"])

            if user is not None:
                if user.is_activate:
                    login(request,user)
                    return HttpResponse("Xac thuc thanh cong")
                else:
                    return HttpResponse("Tai khoan bi khoa")
            else:
                return HttpResponse("Tai khoan khong ton tai")
    else:
        form = LoginForm()
    return render(request,'account/login.html',{'form':form})

@login_required
def dash_board(request):
    return render(request,'account/index.html',{'section':'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                    user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()

            profile = Profile.objects.create(user=new_user)
            return render(request,
                    'account/register_done.html',
                    {'new_user': new_user})
        else:
            return render(request, 'register/register.html', {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance= request.user.profile,data=request.POST,files = request.FILES)
        #profile_form = ProfileEditForm(instance=request.user.pro)

        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.add_message(request, messages.INFO, 'Hello world.')
        else:
            messages.error(request,"Fail")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile, files = request.FILES)
    return render(request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form})

@login_required
def settings(request):
    user = request.user
    try:
        github_login = user.social_auth.get(provider = 'github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
    return render(request,'account/settings.html',{'github_login':github_login})

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'account/password.html', {'form': form})








