from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('portal/', views.portal , name='portal'),
    path('login/', views.user_login , name='login'),
    path('signup/', views.register , name='register'),
    path('faculty/', views.faculty , name='faculty'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify-email'),
    path('forgot-password/', views.forgot_password , name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password , name='reset-password'),
]