from django.urls import path
import userapp.views as userapp


app_name = 'userapp'

urlpatterns = [
    path('login/', userapp.login, name='login'),
    path('logout/', userapp.logout, name='logout'),
    path('register/', userapp.register, name='register'),
    path('profile/', userapp.profile, name='profile'),

    path('profile/edit/', userapp.profile_edit, name='profile_edit')


]
