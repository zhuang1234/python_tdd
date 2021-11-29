"""superlists URL Configuration

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

superlists/urls.py 的真正作用是定义整个网站使用的 URL。如果某些 URL 只在 lists 应用中使用Django 建议使用单独的文件 lists/urls.py让应用自成一体
"""
from django.contrib import admin
from django.urls import path,re_path
from lists import views

urlpatterns = [
    path('new', views.new_list),
    path('<list_id>/', views.view_list),
    path('<list_id>/add_item', views.add_item),
    #path('admin/', admin.site.urls),
]
