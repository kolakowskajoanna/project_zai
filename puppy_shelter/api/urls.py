
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from api import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet, basename="users")
router.register(r'groups', views.GroupViewSet, basename="groups")

router.register(r'adopters', views.AdopterViewSet, basename="adopters")
router.register(r'adoption-employees', views.AdoptionEmployeeViewSet, basename="adoption-employees")
router.register(r'adoption-users', views.AdoptionUserViewSet, basename="adoption-users")
router.register(r'puppys', views.PuppyViewSet, basename="puppys")

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
