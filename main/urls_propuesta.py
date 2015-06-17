from django.conf.urls import include, url
from django.views.generic import TemplateView
from main import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'hype.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^$', views.home, name ="index"),
    url(r'^spa/(?P<slug>[^\.]+)', views.ver_spa, name='view_spa'),
    url(r'^cirujano/(?P<slug>[^\.]+)', views.ver_cirujano, name='view_cirujano'),
]