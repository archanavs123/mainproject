from django.urls import path
from . import views

urlpatterns = [
    path('',views.base,name='home'),
    path('loginn/',views.user_login,name='loginn'),
    path('signUp/',views.user_signup,name='signUp'),
    path('logout/',views.user_logout,name='logout1'),
    path('issue/',views.issue,name='issue'),
    path('return/',views.return_item,name='return'),

]
