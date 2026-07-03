from django.urls import path
from .views import landing,register,user_login,user_logout
from .views import profile,follow_user,edit_profile

urlpatterns = [
   
    path('', landing, name='landing'),
    path('register/',register,name="register"),
    path('login/',user_login,name="login"),
    path('logout/',user_logout,name='logout'),
    path('profile/<str:username>/', profile, name='profile'),
    path('follow/<str:username>/',follow_user, name='follow_user'),
    path("edit-profile/",edit_profile,name="edit_profile"),


]