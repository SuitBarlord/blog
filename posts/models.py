from django.db import models
from users.models import CustomUser

# Create your models here.



class Post(models.Model):
    id = models.AutoField(primary_key=True, unique=True)    
    topic = models.CharField(max_length=256, blank=False, verbose_name='Тема поста')
    content = models.TextField(max_length=4000, blank=False, verbose_name='Текст поста')
    number_likes = models.IntegerField(default=0, blank=True, verbose_name='Лайки')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Автор')
    date_publish = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    def __str__(self) -> str:
        return self.topic