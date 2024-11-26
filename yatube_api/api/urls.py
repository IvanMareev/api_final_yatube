from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

urlpatterns = [
    path('', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
