from django.urls import path
from . import views

urlpatterns = [
    path('validate_phone/', views.verify_phone_send_otp, name='validate-otp'),
    path('validate_otp/', views.verify_otp, name='validate-otp'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('admin/login/', views.login_admin, name='login-admin'),
    path('logout/', views.logout, name='logout'),
    path('my_profile/', views.get_profile, name='profile'),
    path('my_profile/update/', views.update_profile, name='update-profile'),
    path('my_profile/image/upload/', views.upload_profile_image, name='upload-profile-image'),
]