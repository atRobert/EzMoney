"""ezmoney URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from userbase.views import home_view, signup_view, IncomeCreateView, GoalCreateView, PayCreateView, user_logout, GoalUpdateView, IncomeUpdateView, PaymentListView
from django.contrib.auth import views as auth_views
import os

urlpatterns = [
    path(os.environ.get('admin_url'), admin.site.urls),
    path('', home_view, name="home"),
    path('signup/', signup_view, name="signup"),
    path('add_income/', IncomeCreateView.as_view(), name='add-income'),
    re_path(r'update_income/(?P<pk>\d+)', IncomeUpdateView.as_view(), name='update-income'),
    path('add_goal/', GoalCreateView.as_view(), name='add-goal'),
    re_path(r'update_goal/(?P<pk>\d+)', GoalUpdateView.as_view(), name='update-goal'),
    path('add_money/', PayCreateView.as_view(), name='add-money'),
    re_path(r'^logout/', user_logout, name='user_logout'),
    re_path(r'my_activity/', PaymentListView.as_view(), name='my-activity'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name ='login')
]
