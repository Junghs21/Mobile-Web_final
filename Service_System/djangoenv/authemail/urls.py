from django.urls import path, include
from .views import SendEmailVerification, VerifyEmail, EmailVerificationViewSet, AdminSendEmail, email_dashboard
from rest_framework.routers import DefaultRouter
from .views import UpdateHelmetStatus

router = DefaultRouter()
router.register(r'email', EmailVerificationViewSet, basename='email-verification')

urlpatterns = [
    path('email/send/', AdminSendEmail.as_view(), name='admin_send_email'),  # 이메일 전송
    path('email/dashboard/', email_dashboard, name='email_dashboard'),      # 이메일 대시보드
    path('send/', SendEmailVerification.as_view(), name='send_verification'),
    path('verify/', VerifyEmail.as_view(), name='verify_email'),
    path('update_helmet/', UpdateHelmetStatus.as_view(), name='update_helmet_status'),
    path('', include(router.urls)),  # Router에 등록된 URL 포함
]
