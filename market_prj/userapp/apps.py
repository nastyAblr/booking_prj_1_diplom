from django.apps import AppConfig


class UserappConfig(AppConfig):
    name = 'userapp'
    verbose_name = 'Пользователи'

    def ready(self):
        import userapp.signals