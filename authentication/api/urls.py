from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('register', views.RegistrationAPIView.as_view()),
    path('login', views.LoginAPIView.as_view()),
    path('state', views.UserView.as_view()),
    path('current', views.UserRetrieveUpdateAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
