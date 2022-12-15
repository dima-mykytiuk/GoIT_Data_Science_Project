from django.conf import settings
from django.conf.urls.static import static
from django.conf import urls
from django.urls import path, re_path
from django.views.static import serve

from fileuploader.views import IndexView, AboutView, LoginView, RegistrationView, LogOutView, ProfileView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]