import json

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger

from bookmarks.common.decorators import ajax_required
from .models import Post
from .forms import  PostCreateForm

# Create your views here.
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST,request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request,"Post added successfully")

            return redirect("dashboard")
    else:
        form = PostCreateForm(data = request.GET)
    return render(request,'post/create.html',{'section': 'images','form': form})

def post_detail(request,id):
    post = get_object_or_404(Post,id=id)
    return render(request,'post/detail.html',{'section':'images','post':post})

@require_POST
@ajax_required
@csrf_exempt
@login_required
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status':'ok'})

@login_required
def post_list(request):
    post_list = Post.objects.all()
    panigator = Paginator(post_list,10)

    page = request.GET.get('page',1)
    try:
        posts = panigator.page(page)
    except PageNotAnInteger:
        posts = panigator.page(1)
    except EmptyPage:
        posts = panigator.page(panigator.num_pages)
    return render(request,'post/list.html',{'posts':posts})



