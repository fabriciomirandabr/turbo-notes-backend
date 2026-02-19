from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CategoryViewSet, NoteViewSet, SignupView

router = DefaultRouter(trailing_slash=False)
router.register("notes", NoteViewSet, basename="note")
router.register("categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("auth/signup", SignupView.as_view(), name="signup"),
    path("auth/login", TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
