from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  CollegeDataViewset, CollegeViewSet


router = DefaultRouter()

router.register(r'colleges', CollegeDataViewset , basename='colleges')
router.register(r'college_views', CollegeViewSet , basename='college_views')

urlpatterns = [

    path('college/', include(router.urls)),
    path('college_view/',include(router.urls))
]
