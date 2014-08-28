from django.conf.urls import patterns, url

from auskunft import views

urlpatterns = patterns('',
    url(r'^$',views.address,name='address'),
    url(r'^address$',views.address,name='address'),
    url(r'^addinfo$',views.addinfo,name='addinfo'),
    url(r'^delivery$',views.delivery,name='delivery')
)
