from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
        #path('login',views.login,name = 'login'),
        path('login',auth_views.login,name = 'login'),
        path('logout',auth_views.logout,{'template_name':'registration/logout.html'},name = 'logout'),
        path('logout-then-login',auth_views.logout_then_login,name = 'logout-then-login'),
        path('',views.dash_board,name='dashboard'),

        #change password
        path('password-change',auth_views.password_change,name = 'password_change'),
        path('password-change-done',auth_views.password_change_done,name = 'password_change_done'),

        #reset password
        path('password-reset',auth_views.password_reset,name='password_reset'),
        path('password-reset/done',auth_views.password_reset_done,name='password_reset_done'),
        path('password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',auth_views.password_reset_confirm,name='password_reset_confirm'),
        path('password-reset/complete',auth_views.password_reset_complete,name='password_reset_complete'),

        #register

        path('register',views.register,name='register'),

        #edit
        path('edit',views.edit,name = 'edit'),
]