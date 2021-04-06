from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.register),
    path('profile/', views.profile),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('posts/', include('posts.urls')),
    path('music/', include('music.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 