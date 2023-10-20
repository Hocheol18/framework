from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=100)

class Article(models.Model):
    topics = models.ManyToManyField(Topic, blank=True, null=True)
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 조회수는 상세 페이지에서만 조회 가능하다고 가정
    views = models.IntegerField(default=0)

class Comment(models.Model):
    comment = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 매직 메서드를 사용해서 따로 호출해야 함!
    def __str__(self):
        return self.content
