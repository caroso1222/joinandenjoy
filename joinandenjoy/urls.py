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
    url(r'^generate/', views.generate2, name ="generate"),
    url(r'^emails_spa/', views.emails_spa3, name ="emails_spa"),
    url(r'^adriana-barreneche-450679/', TemplateView.as_view(template_name="adriana-barreneche.html")),
    url(r'^armonia-naturall-spa-403921/', TemplateView.as_view(template_name="armonia-naturall-spa.html")),
    url(r'^beauty-in-motion-carolina-serrano-209310/', TemplateView.as_view(template_name="beauty-in-motion-carolina-serrano.html")),
    url(r'^bellas-y-esbeltas-450679/', TemplateView.as_view(template_name="bellas-y-esbeltas.html")),
    url(r'^bioesthetic-laser-113343/', TemplateView.as_view(template_name="bioesthetic-laser.html")),
    url(r'^clinica-estetica-laser-231564/', TemplateView.as_view(template_name="clinica-estetica-laser.html")),
    url(r'^dana-spa-442433/', TemplateView.as_view(template_name="dana-spa.html")),
    url(r'^divina-vanidad-231564/', TemplateView.as_view(template_name="divina-vanidad.html")),
    url(r'^dr-fernando-ruiz-gaitan-455032/', TemplateView.as_view(template_name="dr-fernando-ruiz-gaitan.html")),
    url(r'^maja-spa-159291/', TemplateView.as_view(template_name="maja-spa.html")),
    url(r'^marisol-caro-159291/', TemplateView.as_view(template_name="marisol-caro.html")),
    url(r'^splendor-centro-de-estetica-159291/', TemplateView.as_view(template_name="splendor-centro-de-estetica.html")),
    url(r'^wow-gentestilos-peluqueria-spa-159291/', TemplateView.as_view(template_name="wow-gentestilos-peluqueria-spa.html")),
    url(r'^p/', include('main.urls_propuesta')),
]