from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from social_django.models import UserSocialAuth

from bookmarks.common.decorators import ajax_required
from .forms import LoginForm,UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile,Contact

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

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,'account/user/list.html',{'section':'people','users':users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User,username=username,is_active=True)
    c = Contact.objects.filter(user_from=user.id).count
    cc = Contact.objects.filter(user_from=request.user.id,user_to=user.id)
    s = 'follow'
    if cc:
        s = 'unfollow'
    else:
        s = 'follow'
    return render(request,'account/user/detail.html',{'section': 'people','user': user,'c':c,'s':s})

@csrf_exempt
@login_required
@ajax_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})








