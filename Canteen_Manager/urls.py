"""
URL configuration for Canteen_Manager project.

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
# canteen_manager/urls.py

from django.contrib import admin
from django.urls import path, include  # <-- 'include' को इंपोर्ट करें

urlpatterns = [
    path('admin/', admin.site.urls),
    path('management/', include('management.urls')),  # <-- यह लाइन जोड़ें
    # हम http://127.0.0.1:8000/management/ पर ऐप को देखेंगे
]