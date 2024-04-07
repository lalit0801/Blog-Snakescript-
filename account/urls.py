from django.urls import path, include
from . import views

urlpatterns=[
     path('register/', views.RegisterView.as_view(), name = 'register'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('mailverification/resend/otp/', views.ResendOTPForMailVerificationView.as_view(), name = 'resend-otp-for-mail-verification'),
    path('mailverification/', views.MailVerificationView.as_view(), name = 'Verify-mail'),

]