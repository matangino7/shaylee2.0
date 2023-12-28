from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuardRoundViewSet, OrganizeShifts

router = DefaultRouter()
router.register(r'guard-rounds', GuardRoundViewSet, basename='guard_round')

urlpatterns = [
    path('shifts/', include(router.urls)),
    path('calendar/', OrganizeShifts.as_view, name="calendar"),
]
