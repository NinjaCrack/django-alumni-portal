"""
URL configuration for alumniwebsite project.

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

from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('authentication.urls')),
    path('', include('homepage.urls')),
    path('', include('events.urls')),
    path('', include('articles.urls')),
    path('', include('services.urls')),
    path('', include('careers.urls')),
    path('', include('about.urls')),
    path('', include('faculty.urls')),
    path('', include('users.urls')),
    path('', include('story.urls')),
    path('', include('alumninetwork.urls')),

    path('home/', include('homepage.urls')),
    path('help-email/', views.help_email , name='help_email'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),
    path('.well-known/security.txt', views.security_txt),
    path("csp-report/", views.csp_report_view, name="csp-report"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)