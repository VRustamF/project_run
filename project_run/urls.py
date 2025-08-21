"""
URL configuration for project_run project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import path, include

from app_run.views import (company_details, RunViewSet, UserViewSet, StopAPIView, StartAPIView, AthleteInfoAPIView,
                           ChallengesViewSet, PositionViewSet, CollectibleItemViewSet, CollectibleItemAPIView,
                           SubscribeAPIView)

from debug_toolbar.toolbar import debug_toolbar_urls

router = DefaultRouter()
router.register('api/runs', viewset=RunViewSet)
router.register('api/users', viewset=UserViewSet)
router.register('api/challenges', viewset=ChallengesViewSet)
router.register('api/positions', viewset=PositionViewSet)
router.register('api/collectible_item', viewset=CollectibleItemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/company_details/', company_details, name='company_details'),
    path('', include(router.urls)),
    path('api/runs/<int:run_id>/start/', StartAPIView.as_view(), name='start_run'),
    path('api/runs/<int:run_id>/stop/', StopAPIView.as_view(), name='stop_run'),
    path('api/athlete_info/<int:user_id>/', AthleteInfoAPIView.as_view(), name='athlete_info'),
    path('api/upload_file/', CollectibleItemAPIView.as_view(), name='upload_collectible_file'),
    path('api/subscribe_to_coach/<int:coach_id>/', SubscribeAPIView.as_view(), name='subscribe_to_coach'),
] + debug_toolbar_urls()

