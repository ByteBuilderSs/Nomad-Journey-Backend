"""NormandJourney URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/' , include('accounts.urls')),
    path('announcement/', include('announcement.urls')),
    path('blog/', include('blog.urls')),
    path('ticket/' , include('ticket.urls')),
    path('anc_request/', include('anc_request.urls')),
    path('utils/', include('utils.urls')),
    path('feedback/', include('feedback.urls')),
    path('like_post/', include('like_post.urls')),
    path('landing-page/' , include('landing_page.urls')),
    path('notification/', include('notification.urls'))
]

urlpatterns = [
    path('api/v1/', include(urlpatterns), name='api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
