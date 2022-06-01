
from django.urls import path, include
from rest_framework import routers
from api import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    path('ping/', views.ping, name='ping'),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls'))
]
