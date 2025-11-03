"""
URL configuration for examPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from api.views import UserCreateView
from student.views import DashboardView, custom_logout_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from exam.views import LandingPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing'),  # Landing page at root
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),  # Login page
    path('signup/', TemplateView.as_view(template_name='signup.html'), name='signup'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  # New dashboard route
    path('api/user/register/', UserCreateView.as_view(), name='user-create'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework.urls')),
    path('logout/', custom_logout_view, name='logout'),
    # Include exam URLs
    path('', include('exam.urls')),
    # Include student URLs
    path('', include('student.urls')),
    # Include teacher URLs
    path('teacher/', include('teacher.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

