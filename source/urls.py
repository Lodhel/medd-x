from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register('company', views.CompanyViewSet)
router.register('anonym', views.AnonymViewSet)
router.register('secure', views.SecureViewSet)
router.register('manager', views.ManagerViewSet)
router.register('assistant', views.AssistantViewSet)
router.register('translator', views.TranslatorViewSet)
router.register('physician', views.PhysicianViewSet)

router.register('choice_attachment', views.ChoiceAttachmentViewSet)
router.register('choice_gender', views.ChoiceGenderViewSet)
router.register('choice_age_groups', views.ChoiceAgeGroupsViewSet)
router.register('choice_destination_block', views.ChoiceDestinationBlockViewSet)
router.register('choice_destination_chapter', views.ChoiceDestinationChapterViewSet)
router.register('choice_default_block', views.ChoiceDefaultBlockViewSet)
router.register('choice_default_chapter', views.ChoiceDefaultChapterViewSet)
router.register('choice_health_status', views.ChoiceHealthStatusViewSet)
router.register('choice_bio_market', views.ChoiceBioMarketViewSet)
router.register('choice_meddata_type', views.ChoiceMeddataTypeViewSet)
router.register('choice_measurment_default', views.ChoiceMeasurmentDefaultViewSet)
router.register('choice_measurment', views.ChoiceMeasurmentViewSet)


urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'', include(router.urls)),
]