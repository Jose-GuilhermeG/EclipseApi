
from django.contrib import admin
from django.urls import path , include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
from oauth2_provider import urls as oauth_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(("product.urls","product") , namespace='product')),
    path('auth/', include(("users.urls","users") , namespace='auth')),
    path('workplace/', include(("workplace.urls","workplace") , namespace='workplace')),
]

#docs
urlpatterns += [
     path(
        'docs/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        'docs/', 
        SpectacularSwaggerView.as_view(url_name='schema'), 
        name='swagger-ui'
    ),
]

urlpatterns += [
    path('auth//', include(oauth_urls,namespace="oauth2_provider"))
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)