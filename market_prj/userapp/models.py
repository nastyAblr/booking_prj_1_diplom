from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars/', blank=True, null=True)
    email = models.EmailField(unique=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class CustomUserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ('user',)



    def __str__(self):
        return f'Профиль {self.user.username}'




