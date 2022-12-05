"""notifier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework.schemas import get_schema_view

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from mainapp import views


router = DefaultRouter()
router.register(
    r'customers',
    views.CustomerViewSet,
    basename='customer'
)
router.register(
    r'mailing_lists',
    views.MailingListViewSet,
    basename='mailing_list'
)
router.register(
    r'mailing_lists_statistics',
    views.MailingListsStatisticsViewSet,
    basename='mailing_lists_statistics'
)
router.register(
    r'active_mailing_lists',
    views.ActiveMailingListsViewSet,
    basename='active_mailing_lists'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('openapi', get_schema_view(
        title='Notifier',
        description='API for notifier',
        version='0.1.0'
    ), name='openapi-schema'),
    path('doc/', TemplateView.as_view(
        template_name='mainapp/doc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='doc'),
]
