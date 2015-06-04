from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from main import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'joinandenjoy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name ="home"),
    url(r'^adriana-barreneche-450679/', TemplateView.as_view(template_name="adriana-barreneche.html")),
]