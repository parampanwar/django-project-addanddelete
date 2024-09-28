"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from new import views 
from new.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', views.new, name='new'),
    
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('export_to_excel/' ,export_to_excel,name='export_to_excel'),
    path('upload-xlsx/', views.upload_xlsx, name='upload_xlsx'),
    path('venue_pdf/', views.venue_pdf, name='venue_pdf'),
    path('search', views.search_view, name="search_view"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
