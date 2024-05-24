from django.urls import path
from .views import register, EmailLoginView, EmailLogoutView, authenticated, home

urlpatterns = [
    path('', home, name='home'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('logout/', EmailLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('authenticated/', authenticated, name='authenticated'),
]
