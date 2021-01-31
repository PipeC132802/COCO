# User/urls.py
from django.urls import path, include
from .views import *

urlpatterns = [
    path('user-auth/', include('dj_rest_auth.urls')),
    path('user-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('user-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('user-auth/twitter/', TwitterLogin.as_view(), name='twitter_login'),
    path('create-user/', CreateUserApi.as_view(), name='create_user'),
    path('user-status/', UserStatus.as_view(), name='user_status'),
    path('confirm-user/', UserVerificationApi.as_view(), name='confirm_user'),
    path('contact-user/', UserContactApi.as_view(), name='contact_user'),
    path('about-user/', UserAboutAndAreasApi.as_view(), name='about_user'),
    path('profile-picture-user/', ProfilePictureApi.as_view(), name='profile_picture'),
    path('cover-photo-user/', CoverPhotoApi.as_view(), name='cover_photo'),
    path('area-list/', AreaListApi.as_view(), name='areas'),
    path('account/', UserAccountInfoApi.as_view(), name='account_info'),
    path('user-about/', UserAboutApi.as_view(), name='user_about'),
    path('user-contact/', UserContactAndAreasApi.as_view(), name='user_contact'),
    path('follow-user/', FollowUserApi.as_view(), name='follow_user'),
    path('suggest-users/', SuggestUserApi.as_view(), name='suggest_users'),
    path('follow-list/', FollowApi.as_view(), name='follow_list'),
    path('user-info-update/', UpdateUserAccountInfoApi.as_view(), name='update_info'),
    path('user-account-deactivated/', DeactivateAccountApi.as_view(), name='deactivate_account'),
]
