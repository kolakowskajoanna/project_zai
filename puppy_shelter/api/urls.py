
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from api import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

router.register(r'adopters', views.AdopterViewSet)
# todo: kolejne

urlpatterns = [
    path('ping', views.ping, name='ping'),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('func/list_users', views.list_users, name='f-list_users'),
]
