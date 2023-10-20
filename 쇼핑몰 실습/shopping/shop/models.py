from django.db import models
from django.conf import settings

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    # 이미지 URL 저장
    image = models.URLField()
    # 장바구니 > 중계키 생성 (Product:User = M:N)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='cart', blank=True)
