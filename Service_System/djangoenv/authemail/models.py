from django.db import models

# Create your models here.
class EmailVerification(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    verification_code = models.CharField(max_length=6)
    helmet = models.BooleanField(default=False)  # 헬멧 착용 여부, 기본값 False
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return self.email
