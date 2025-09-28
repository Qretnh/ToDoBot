from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, TaskViewSet, UserCreateAPIView

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("users/", UserCreateAPIView.as_view(), name="user-create"),  # сюда!
]
