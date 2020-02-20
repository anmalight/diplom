"""diplom001 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cinema.views import GoodViewSet, UserViewSet, MovieViewApi, MovieSessionViewApi
from diplom001 import settings

router = DefaultRouter()
router.register(r'moviee', MovieViewApi)
router.register(r'movieesession', MovieSessionViewApi)


router.register(r'session', GoodViewSet)
router.register(r'user', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('', include('cinema.urls')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
