from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('company', views.CompanyViewSet)
router.register('anonym', views.AnonymViewSet)
router.register('secure', views.SecureViewSet)
router.register('manager', views.ManagerViewSet)


urlpatterns = [
    url(r'', include(router.urls)),
]