from django.contrib import admin
from django.urls import path,  include

#8/3 추가한부분
# from django.conf.urls import url, include
# from rest_framework import routers
# from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('users/', include('authentication.api.urls'), name='authentication'),
    # url(r'^rest-auth/', include('rest_auth.urls')),
    # url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),


]
