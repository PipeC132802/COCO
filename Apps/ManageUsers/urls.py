# User/urls.py
from django.urls import path, include
from .views import *

urlpatterns = [
    path('user-auth/', include('dj_rest_auth.urls')),
    path('create-user/', CreateUserApi.as_view(), name='create_user'),
    path('user-status/', UserStatus.as_view(), name='user_status'),
    path('confirm-user/', UserVerificationApi.as_view(), name='confirm_user'),
    path('contact-user/', UserContactApi.as_view(), name='contact_user'),
    path('about-user/', UserAboutAndAreasApi.as_view(), name='about_user'),
    path('profile-picture-user/', ProfilePictureApi.as_view(), name='profile_picture'),
    path('area-list/', AreaListApi.as_view(), name='areas'),
    path('account/', UserAccountInfoApi.as_view(), name='account_info')
]
