from django.urls import path
from . import views

urlpatterns = [
    path('create',views.post_create,name='create'),
    path('detail/<int:id>/',views.post_detail,name='detail'),
    path('like',views.post_like,name='like'),
    path('posts',views.post_list,name='posts'),
    path('ranking',views.post_ranking,name='ranking')
]