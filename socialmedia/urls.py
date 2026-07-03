from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from accounts.views import landing


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', landing, name='landing'),

    path('', include('accounts.urls')),

    path('', include('posts.urls')),

]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )