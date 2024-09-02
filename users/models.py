from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



# Создаем кастомную модель пользователя, наследуем от AbstractUser 
class CustomUser(AbstractUser):
    gender_choices = (
        ('masc', 'Мужской'),
        ('femn', 'Женский'),
    )
    # Выбор пола
    gender = models.CharField(max_length=4, choices=gender_choices, blank=False, default='femn', verbose_name='Пол')