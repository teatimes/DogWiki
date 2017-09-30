from src.apps.dogwiki import views
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from src.apps.authentication import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^contact/', views.ContactUsView.as_view(), name='contact_us'),

    url(r'^accounts/login/', auth_views.login, name='auth_login'),
    url(r'^', include('src.apps.authentication.urls')),

    url(r'^litterature/', include('src.apps.litterature.urls')),

    url(r'^profile/', include('src.apps.profile.urls')),

    url(r'^forum/', include('src.apps.forum.urls')),

    url(r'^400/', TemplateView.as_view(template_name='400.html')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
