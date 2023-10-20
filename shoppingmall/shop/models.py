from django.db import models
from django.conf import settings


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    # 이미지 URL 을 저장
    image = models.URLField()
    # 장바구니(Product:User = M:N)
    # related_name : 역참조 시 사용할 이름
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='cart', blank=True)    
