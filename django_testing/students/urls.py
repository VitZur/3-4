from  django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CoursesViewSet


router = DefaultRouter()
router.register("courses", CoursesViewSet, basename="courses")

urlpatterns = router.urls