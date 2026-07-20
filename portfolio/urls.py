from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonalInfoViewSet, SkillViewSet, ProjectViewSet, ContactMessageViewSet

router = DefaultRouter()
router.register(r'personal', PersonalInfoViewSet, basename='personal')
router.register(r'skills', SkillViewSet, basename='skills')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'contact', ContactMessageViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
]
