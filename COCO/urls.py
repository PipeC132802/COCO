"""COCO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from Apps.ManageUsers import urls as user_urls
from Apps.ManageBarters import urls as barter_urls
from Apps.ManageSearches import urls as search_urls
from Apps.ManageNotifications import urls as notify_urls


coco_api_base = 'coco/api/v1.0/'

urlpatterns = [
    path('admin/', admin.site.urls),

    # User app apis
    path(coco_api_base, include(user_urls)),

    # Barter app apis
    path(coco_api_base, include(barter_urls)),

    # Search app apis
    path(coco_api_base, include(search_urls)),

    # Notifications app apis
    path(coco_api_base, include(notify_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
