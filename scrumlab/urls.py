"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from jedzonko.views import add_recipe, recipe_list, recipe_details, delete_recipe, edit_recipe, plan_details_views
from jedzonko.views import loading_page, contact_view, about_view
from jedzonko.views import plan_add_view, plan_add_details, plan_list_page1, plan_list, plan_id


urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipe/add/', add_recipe),
    path('recipe/list/', recipe_list),
    path('recipe/<r_id>/', recipe_details),
    path('recipe/delete/<r_id>/', delete_recipe),
    path('recipe/modify/<r_id>/', edit_recipe),
    path('', loading_page),
    path('contact/', contact_view),
    path('about/', about_view),
    path('plan/', plan_details_views),
    path('plan/add/', plan_add_view),
    path('plan/add/details/', plan_add_details),
    path('plan/list/', plan_list_page1),
    re_path('list/(?P<page_number>(\d){1,4})$', plan_list),
    re_path('plan/(?P<plan_number>(\d){1,4})$', plan_id)
]
