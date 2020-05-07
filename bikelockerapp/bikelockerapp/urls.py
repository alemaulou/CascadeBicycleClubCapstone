from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.views.generic import RedirectView
from rest_framework import routers, serializers, viewsets
from django.contrib import admin
from django.urls import include, path
from . import views

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
admin.site.site_header = 'Cascade Bicycle Club Locker Management Admin'
admin.site.index_title = 'Cascade Bicycle Club Locker Management'

urlpatterns = [
    path('admin/database/', include('database.urls')),
    path('admin/', RedirectView.as_view(url='database')),
    path('admin/', admin.site.urls),
    path('maintenance_report/', views.maintenance_report, name='maintenance-report'),
    path('', views.customer_inquiry, name='landing'),
    url(r'^select2/', include('django_select2.urls')),
]