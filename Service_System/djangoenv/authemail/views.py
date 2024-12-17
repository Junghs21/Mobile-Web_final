from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import viewsets
from rest_framework import status
from .models import EmailVerification
from .serializers import EmailVerificationSerializer


# 인증 코드 발송 (기존)
class SendEmailVerification(APIView):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        verification_code = get_random_string(6)  # 6자리 랜덤 코드 생성

        # 기존 데이터 삭제 후 새로 생성
        EmailVerification.objects.filter(email=email).delete()
        EmailVerification.objects.create(name=name, email=email, verification_code=verification_code)

        # 이메일 전송
        send_mail(
            'Your Verification Code',
            f'Your verification code is: {verification_code}',
            'noreply@example.com',
            [email]
        )
        return Response({"message": "Verification code sent to email."})


# 인증 코드 확인 (기존)
class VerifyEmail(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        try:
            verification = EmailVerification.objects.get(email=email, verification_code=code)
            verification.helmet = False  # 기본값 False 설정
            verification.save()
            return Response({"message": "Email verified and data saved successfully."})
        except EmailVerification.DoesNotExist:
            return Response({"error": "Invalid code or email."}, status=400)


# 운영자: 이메일 전송 기능
# 운영자: 이메일 전송 기능
class AdminSendEmail(APIView):
    def post(self, request):
        message = request.POST.get("message", "")
        filter_helmet = request.POST.get("filter_helmet", None)  # 필터 값 가져오기

        # 헬멧 필터링 적용
        if filter_helmet == "true":
            recipients = EmailVerification.objects.filter(helmet=True).values_list('email', flat=True)
        elif filter_helmet == "false":
            recipients = EmailVerification.objects.filter(helmet=False).values_list('email', flat=True)
        else:
            recipients = EmailVerification.objects.all().values_list('email', flat=True)  # 모든 사용자

        if not recipients:
            return Response({"error": "No recipients found."}, status=400)

        sent_recipients = []  # 보낸 유저 목록 저장

        try:
            for email in recipients:
                send_mail(
                    "Admin Message",
                    message,
                    "noreply@example.com",
                    [email],
                    fail_silently=False,
                )
                sent_recipients.append(email)  # 보낸 이메일 추가

            return Response({
                "message": "Emails sent successfully.",
                "send_user": sent_recipients  # 보낸 유저 목록 반환
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# 운영자 대시보드 HTML 렌더링
def email_dashboard(request):
    return render(request, 'email_admin_dashboard.html')


# 이메일 인증 관련 API ViewSet (기존)
class EmailVerificationViewSet(viewsets.ModelViewSet):
    queryset = EmailVerification.objects.all()
    serializer_class = EmailVerificationSerializer


class UpdateHelmetStatus(APIView):
    def post(self, request):
        email = request.data.get("email")  # 이메일 가져오기
        helmet_status = request.data.get("helmet")  # 헬멧 상태 가져오기 (true/false)

        if not email or helmet_status is None:
            return Response({"error": "Invalid input data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 이메일을 소문자로 변환하여 비교
            user = EmailVerification.objects.get(email__iexact=email.strip())  # 대소문자 구분 없이 비교
            user.helmet = helmet_status  # helmet 값 업데이트
            user.save()  # 저장
            return Response({"message": "Helmet status updated successfully."}, status=status.HTTP_200_OK)
        except EmailVerification.DoesNotExist:
            return Response({"error": "User not found with this email."}, status=status.HTTP_404_NOT_FOUND)
