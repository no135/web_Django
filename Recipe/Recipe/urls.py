"""
URL configuration for Recipe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Recipie_app.views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_settings, name='profile'),

    path('', home, name='home'),
    path('recipe/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('search/', search_recipes, name='search_recipes'),
    path('category/<int:cat_id>/', category_recipes, name='category_recipes'),

    path('recipe/submit/', submit_recipe, name='submit_recipe'),
    path('my-recipes/', my_recipes, name='my_recipes'),
    path('recipe/edit/<int:recipe_id>/', edit_recipe, name='edit_recipe'),
    path('recipe/delete/<int:recipe_id>/', delete_recipe, name='delete_recipe'),

    path('recipe/<int:recipe_id>/favorite/', add_to_favorites, name='add_to_favorites'),
    path('recipe/<int:recipe_id>/rate/', rate_recipe, name='rate_recipe'),

    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('approve/<int:recipe_id>/', approve_recipe, name='approve_recipe'),
    path('reject/<int:recipe_id>/', reject_recipe, name='reject_recipe'),
    path('users/', manage_users, name='manage_users'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('logs/', admin_logs, name='admin_logs'),

    path('dashboard/categories/', manage_categories, name='manage_categories'),
    path('category/add/', add_category, name='add_category'),
    path('category/delete/<int:cat_id>/', delete_category, name='delete_category'),
    path('roles/', role, name='manage_roles'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)